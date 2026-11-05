"""Render the workflow cheatsheet's Mermaid flowchart as a wide, readable HTML layout.

The markdown keeps its Mermaid diagram (GitHub and VS Code render it). For the HTML course the
same flowchart is redrawn here: boxes are real links laid out on a grid (four phase bands, using
the full page width) and a small script draws the arrows between them from the boxes' measured
positions. Node text, shapes, edges, edge labels and links all come from the Mermaid source, so
the content has a single source of truth; only the grid positions (LAYOUT) are defined here.

Below a minimum width the arrows are dropped and the boxes stack in reading order, each followed
by a plain "leads to" list, so the flow stays usable on narrow screens and for screen readers.
"""

from __future__ import annotations

import html
import json
import re
from typing import Callable

import course_i18n

# node id -> (grid row, first column, column span) on a 6-column grid.
LAYOUT = {
    "A": (1, 1, 2), "B": (1, 3, 2), "B1": (1, 5, 2),
    "C": (2, 3, 2),
    "F": (3, 1, 2), "D": (3, 5, 2),
    "F1": (4, 1, 2), "Z1": (4, 3, 2),
    "E": (5, 5, 2), "H": (5, 1, 2),
    "I": (6, 1, 2), "J": (6, 3, 2), "G": (6, 5, 2),
    "K": (7, 3, 2),
    "Z2": (8, 1, 2), "L": (8, 3, 2), "Z3": (8, 5, 2),
}
# (subgraph id in the Mermaid source, first grid row, last grid row)
BANDS = [("S0", 1, 1), ("S1", 2, 4), ("S2", 5, 7), ("S3", 8, 8)]

NODE_RE = re.compile(r'\b([A-Za-z]\w*)(\(\[|\{|\[)"(.*?)"(\]\)|\}|\])')
EDGE_RE = re.compile(r'^\s*(\w+)\s*(-->|-\.->)\s*(?:\|(.*?)\|)?\s*(\w+)\s*$')
SUBGRAPH_RE = re.compile(r'^\s*subgraph\s+(\w+)\["(.*?)"\]')
CLASS_RE = re.compile(r'^\s*class\s+([\w,]+)\s+(\w+);')
CLICK_RE = re.compile(r'^\s*click\s+(\w+)\s+"([^"]+)"(?:\s+"([^"]*)")?')
SHAPE_KIND = {"{": "decision", "[": "process", "([": "terminal"}


def parse_mermaid(source: str) -> dict:
    """Extract nodes, edges, subgraph titles and click links from the flowchart source."""
    nodes: dict[str, dict] = {}
    edges: list[dict] = []
    subgraphs: dict[str, str] = {}
    kinds: dict[str, str] = {}
    clicks: dict[str, tuple[str, str]] = {}

    for raw_line in source.splitlines():
        line = raw_line.strip()
        if not line or line.startswith(("flowchart", "classDef", "style", "end")):
            continue
        if m := SUBGRAPH_RE.match(line):
            subgraphs[m.group(1)] = m.group(2).replace(r"\n", " ")
            continue
        if m := CLASS_RE.match(line):
            for node_id in m.group(1).split(","):
                kinds[node_id] = m.group(2)
            continue
        if m := CLICK_RE.match(line):
            clicks[m.group(1)] = (m.group(2), m.group(3) or "")
            continue

        for node_id, opener, label, _closer in NODE_RE.findall(line):
            text = label.replace(r"\n", " ").strip()
            text = re.sub(rf"^{re.escape(node_id)}:\s*", "", text)
            nodes[node_id] = {"id": node_id, "text": text, "kind": SHAPE_KIND[opener]}
        bare = NODE_RE.sub(lambda m: m.group(1), line)
        if m := EDGE_RE.match(bare):
            label = (m.group(3) or "").replace(r"\n", " ").strip().strip('"').strip()
            edges.append({"from": m.group(1), "to": m.group(4), "label": label, "dashed": m.group(2) == "-.->"})

    for node_id, kind in kinds.items():
        if node_id in nodes:
            nodes[node_id]["kind"] = kind
    for node_id, (href, tooltip) in clicks.items():
        if node_id in nodes:
            nodes[node_id]["href"], nodes[node_id]["tooltip"] = href, tooltip
    return {"nodes": nodes, "edges": edges, "subgraphs": subgraphs}


def _label_html(text: str) -> str:
    """Bold the lead-in before a colon ("Plan sample size: power ...") for scannability."""
    head, sep, tail = text.partition(":")
    if sep and len(head) <= 45:
        return f"<strong>{html.escape(head)}:</strong> {html.escape(tail.strip())}"
    return html.escape(text)


def render(source: str, resolve_href: Callable[[str], str], ui: dict[str, str] | None = None) -> str:
    """Return the HTML for the diagram. `resolve_href` maps a markdown link to the page URL.

    `ui` supplies the legend and default edge label (see course_i18n.UI); English when omitted.
    """
    ui = ui or course_i18n.UI[course_i18n.DEFAULT_LANG]
    graph = parse_mermaid(source)
    nodes, edges = graph["nodes"], graph["edges"]
    missing = set(nodes) ^ set(LAYOUT)
    if missing:
        raise ValueError(f"Workflow diagram nodes and LAYOUT disagree on: {sorted(missing)}")
    for edge in edges:
        for end in (edge["from"], edge["to"]):
            if end not in nodes:
                raise ValueError(f"Workflow diagram edge refers to unknown node {end!r}")

    outgoing: dict[str, list[dict]] = {node_id: [] for node_id in nodes}
    for edge in edges:
        outgoing[edge["from"]].append(edge)

    parts = [
        '<div class="wf-wrap" data-edges="',
        html.escape(json.dumps([[e["from"], e["to"], e["label"], e["dashed"]] for e in edges])),
        '">',
        f'<p class="wf-legend"><span class="wf-key wf-decision">{html.escape(ui["legend_decision"])}</span>'
        f'<span class="wf-key wf-process">{html.escape(ui["legend_process"])}</span>'
        f'<span class="wf-key wf-terminal">{html.escape(ui["legend_terminal"])}</span>'
        f'<span class="wf-hint">{html.escape(ui["legend_hint"])}</span></p>',
        '<div class="wf">',
    ]
    for subgraph_id, first_row, last_row in BANDS:
        title = html.escape(graph["subgraphs"].get(subgraph_id, subgraph_id))
        parts.append(
            f'<div class="wf-band" style="grid-row:{first_row} / {last_row + 1}">'
            f'<span class="wf-band-title">{title}</span></div>'
        )
    for node_id, node in nodes.items():
        row, col, span = LAYOUT[node_id]
        href = resolve_href(node["href"]) if "href" in node else None
        tooltip = f' title="{html.escape(node["tooltip"])}"' if node.get("tooltip") else ""
        tag_open = f'<a class="wf-node wf-{node["kind"]}" href="{html.escape(href)}"{tooltip}' if href else \
            f'<span class="wf-node wf-{node["kind"]}"'
        tag_close = "</a>" if href else "</span>"
        leads_to = "".join(
            f'<li>{html.escape(e["label"] or ui["edge_default"])} &rarr; {html.escape(nodes[e["to"]]["text"])}</li>'
            for e in outgoing[node_id]
        )
        parts.append(
            f'<div class="wf-item" style="grid-row:{row}; grid-column:{col} / span {span}">'
            f'{tag_open} data-node="{node_id}"><span class="wf-text">{_label_html(node["text"])}</span>{tag_close}'
            f'{f"<ul class=wf-next>{leads_to}</ul>" if leads_to else ""}</div>'
        )
    parts.append(
        '<svg class="wf-lines" aria-hidden="true"><defs>'
        '<marker id="wf-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker>'
        "</defs></svg>"
    )
    parts.append("</div></div>")
    return "".join(parts)


CSS = """
.wf-wrap{container-type:inline-size; margin:1.2rem 0 2rem;
  --wf-decision-bg:#fde68a; --wf-decision-bd:#b45309; --wf-decision-fg:#1c1917;
  --wf-process-bg:#bfdbfe; --wf-process-bd:#1d4ed8; --wf-process-fg:#1c1917;
  --wf-terminal-bg:#bbf7d0; --wf-terminal-bd:#15803d; --wf-terminal-fg:#1c1917;}
[data-theme="dark"] .wf-wrap{
  --wf-decision-bg:#3d3210; --wf-decision-bd:#d99a2b; --wf-decision-fg:#fde9a8;
  --wf-process-bg:#15294d; --wf-process-bd:#5b8def; --wf-process-fg:#dbe7ff;
  --wf-terminal-bg:#10331f; --wf-terminal-bd:#3fb86b; --wf-terminal-fg:#c9f5d8;}
.wf-legend{display:flex; flex-wrap:wrap; align-items:center; gap:.5rem 1rem; margin:0 0 .8rem; font-size:.85rem; color:var(--muted);}
.wf-key{padding:.15rem .7rem; border:2px solid; font-size:.8rem;}
.wf-hint{margin-left:auto;}
.wf{position:relative; display:grid; grid-template-columns:repeat(6,minmax(0,1fr));
  column-gap:4.5rem; row-gap:3.4rem; padding:2rem 1rem 1.2rem;}
.wf-band{grid-column:1 / -1; position:relative; margin:-1.6rem -1rem -1.4rem;
  background:var(--bg-alt); border:1px solid var(--border); border-radius:16px;}
.wf-band-title{position:absolute; z-index:2; top:.45rem; left:.8rem; padding:0 .25rem; font-size:.72rem; font-weight:650;
  letter-spacing:.07em; text-transform:uppercase; color:var(--muted); background:var(--bg-alt);}
.wf-item{position:relative; z-index:2; display:flex;}
.wf-node{flex:1; display:flex; align-items:center; justify-content:center; text-align:center;
  min-height:3.8rem; padding:.6rem .9rem; border:2px solid; border-radius:10px;
  font-size:.95rem; line-height:1.3; color:inherit; text-decoration:none;
  transition:box-shadow .15s ease, transform .15s ease;}
a.wf-node:hover{text-decoration:none; transform:translateY(-1px); box-shadow:0 5px 12px #0000002e;}
a.wf-node:focus-visible{outline:3px solid var(--accent); outline-offset:2px;}
.wf-decision{background:var(--wf-decision-bg); border-color:var(--wf-decision-bd); color:var(--wf-decision-fg); border-radius:14px;}
.wf-decision:not(.wf-key)::before{content:"\\25C6"; margin-right:.5rem; font-size:.7rem; flex:none;}
.wf-process{background:var(--wf-process-bg); border-color:var(--wf-process-bd); color:var(--wf-process-fg);}
.wf-terminal{background:var(--wf-terminal-bg); border-color:var(--wf-terminal-bd); color:var(--wf-terminal-fg); border-radius:999px;}
.wf-node strong{color:inherit;}
.wf-key.wf-decision{border-radius:14px;} .wf-key.wf-terminal{border-radius:999px;} .wf-key.wf-process{border-radius:6px;}
.wf-lines{position:absolute; inset:0; width:100%; height:100%; z-index:1; pointer-events:none; overflow:visible; color:var(--muted);}
.wf-lines path{fill:none; stroke:currentColor; stroke-width:1.6;}
.wf-lines path.wf-dashed{stroke-dasharray:5 4;}
.wf-label{position:absolute; z-index:3; transform:translate(-50%,-50%); padding:0 .3rem;
  max-width:6.5rem; text-align:center; font-size:.74rem; line-height:1.15; color:var(--text);
  background:var(--bg-alt); border-radius:4px; pointer-events:none;}
.wf-next{position:absolute; width:1px; height:1px; overflow:hidden; clip-path:inset(50%); white-space:nowrap;}
#content.wide{max-width:none;}
#content.wide .page > :not(.wf-wrap){max-width:860px;}
@container (max-width: 759px){
  .wf{display:flex; flex-direction:column; gap:.7rem; padding:.5rem 0;}
  .wf-band,.wf-lines,.wf-label,.wf-hint{display:none;}
  .wf-item{flex-direction:column; grid-row:auto!important; grid-column:auto!important;}
  .wf-next{position:static; width:auto; height:auto; overflow:visible; clip-path:none; white-space:normal;
    list-style:none; margin:.2rem 0 0; padding:0 0 0 1rem; font-size:.82rem; color:var(--muted);}
}
"""

JS = """
(function () {
  const wrap = document.querySelector('.wf-wrap');
  if (!wrap) return;
  const grid = wrap.querySelector('.wf');
  const svg = wrap.querySelector('.wf-lines');
  const edges = JSON.parse(wrap.dataset.edges);
  const MIN_WIDTH = 760, RADIUS = 9, BUS = 20, NS = 'http://www.w3.org/2000/svg';

  const rounded = (pts) => {
    let d = `M${pts[0].x},${pts[0].y}`;
    for (let i = 1; i < pts.length - 1; i++) {
      const prev = pts[i - 1], cur = pts[i], next = pts[i + 1];
      const r1 = Math.min(RADIUS, Math.hypot(cur.x - prev.x, cur.y - prev.y) / 2);
      const r2 = Math.min(RADIUS, Math.hypot(next.x - cur.x, next.y - cur.y) / 2);
      const a = { x: cur.x + Math.sign(prev.x - cur.x) * r1, y: cur.y + Math.sign(prev.y - cur.y) * r1 };
      const b = { x: cur.x + Math.sign(next.x - cur.x) * r2, y: cur.y + Math.sign(next.y - cur.y) * r2 };
      d += ` L${a.x},${a.y} Q${cur.x},${cur.y} ${b.x},${b.y}`;
    }
    const last = pts[pts.length - 1];
    return d + ` L${last.x},${last.y}`;
  };

  const draw = () => {
    svg.querySelectorAll('path').forEach(p => p.remove());
    grid.querySelectorAll('.wf-label').forEach(el => el.remove());
    if (wrap.clientWidth < MIN_WIDTH) return;

    const origin = grid.getBoundingClientRect();
    const box = (id) => {
      const r = grid.querySelector(`[data-node="${id}"]`).getBoundingClientRect();
      return { l: r.left - origin.left, r: r.right - origin.left, t: r.top - origin.top, b: r.bottom - origin.top,
               cx: (r.left + r.right) / 2 - origin.left, cy: (r.top + r.bottom) / 2 - origin.top };
    };
    const items = edges.map(([from, to, label, dashed]) => {
      const s = box(from), t = box(to);
      const [sideS, sideT] = t.t >= s.b - 1 ? ['b', 't'] : t.l >= s.r - 1 ? ['r', 'l'] : ['l', 'r'];
      return { from, to, label, dashed, s, t, sideS, sideT };
    });

    // Several arrows on one side of a box are spread out, ordered by where they come from / go to.
    const slots = new Map();
    items.forEach(it => {
      [['s', it.from, it.sideS, it.t], ['t', it.to, it.sideT, it.s]].forEach(([end, id, side, other]) => {
        const key = id + '|' + side;
        if (!slots.has(key)) slots.set(key, []);
        slots.get(key).push({ it, end, side, other });
      });
    });
    const anchor = (b, side, f) => side === 'b' ? { x: b.l + (b.r - b.l) * f, y: b.b }
      : side === 't' ? { x: b.l + (b.r - b.l) * f, y: b.t }
      : side === 'r' ? { x: b.r, y: b.t + (b.b - b.t) * f } : { x: b.l, y: b.t + (b.b - b.t) * f };
    slots.forEach(list => {
      const vertical = list[0].side === 'b' || list[0].side === 't';
      list.sort((p, q) => vertical ? p.other.cx - q.other.cx : p.other.cy - q.other.cy);
      list.forEach((entry, i) => {
        const own = entry.end === 's' ? entry.it.s : entry.it.t;
        entry.it[entry.end + 'p'] = anchor(own, entry.side, (i + 1) / (list.length + 1));
      });
    });

    items.forEach(it => {
      const a = it.sp, b = it.tp;
      let pts;
      if (it.sideS === 'b') {
        const midY = Math.max(a.y + 10, b.y - BUS);
        pts = Math.abs(a.x - b.x) < 1 ? [a, b] : [a, { x: a.x, y: midY }, { x: b.x, y: midY }, b];
      } else {
        const midX = (a.x + b.x) / 2;
        pts = Math.abs(a.y - b.y) < 1 ? [a, b] : [a, { x: midX, y: a.y }, { x: midX, y: b.y }, b];
      }
      const path = document.createElementNS(NS, 'path');
      path.setAttribute('d', rounded(pts));
      path.setAttribute('marker-end', 'url(#wf-arrow)');
      if (it.dashed) path.setAttribute('class', 'wf-dashed');
      svg.appendChild(path);

      if (it.label) {
        const el = document.createElement('span');
        el.className = 'wf-label';
        el.textContent = it.label;
        const first = pts[1];
        el.style.left = (it.sideS === 'b' ? a.x : (a.x + first.x) / 2) + 'px';
        el.style.top = (it.sideS === 'b' ? a.y + Math.min(12, (first.y - a.y) / 2 + 2) : a.y) + 'px';
        grid.appendChild(el);
      }
    });
  };

  new ResizeObserver(draw).observe(wrap);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(draw);
  draw();
})();
"""
