"""Run every Python snippet in the how-to guides (and the notebooks) so they can't silently rot.

Each how-to snippet reads the reader's own CSV via pd.read_csv("my_data.csv"); here that call is
patched to return a small synthetic dataset with the column names the guide uses (whatever file
name the snippet asks for).

Skipped automatically when the scientific-Python stack (numpy, pandas, scipy, statsmodels,
scikit-learn, matplotlib, seaborn) isn't installed. Notebook execution additionally needs
nbclient + ipykernel.

Run one guide and see its printed output:
    python test_howto_snippets.py show check-multicollinearity
"""

import importlib.util
import json
import os
import pathlib
import re
import sys
import tempfile
import unittest
from unittest import mock

import build_explainers_html as builder

REQUIRED = ["numpy", "pandas", "scipy", "statsmodels", "sklearn", "matplotlib", "seaborn"]
MISSING = [name for name in REQUIRED if importlib.util.find_spec(name) is None]
CODE_BLOCK_RE = re.compile(r"```python\n(.*?)```", re.DOTALL)


def fixture_mia_models():
    import numpy as np
    import pandas as pd

    rng = np.random.default_rng(0)
    n = 300
    variant_a = rng.binomial(2, 0.3, n)                       # allele count, 0/1/2
    linked = rng.random(n) < 0.97                              # variant B is inherited with A almost always
    variant_b = np.where(linked, variant_a, rng.binomial(2, 0.3, n))
    age = rng.normal(45, 12, n)
    return pd.DataFrame({
        "variant_a": variant_a,
        "variant_b": variant_b,
        "age": age,
        "ldl_mmol": 3.2 + 0.45 * variant_a + 0.02 * age + rng.normal(0, 0.6, n),
    })


def fixture_theo_replicates():
    import numpy as np
    import pandas as pd

    rng = np.random.default_rng(0)
    n = 400
    true_bp = rng.normal(130, 12, n)
    return pd.DataFrame({
        "bp_1": true_bp + rng.normal(0, 8, n),
        "bp_2": true_bp + rng.normal(0, 8, n),
        "outcome": 0.5 * true_bp + rng.normal(0, 8, n),
    })


def fixture_tests():
    """One table with the columns used by the classical-test and test-as-regression guides."""
    import numpy as np
    import pandas as pd

    rng = np.random.default_rng(1)
    n = 240
    carrier = rng.random(n) < 0.5
    genotype = rng.choice(["ref/ref", "ref/alt", "alt/alt"], n)
    age = rng.normal(45, 12, n)
    ldl_mmol = (
        3.5 + 0.35 * carrier + 0.02 * (age - 45) + np.select([genotype == "ref/alt", genotype == "alt/alt"], [0.2, -0.2], 0)
        + rng.normal(0, 0.2, n) * np.where(carrier, 5, 3.5)
    )
    ldl_mmol[rng.random(n) < 0.05] = np.nan
    bp_before = rng.normal(140, 12, n)
    drug = rng.random(n) < 0.5
    return pd.DataFrame({
        "carrier_status": np.where(carrier, "carrier", "non-carrier"),
        "genotype": genotype,
        "age": age,
        "ldl_mmol": ldl_mmol,
        "bp_before": bp_before,
        "bp_after": bp_before - 8 + rng.normal(0, 8, n),
        "treatment": np.where(drug, "drug", "placebo"),
        "disease": np.where(rng.random(n) < np.where(drug, 0.22, 0.38), "yes", "no"),
    })


def fixture_eda():
    import numpy as np
    import pandas as pd

    rng = np.random.default_rng(2)
    n = 200
    df = pd.DataFrame({
        "clinic": rng.choice(["C1", "C2", "C3", "C4"], n),
        "carrier_status": rng.choice(["non-carrier", "carrier"], n),
        "age": rng.normal(45, 12, n),
        "sample_date": pd.Timestamp("2024-06-01") + pd.to_timedelta(rng.integers(0, 100, n), unit="D"),
        "ldl_mmol": rng.normal(3.8, 0.8, n),
    })
    df.loc[rng.random(n) < 0.1, "ldl_mmol"] = np.nan
    df.loc[3, "ldl_mmol"] = -2.0
    return df


def fixture_dag():
    import numpy as np
    import pandas as pd

    rng = np.random.default_rng(3)
    n = 500
    ancestry = rng.normal(0, 1, n)                                         # e.g. a genetic principal component
    carrier = (0.8 * ancestry + rng.normal(0, 1, n) > 0.7).astype(int)     # variant frequency differs by ancestry
    ldl_mmol = 3.5 + 0.5 * carrier + 0.6 * ancestry + rng.normal(0, 0.5, n)
    return pd.DataFrame({"ancestry": ancestry, "carrier": carrier, "ldl_mmol": ldl_mmol})


def fixture_clustered():
    import numpy as np
    import pandas as pd

    rng = np.random.default_rng(4)
    n_families, per_family = 15, 20
    family = np.repeat(np.arange(n_families), per_family)
    family_effect = rng.normal(0, 0.5, n_families)[family]
    carrier_families = rng.permutation(np.arange(n_families) % 2)          # variant segregates in whole families
    carrier = carrier_families[family]
    age = rng.normal(45, 12, n_families * per_family)
    return pd.DataFrame({
        "family": family,
        "carrier": carrier,
        "age": age,
        "ldl_mmol": 3.0 + 0.3 * carrier + 0.02 * age + family_effect
        + rng.normal(0, 0.5, n_families * per_family),
    })


def fixture_meta():
    import numpy as np
    import pandas as pd

    rng = np.random.default_rng(8)
    n_studies = 10
    se = np.round(rng.uniform(0.3, 1.0, n_studies), 2)
    true_effect = 1.5 + rng.normal(0, 0.8, n_studies)                # each study has its own true effect
    effect = np.round(true_effect + rng.normal(0, se), 2)
    scale = 0.2                                                      # express the effects in mmol/L of LDL
    return pd.DataFrame({
        "study": [f"Study {i + 1}" for i in range(n_studies)],
        "effect": np.round(effect * scale, 3),
        "se": np.round(se * scale, 3),
    })


FIXTURES = {
    "check-multicollinearity": fixture_mia_models,
    "validate-a-predictive-model": fixture_mia_models,
    "handle-measurement-error": fixture_theo_replicates,
    "plan-a-sample-size": fixture_mia_models,      # reads no data
    "explore-a-dataset": fixture_eda,
    "check-test-assumptions": fixture_tests,
    "run-a-common-test": fixture_tests,
    "run-a-test-as-a-regression": fixture_tests,
    "draw-and-use-a-causal-diagram": fixture_dag,
    "analyze-clustered-data": fixture_clustered,
    "run-a-meta-analysis": fixture_meta,
}

# Code that makes later snippets applicable to the synthetic data (e.g. a yes/no outcome).
BEFORE_BLOCK = {
    ("validate-a-predictive-model", 1): (
        "y_test = (y_test > y_train.median()).astype(int)\n"
        "y_train = (y_train > y_train.median()).astype(int)\n"
    ),
}


def howto_pages():
    return [
        (path, pathlib.PurePosixPath(path).stem)
        for path, _, _, _ in builder.STRUCTURE if builder.is_howto(path)
    ]


def run_howto(path: str, name: str) -> dict:
    """Execute every python block of a how-to guide in one shared namespace; return it."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import pandas as pd

    source = (builder.MARKDOWN_ROOT / path).read_text()
    blocks = CODE_BLOCK_RE.findall(source)
    if not blocks:
        raise AssertionError(f"{path} has no python code block")
    namespace: dict = {"__name__": "howto"}
    with mock.patch.object(pd, "read_csv", lambda *_a, **_k: FIXTURES[name]()), \
            mock.patch.object(plt, "show", lambda *_a, **_k: None):
        for index, block in enumerate(blocks):
            code = BEFORE_BLOCK.get((name, index), "") + block
            try:
                exec(compile(code, f"{name}[{index}]", "exec"), namespace)
            except Exception as exc:
                raise AssertionError(f"{name}: code block {index} failed: {exc!r}") from exc
            plt.close("all")
    return namespace


@unittest.skipIf(MISSING, f"missing packages: {MISSING}")
class HowToSnippetTests(unittest.TestCase):
    def test_every_howto_has_a_fixture_and_runs(self):
        for path, name in howto_pages():
            with self.subTest(howto=name):
                self.assertIn(name, FIXTURES, f"add a synthetic fixture for {name}")
                run_howto(path, name)

    def test_multicollinearity_snippet_flags_the_overlapping_pair(self):
        ns = run_howto("06-building-models/how-to/check-multicollinearity.md", "check-multicollinearity")
        self.assertGreater(ns["vif"]["variant_a"], 10)
        self.assertGreater(ns["vif"]["variant_b"], 10)
        self.assertLess(ns["vif"]["age"], 2)

    def test_measurement_error_snippet_recovers_the_true_slope(self):
        ns = run_howto("06-building-models/how-to/handle-measurement-error.md", "handle-measurement-error")
        self.assertLess(ns["naive"], 0.45)
        self.assertAlmostEqual(ns["corrected"], 0.5, delta=0.1)
        self.assertLess(ns["low"], 0.5)
        self.assertGreater(ns["high"], 0.5)

    def test_regression_forms_match_the_classical_tests(self):
        ns = run_howto("04-regression-basics/how-to/run-a-test-as-a-regression.md", "run-a-test-as-a-regression")
        self.assertAlmostEqual(ns["ols"].pvalues["carrier"], ns["stats"].ttest_ind(ns["a"], ns["b"]).pvalue, places=8)
        self.assertAlmostEqual(ns["slope"].pvalues["age"],
                               ns["stats"].pearsonr(ns["df"]["age"], ns["df"]["ldl_mmol"]).pvalue, places=8)
        classical_f = ns["stats"].f_oneway(*[g for _, g in ns["df"].groupby("genotype")["ldl_mmol"]]).statistic
        self.assertAlmostEqual(ns["anova_model"].fvalue, classical_f, places=8)

    def test_clustered_snippet_shows_overconfident_naive_intervals(self):
        ns = run_howto("07-special-data-structures/how-to/analyze-clustered-data.md", "analyze-clustered-data")
        naive_width = ns["naive"].conf_int().loc["carrier"].diff().iloc[-1]
        robust_width = ns["robust"].conf_int().loc["carrier"].diff().iloc[-1]
        self.assertGreater(robust_width, 1.5 * naive_width)

    def test_meta_analysis_snippet_pools_by_precision_and_reports_the_spread(self):
        ns = run_howto("07-special-data-structures/how-to/run-a-meta-analysis.md", "run-a-meta-analysis")
        df = ns["df"]
        weights = 1 / (df["se"] ** 2 + ns["tau2"])
        self.assertAlmostEqual(ns["pooled"], (weights * df["effect"]).sum() / weights.sum(), places=6)
        self.assertGreater(ns["tau2"], 0)
        self.assertGreater(ns["pooled_se"], ns["fixed_se"])           # random effects counts between-study spread
        self.assertGreater(ns["pi_half"], 1.96 * ns["pooled_se"])      # a new study varies more than the mean does
        self.assertGreaterEqual(ns["se_hksj"], ns["pooled_se"] * 0.99)
        self.assertEqual(len(ns["leave_one_out"]), len(df))

    def test_dag_snippet_classifies_roles(self):
        ns = run_howto("05-prediction-vs-causation/how-to/draw-and-use-a-causal-diagram.md", "draw-and-use-a-causal-diagram")
        self.assertEqual(ns["roles"]["ancestry"], "confounder")
        self.assertEqual(ns["roles"]["receptor_activity"], "mediator")
        self.assertEqual(ns["roles"]["clinic_referral"], "collider (consequence of both)")


@unittest.skipIf(MISSING, f"missing packages: {MISSING}")
class GuidePageSnippetTests(unittest.TestCase):
    """The setup and project-structure pages have Python snippets too; run them in an empty folder."""

    def run_blocks(self, rel_path: str, cwd: pathlib.Path) -> tuple[dict, list[str]]:
        blocks = CODE_BLOCK_RE.findall((builder.MARKDOWN_ROOT / rel_path).read_text())
        self.assertTrue(blocks, f"{rel_path} has no python code block")
        previous = os.getcwd()
        os.chdir(cwd)
        try:
            namespace: dict = {"__name__": "guide"}
            for index, block in enumerate(blocks):
                exec(compile(block, f"{rel_path}[{index}]", "exec"), namespace)
        finally:
            os.chdir(previous)
        return namespace, blocks

    def test_setup_check_snippet_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            namespace, _ = self.run_blocks("setup-environment.md", pathlib.Path(tmp))
        self.assertIn("numpy", namespace)

    def test_project_snippets_create_the_layout_and_find_the_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            namespace, blocks = self.run_blocks("project-structure.md", root)
            for folder in ["data/raw", "data/processed", "notebooks", "src", "results/figures", "results/tables", "docs"]:
                self.assertTrue((root / folder).is_dir(), folder)
            self.assertEqual(namespace["ROOT"], pathlib.Path(os.path.realpath(root)))

            # The same path snippet, run from inside notebooks/, must still find the project folder.
            previous = os.getcwd()
            os.chdir(root / "notebooks")
            try:
                inside: dict = {}
                exec(compile(blocks[-1], "project-structure[root]", "exec"), inside)
            finally:
                os.chdir(previous)
            self.assertEqual(inside["ROOT"], pathlib.Path(os.path.realpath(root)))


@unittest.skipIf(MISSING, f"missing packages: {MISSING}")
class NotebookTests(unittest.TestCase):
    def test_notebooks_are_valid_and_output_free(self):
        for path in builder.NOTEBOOKS_SRC.glob("*.ipynb"):
            with self.subTest(notebook=path.name):
                nb = json.loads(path.read_text())
                self.assertEqual(nb["nbformat"], 4)
                for cell in nb["cells"]:
                    if cell["cell_type"] == "code":
                        self.assertEqual(cell["outputs"], [])
                        self.assertIsNone(cell["execution_count"])

    @unittest.skipUnless(
        importlib.util.find_spec("nbclient") and importlib.util.find_spec("ipykernel"),
        "nbclient/ipykernel not installed",
    )
    def test_notebooks_execute(self):
        import nbformat
        from nbclient import NotebookClient

        for path in builder.NOTEBOOKS_SRC.glob("*.ipynb"):
            with self.subTest(notebook=path.name):
                nb = nbformat.read(str(path), as_version=4)
                NotebookClient(nb, timeout=600, kernel_name="python3",
                               resources={"metadata": {"path": str(path.parent)}}).execute()


@unittest.skipIf(MISSING, f"missing packages: {MISSING}")
class SkillMetaAnalysisTemplateTests(unittest.TestCase):
    """The skill's meta-analysis template is a script, not a course page; keep it from rotting here."""

    @classmethod
    def setUpClass(cls):
        path = pathlib.Path(__file__).resolve().parents[2] / "statistics-advisor" / "scripts" / "meta_analysis_template.py"
        spec = importlib.util.spec_from_file_location("meta_analysis_template", path)
        cls.template = importlib.util.module_from_spec(spec)
        previous, sys.dont_write_bytecode = sys.dont_write_bytecode, True   # keep __pycache__ out of the skill folder
        try:
            spec.loader.exec_module(cls.template)
        finally:
            sys.dont_write_bytecode = previous
        cls.data = cls.template.load_study_data()

    def test_pooling_is_the_precision_weighted_average_with_a_wider_prediction_interval(self):
        pooled = self.template.pool_random_effects(self.data)
        weights = 1 / (self.data["se"] ** 2 + pooled["tau2"])
        self.assertAlmostEqual(pooled["estimate"], (weights * self.data["effect"]).sum() / weights.sum(), places=8)
        self.assertAlmostEqual(pooled["estimate"], pooled["result"].mean_effect_re, places=6)
        low, high = pooled["prediction_interval"]
        self.assertLess(low, pooled["ci"][0])
        self.assertGreater(high, pooled["ci"][1])
        self.assertGreaterEqual(pooled["i2"], 0)
        self.assertIn("prediction interval", self.template.summarize(pooled))

    def test_hartung_knapp_is_never_narrower_and_two_studies_have_no_prediction_interval(self):
        usual = self.template.pool_random_effects(self.data)
        adjusted = self.template.pool_random_effects(self.data, hksj=True)
        self.assertGreaterEqual(adjusted["ci"][1] - adjusted["ci"][0], usual["ci"][1] - usual["ci"][0])
        self.assertIsNone(self.template.pool_random_effects(self.data.head(2))["prediction_interval"])
        with self.assertRaises(ValueError):
            self.template.pool_random_effects(self.data.head(1))

    def test_leave_one_out_bias_check_and_conversions(self):
        loo = self.template.leave_one_out(self.data)
        self.assertEqual(len(loo), len(self.data))
        self.assertEqual(self.template.egger_test(self.data.head(8))["low_power"], True)
        summaries = fixture_summaries()
        diff = self.template.effect_sizes_from_summaries(summaries, "mean_difference")
        self.assertAlmostEqual(diff["effect"][0], 2.1)
        for kind in ("smd", "log_odds_ratio", "log_risk_ratio"):
            converted = self.template.effect_sizes_from_summaries(summaries, kind)
            self.assertTrue((converted["se"] > 0).all(), kind)
        with self.assertRaises(ValueError):
            self.template.effect_sizes_from_summaries(summaries, "nonsense")


def fixture_summaries():
    import pandas as pd

    return pd.DataFrame({
        "mean_t": [24.1, 22.8, 25.0], "sd_t": [3.2, 2.9, 3.6], "n_t": [30, 45, 28],
        "mean_c": [22.0, 22.1, 22.7], "sd_c": [3.0, 3.1, 3.3], "n_c": [30, 44, 29],
        "events_t": [12, 9, 20], "events_c": [20, 15, 24],
    })


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "show":
        target = dict((name, path) for path, name in howto_pages())[sys.argv[2]]
        run_howto(target, sys.argv[2])
    else:
        unittest.main()
