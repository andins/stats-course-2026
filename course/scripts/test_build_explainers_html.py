import html
import json
import pathlib
import posixpath
import re
import unittest
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

import build_explainers_html as builder
import workflow_diagram


class PageParser(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids = []
        self.links = []
        self.scripts = []
        self.images = []
        self.current_pages = []
        self.language_links = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if "href" in attrs and attrs.get("class") != "lang-switch":
            self.links.append(attrs["href"])
        if attrs.get("class") == "lang-switch":
            self.language_links.append(attrs["href"])
        if tag == "img":
            self.images.append((attrs.get("src", ""), attrs.get("alt", "")))
        if tag == "script" and "src" in attrs:
            self.scripts.append(attrs["src"])
        if attrs.get("aria-current") == "page":
            self.current_pages.append(attrs["href"])


class CourseBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.documents = {}
        for path, anchor, title, _ in builder.STRUCTURE:
            filename = builder.page_href(anchor, "home")
            cls.documents[filename] = builder.build_document(
                anchor, title, builder.convert_page(path, anchor),
            )
        cls.pages = {name: PageParser(doc) for name, doc in cls.documents.items()}

    def test_root_page_links_to_every_language(self):
        root = builder.build_root_page()
        for lang in builder.course_i18n.UI:
            with self.subTest(lang=lang):
                self.assertIn(f'href="{lang}/index.html"', root)
                self.assertTrue((builder.COURSE_DIR / lang / "index.html").is_file())

    def test_one_topic_per_page(self):
        self.assertEqual(len(self.pages), 49)
        for filename, doc in self.documents.items():
            with self.subTest(page=filename):
                self.assertEqual(doc.count('<section id='), 1)
                labels = "|".join(re.escape(builder.UI[key]) for key in ("previous", "next", "next_module", "previous_module"))
                self.assertNotRegex(doc, rf'<strong>(?:{labels}):</strong>')
                page = self.pages[filename]
                self.assertTrue(page.language_links)
                self.assertRegex(doc, r'<a class="lang-switch"[^>]*><svg[^>]*aria-hidden="true"')
                self.assertEqual(len(page.ids), len(set(page.ids)))
                self.assertEqual(len(page.current_pages), 1)
                current = posixpath.normpath(posixpath.join(
                    posixpath.dirname(filename), page.current_pages[0],
                ))
                self.assertEqual(current, filename)

    def test_all_generated_links_and_assets_resolve(self):
        assets = {
            "pages/course.css",
            "pages/course.js",
        } | {
            f"pages/notebooks/{path.name}"
            for path in builder.NOTEBOOKS_SRC.iterdir() if path.is_file()
        }
        for filename, page in self.pages.items():
            for href in page.links + page.scripts:
                url = urlsplit(href)
                if url.scheme or url.netloc:
                    continue
                with self.subTest(page=filename, href=href):
                    target = posixpath.normpath(posixpath.join(
                        posixpath.dirname(filename), unquote(url.path),
                    )) if url.path else filename
                    self.assertIn(target, set(self.pages) | assets)
                    if url.fragment:
                        self.assertIn(unquote(url.fragment), self.pages[target].ids)

    def test_figures_resolve_have_alt_text_and_captions(self):
        available = {f"pages/figures/{path.name}" for path in builder.FIGURES_SRC.glob("*.png")}
        shown = set()
        for filename, page in self.pages.items():
            with self.subTest(page=filename):
                doc = self.documents[filename]
                self.assertEqual(len(page.images), doc.count("<figure>"))
                self.assertEqual(doc.count("<figcaption>"), doc.count("<figure>"))
                for src, alt in page.images:
                    target = posixpath.normpath(posixpath.join(posixpath.dirname(filename), unquote(src)))
                    self.assertIn(target, available)
                    self.assertGreater(len(alt.split()), 5, f"alt text of {src} is too short to describe the figure")
                    shown.add(target)
        self.assertEqual(shown, available, "every figure in markdown/figures/ should be used on a page")

    def test_figure_markup_requires_a_caption_and_an_existing_file(self):
        figure = next(builder.FIGURES_SRC.glob("*.png")).name
        image = f'<p><img src="../figures/{figure}" alt="Some alt text" /></p>'
        self.assertEqual(
            builder.style_figures(image + "<p><em>A <strong>caption</strong>.</em></p>", "05-prediction-vs-causation", "m5"),
            f'<figure><img src="figures/{figure}" alt="Some alt text" loading="lazy">'
            '<figcaption>A <strong>caption</strong>.</figcaption></figure>',
        )
        self.assertIn(
            f'src="pages/figures/{figure}"',
            builder.style_figures(f'<p><img src="figures/{figure}" alt="Some alt text" /></p><p><em>Cap.</em></p>', "", "home"),
        )
        with self.assertRaises(ValueError):       # no caption
            builder.style_figures(image + "<p>Not italic.</p>", "05-prediction-vs-causation", "m5")
        with self.assertRaises(ValueError):       # file does not exist
            builder.style_figures('<p><img src="../figures/nope.png" alt="x" /></p><p><em>Cap.</em></p>',
                                  "05-prediction-vs-causation", "m5")
        with self.assertRaises(ValueError):       # no alt text
            builder.style_figures(f'<p><img src="../figures/{figure}" alt="" /></p><p><em>Cap.</em></p>',
                                  "05-prediction-vs-causation", "m5")

    def test_no_page_loads_mermaid(self):
        for filename, page in self.pages.items():
            with self.subTest(page=filename):
                self.assertFalse(any("mermaid" in src for src in page.scripts))
                self.assertNotIn('class="mermaid"', self.documents[filename])

    def test_workflow_diagram_covers_the_whole_mermaid_flowchart(self):
        source = (builder.MARKDOWN_ROOT / "workflow-cheatsheet.md").read_text()
        mermaid = re.search(r"```mermaid\n(.*?)```", source, re.DOTALL).group(1)
        graph = workflow_diagram.parse_mermaid(mermaid)
        self.assertEqual(len(graph["nodes"]), 17)
        self.assertEqual(len(graph["edges"]), 20)
        self.assertEqual(set(graph["nodes"]), set(workflow_diagram.LAYOUT))
        self.assertEqual({sub for sub, _, _ in workflow_diagram.BANDS}, set(graph["subgraphs"]))

        doc = self.documents["pages/workflow.html"]
        self.assertEqual(doc.count('class="wf-node '), 17)
        self.assertEqual(doc.count('<div class="wf-band"'), 4)
        self.assertIn('<main id="content" class="wide">', doc)
        edges = json.loads(html.unescape(re.search(r'data-edges="([^"]*)"', doc).group(1)))
        self.assertEqual(len(edges), 20)
        self.assertEqual(sum(1 for edge in edges if edge[3]), 1)   # the single dashed "once collected" edge

    def test_diagram_boxes_link_to_topic_pages(self):
        page = self.pages["pages/workflow.html"]
        box_links = re.findall(r'<a class="wf-node [^"]*" href="([^"]+)"', self.documents["pages/workflow.html"])
        self.assertEqual(len(box_links), 17)
        for href in box_links:
            self.assertIn(f"pages/{href}", self.pages)
        self.assertEqual(len(page.current_pages), 1)

    def test_layout_cells_do_not_overlap(self):
        cells = set()
        for node_id, (row, col, span) in workflow_diagram.LAYOUT.items():
            for c in range(col, col + span):
                self.assertNotIn((row, c), cells, f"{node_id} overlaps another node")
                cells.add((row, c))
            self.assertLessEqual(col + span - 1, 6)

    def test_diagram_refuses_a_layout_that_disagrees_with_the_flowchart(self):
        with self.assertRaises(ValueError):
            workflow_diagram.render('flowchart TD\n    X["X: only node"]\n', lambda href: href)

    def test_footer_stripping_preserves_content_and_markdown_sources(self):
        markdown = f"# Topic\n\n---\n\nBody.\n\n---\n**{builder.UI['previous']}:** [Home](./README.md)\n"
        self.assertEqual(builder.strip_footer_navigation(markdown), "# Topic\n\n---\n\nBody.\n\n")
        for path, _, _, _ in builder.STRUCTURE:
            source = (builder.MARKDOWN_ROOT / path).read_text()
            if re.search(r"\*\*(?:%s):\*\*" % "|".join(builder.UI[k] for k in ("previous", "next", "next_module", "previous_module")), source):
                self.assertNotEqual(source, builder.strip_footer_navigation(source))

    def test_learn_more_box_on_every_topic_and_module_page(self):
        for path, anchor, _, group in builder.STRUCTURE:
            if group is None or builder.is_howto(path):
                continue
            with self.subTest(page=anchor):
                source = (builder.MARKDOWN_ROOT / path).read_text()
                self.assertEqual(source.count(f"> **{builder.UI['learn_more']}**"), 1)
                doc = self.documents[builder.page_href(anchor, "home")]
                self.assertEqual(doc.count('<aside class="learn-more"'), 1)
                self.assertNotIn(f"<p><strong>{builder.UI['learn_more']}</strong></p>", doc)

    def test_every_howto_is_linked_from_a_do_it_yourself_box(self):
        howtos = {path: anchor for path, anchor, _, _ in builder.STRUCTURE if builder.is_howto(path)}
        self.assertTrue(howtos)
        for path, anchor in howtos.items():
            with self.subTest(howto=anchor):
                filename = builder.page_href(anchor, "m6")  # relative link, as written from a topic page
                linking_pages = []
                for other_path, other_anchor, _, _ in builder.STRUCTURE:
                    if builder.is_howto(other_path):
                        continue
                    doc = self.documents[builder.page_href(other_anchor, "home")]
                    for box in re.findall(r'<aside class="do-it-yourself".*?</aside>', doc, re.DOTALL):
                        if f'href="{filename}"' in box:
                            linking_pages.append(other_anchor)
                self.assertTrue(linking_pages, f"{anchor} has no 'Do it yourself' box pointing to it")

    def test_howto_pages_are_marked_in_the_sidebar(self):
        for path, anchor, _, _ in builder.STRUCTURE:
            if not builder.is_howto(path):
                continue
            with self.subTest(howto=anchor):
                doc = self.documents[builder.page_href(anchor, "home")]
                self.assertIn('class="toc-link toc-howto active"', doc)

    def test_notebook_links_are_rewritten_per_page_depth(self):
        notebook = next(builder.NOTEBOOKS_SRC.glob("*.ipynb"))
        body = f'<a href="../notebooks/{notebook.name}">NB</a>'
        self.assertEqual(
            builder.rewrite_links(body, "06-building-models", "m6-measurement-error"),
            f'<a href="notebooks/{notebook.name}" download>NB</a>',
        )
        self.assertEqual(
            builder.rewrite_links(body, "06-building-models", "home"),
            f'<a href="pages/notebooks/{notebook.name}" download>NB</a>',
        )
        with self.assertRaises(ValueError):
            builder.rewrite_links('<a href="../notebooks/missing.ipynb">NB</a>', "06-building-models", "m6")

    def test_top_level_pages_are_sidebar_links_in_structure_order(self):
        top_level = [anchor for _, anchor, _, group in builder.STRUCTURE if group is None]
        self.assertEqual(top_level[:5], ["home", "setup-environment", "project-structure", "use-an-agent", "workflow"])
        self.assertEqual(top_level[-1], "glossary")
        toc = builder.build_toc("home")
        previous = -1
        for anchor in top_level:
            position = toc.index(f'href="{builder.page_href(anchor, "home")}"')
            self.assertGreater(position, previous, f"{anchor} is out of order in the sidebar")
            previous = position

    def test_setup_pages_link_to_each_other_and_to_the_requirements_file(self):
        setup = self.documents["pages/setup-environment.html"]
        project = self.documents["pages/project-structure.html"]
        self.assertIn('href="project-structure.html"', setup)
        self.assertIn('href="setup-environment.html"', project)
        self.assertIn('href="notebooks/requirements.txt" download', setup)
        self.assertTrue((builder.NOTEBOOKS_SRC / "requirements.txt").is_file())

    def test_fragment_and_cross_page_links(self):
        body = '<a href="#details">Local</a><a href="./effect-size.md#why">Other</a>'
        self.assertEqual(
            builder.rewrite_links(body, "01-planning-your-study", "m1"),
            '<a href="#m1--details">Local</a>'
            '<a href="m1-effect-size.html#m1-effect-size--why">Other</a>',
        )


class TranslationParityTests(unittest.TestCase):
    """A translation must mirror the English course: same pages, code, structure and links."""

    CODE_RE = re.compile(r"```(?!mermaid).*?```", re.DOTALL)   # the Mermaid diagram holds translated labels
    HEADING_RE = re.compile(r"^(#{1,6}) ", re.MULTILINE)
    LINK_TARGET_RE = re.compile(r"\]\(([^)#\s]+)")

    def setUp(self):
        self.english = builder.language_root("en") / "markdown"

    def pairs(self):
        for path, _, _, _ in builder.STRUCTURE:
            yield path, (self.english / path).read_text(), (builder.MARKDOWN_ROOT / path).read_text()

    @unittest.skipIf(builder.LANG == "en", "only translations are compared with English")
    def test_translation_mirrors_the_english_source(self):
        for path, english, translated in self.pairs():
            with self.subTest(page=path):
                self.assertEqual(self.CODE_RE.findall(translated), self.CODE_RE.findall(english), "code blocks differ")
                self.assertEqual(self.HEADING_RE.findall(translated), self.HEADING_RE.findall(english))
                # sorted: the glossary is alphabetical, so translated entries come in a different order
                self.assertEqual(sorted(self.LINK_TARGET_RE.findall(translated)), sorted(self.LINK_TARGET_RE.findall(english)))
                self.assertEqual(translated.count("\n|"), english.count("\n|"), "table rows differ")

    @unittest.skipIf(builder.LANG == "en", "only translations are compared with English")
    def test_translation_has_the_same_notebooks_and_figures(self):
        for kind, source in (("notebooks", builder.NOTEBOOKS_SRC), ("figures", builder.FIGURES_SRC)):
            with self.subTest(kind=kind):
                expected = sorted(p.name for p in (self.english / kind).iterdir() if not p.name.startswith("."))
                self.assertEqual(sorted(p.name for p in source.iterdir() if not p.name.startswith(".")), expected)

    @unittest.skipIf(builder.LANG == "en", "only translations are compared with English")
    def test_notebook_code_cells_are_unchanged(self):
        for notebook in (self.english / "notebooks").glob("*.ipynb"):
            with self.subTest(notebook=notebook.name):
                def code(path):
                    return [c["source"] for c in json.loads(path.read_text())["cells"] if c["cell_type"] == "code"]
                self.assertEqual(code(builder.NOTEBOOKS_SRC / notebook.name), code(notebook))


SKILL_TOPICS = pathlib.Path(__file__).resolve().parents[2] / "statistics-advisor" / "references" / "course-topics.md"


@unittest.skipUnless(SKILL_TOPICS.is_file(), "the sibling statistics-advisor skill folder is not present")
@unittest.skipUnless(builder.LANG == "en", "the skill's topic list is in English")
class SkillTopicListTests(unittest.TestCase):
    """The skill names course pages without linking to them, so its list must match the course exactly."""

    @staticmethod
    def parse_list():
        """Return {section heading: [bullet titles]} for the headings of the skill's course-topics.md."""
        sections, current = {}, None
        for line in SKILL_TOPICS.read_text().splitlines():
            if line.startswith("## "):
                current = line[3:].strip()
                sections[current] = []
            elif current is not None and line.startswith("- ") and current != "Which page for which situation":
                sections[current].append(line[2:].strip())
        return sections

    def test_every_module_lists_exactly_its_pages_and_howtos(self):
        sections = self.parse_list()
        for group, module_title in builder.GROUP_TITLES.items():
            number, name = module_title.split(". ", 1)
            heading = f"Module {number}: {name}"
            expected = [title for _, _, title, g in builder.STRUCTURE if g == group and title != module_title]
            with self.subTest(module=heading):
                self.assertIn(heading, sections)
                self.assertEqual(sections[heading], expected)

    def test_general_pages_match_the_top_level_sidebar_pages(self):
        expected = [title for _, _, title, group in builder.STRUCTURE if group is None and title != "Home"]
        self.assertEqual(self.parse_list()["General pages"], expected)

    def test_notebooks_listed_are_the_notebooks_that_exist(self):
        listed = self.parse_list()["Notebooks (linked from the \"Do it yourself\" boxes)"]
        names = sorted(re.sub(r" \(module \d\)$", "", item) for item in listed)
        self.assertEqual(names, sorted(path.stem for path in builder.NOTEBOOKS_SRC.glob("*.ipynb")))

    def test_no_stale_titles(self):
        all_titles = {title for _, _, title, _ in builder.STRUCTURE}
        for heading, items in self.parse_list().items():
            if heading.startswith(("Module", "General")):
                for item in items:
                    with self.subTest(heading=heading, item=item):
                        self.assertIn(item, all_titles)


if __name__ == "__main__":
    unittest.main()
