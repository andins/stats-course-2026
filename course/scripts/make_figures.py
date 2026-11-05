"""
Regenerate the explanatory figures used in the course pages.

Writes PNG files to <lang>/markdown/figures/ (en/markdown/figures/, es/markdown/figures/, ...).
The figures are schematics and simulations that make a concept easier to grasp
(causal diagrams, what a p-value is, how cross-validation splits the data, ...). Data-driven
plots that students produce themselves live in the notebooks and are deliberately not
duplicated here.

Every figure uses a fixed random seed, so rerunning gives the same pictures. Run this
whenever you change a figure, then rebuild the HTML (build_explainers_html.py).

All visible text goes through _(); the Spanish strings live in figure_strings_es.py
(a dict English -> Spanish). A string missing from that dict raises a KeyError in "es" mode.

Usage:
    python3 make_figures.py                          # all figures, English
    python3 make_figures.py p_value                  # only the named figures
    python3 make_figures.py --lang es                # all figures in Spanish -> es/markdown/figures/
    python3 make_figures.py --lang es p_value        # one figure in Spanish
    COURSE_LANG=es python3 make_figures.py           # same as --lang es (the flag wins over the variable)

Requires: numpy, scipy, statsmodels, matplotlib (the course's scientific Python stack).
"""

from __future__ import annotations

import argparse
import os
import pathlib
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch, Polygon, Rectangle
from scipy import stats
from statsmodels.stats.meta_analysis import combine_effects
from statsmodels.tsa.stattools import acf

COURSE_DIR = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_LANG = "en"
LANG = DEFAULT_LANG


def out_dir(lang: str) -> pathlib.Path:
    return COURSE_DIR / lang / "markdown" / "figures"


def _load_strings(lang: str) -> dict[str, str]:
    if lang == DEFAULT_LANG:
        return {}
    if lang == "es":
        from figure_strings_es import STRINGS
        return STRINGS
    sys.exit(f"Unsupported language '{lang}'. Available: en, es")


STRINGS: dict[str, str] = {}


def set_lang(lang: str) -> None:
    global LANG, STRINGS
    STRINGS = _load_strings(lang)
    LANG = lang


def _(text: str) -> str:
    """Return `text` for English, its translation otherwise (KeyError if the translation is missing)."""
    if LANG == DEFAULT_LANG:
        return text
    try:
        return STRINGS[text]
    except KeyError:
        raise KeyError(f"No '{LANG}' translation in figure_strings_{LANG}.py for: {text!r}") from None


# One palette across all figures. The same colour always means the same role.
INK = "#1f2933"
MUTED = "#6b7280"
EXPOSURE = ("#dce6f7", "#3b6fc4")      # (fill, edge)
OUTCOME = ("#fce8c8", "#d98200")
ADJUST = ("#d6f0e3", "#1b8a5a")
CAUTION = ("#e6def5", "#6f4fb8")
NEVER = ("#f8dad6", "#c0392b")
NEUTRAL = ("#f3f4f6", "#6b7280")
LEARN = "#3b6fc4"      # data / the thing being illustrated
ALERT = "#c0392b"
GOOD = "#1b8a5a"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.edgecolor": MUTED,
    "axes.labelcolor": INK,
    "axes.titleweight": "bold",
    "axes.titlesize": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "text.color": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})


# ---------------------------------------------------------------- DAG helpers

class Dag:
    """A tiny causal-diagram drawer: boxes at fixed positions and arrows clipped to the boxes."""

    def __init__(self, ax, xlim, ylim):
        self.ax = ax
        self.nodes: dict[str, dict] = {}
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.axis("off")

    def node(self, key, xy, label, colors=NEUTRAL, sub=None, size=(2.7, 1.3), dashed=False, fontsize=10):
        x, y = xy
        w, h = size
        self.ax.add_patch(FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.25",
            facecolor=colors[0], edgecolor=colors[1], linewidth=2,
            linestyle=(0, (4, 2)) if dashed else "-", zorder=3,
        ))
        if sub:
            self.ax.text(x, y + h * 0.14, label, ha="center", va="center", fontsize=fontsize, fontweight="bold", zorder=4)
            self.ax.text(x, y - h * 0.24, sub, ha="center", va="center", fontsize=fontsize - 2.2, color=MUTED,
                         style="italic", zorder=4)
        else:
            self.ax.text(x, y, label, ha="center", va="center", fontsize=fontsize, fontweight="bold",
                         linespacing=1.15, zorder=4)
        self.nodes[key] = {"xy": np.array([x, y], float), "size": size}

    def _edge_point(self, key, toward, pad=0.12):
        node = self.nodes[key]
        centre, (w, h) = node["xy"], node["size"]
        d = toward - centre
        tx = (w / 2 + pad) / abs(d[0]) if d[0] else np.inf
        ty = (h / 2 + pad) / abs(d[1]) if d[1] else np.inf
        return centre + d * min(tx, ty)

    def arrow(self, src, dst, kind="cause", rad=0.0, label=None, label_offset=(0, 0)):
        a, b = self.nodes[src]["xy"], self.nodes[dst]["xy"]
        start, end = self._edge_point(src, b), self._edge_point(dst, a)
        style = {
            "cause": dict(color=INK, lw=1.8, ls="-"),
            "effect": dict(color=EXPOSURE[1], lw=3.6, ls="-"),
            "absent": dict(color=MUTED, lw=1.6, ls=(0, (3, 3))),
        }[kind]
        self.ax.add_patch(FancyArrowPatch(
            start, end, arrowstyle="-|>", mutation_scale=18, connectionstyle=f"arc3,rad={rad}",
            color=style["color"], linewidth=style["lw"], linestyle=style["ls"], zorder=2,
            shrinkA=0, shrinkB=0,
        ))
        if label:
            mid = (start + end) / 2 + np.array(label_offset)
            self.ax.text(*mid, label, ha="center", va="center", fontsize=9, color=style["color"],
                         fontweight="bold", zorder=5,
                         bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none"))

    def cross_out(self, src, dst, fraction=0.5):
        a, b = self.nodes[src]["xy"], self.nodes[dst]["xy"]
        p = self._edge_point(src, b) * (1 - fraction) + self._edge_point(dst, a) * fraction
        self.ax.text(*p, "\u2715", ha="center", va="center", fontsize=20, color=ALERT, fontweight="bold", zorder=6,
                     bbox=dict(boxstyle="circle,pad=0.05", facecolor="white", edgecolor="none"))


def role_legend(fig, entries, y=0.0, ncol=None):
    handles = [Patch(facecolor=fill, edgecolor=edge, linewidth=2, label=text) for text, (fill, edge) in entries]
    fig.legend(handles=handles, loc="lower center", ncol=ncol or len(handles), frameon=False,
               bbox_to_anchor=(0.5, y), fontsize=9.5, handlelength=1.6, columnspacing=1.8)


def panel_title(ax, text, y=1.0):
    ax.text(0.5, y, text, transform=ax.transAxes, ha="center", va="bottom", fontsize=13, fontweight="bold")


def panel_verdict(ax, text, color, y=0.0):
    ax.text(0.5, y, text, transform=ax.transAxes, ha="center", va="top", fontsize=10.5, fontweight="bold", color=color,
            linespacing=1.3)


# ------------------------------------------------------------------- figures

def causal_roles():
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.5))
    effect = dict(kind="effect")

    d = Dag(axes[0], (0, 10), (-0.5, 7.5))
    d.node("a", (5, 6.0), _("ancestry"), ADJUST)
    d.node("v", (1.9, 1.4), _("gene\nvariant"), EXPOSURE)
    d.node("l", (8.1, 1.4), "LDL", OUTCOME)
    d.arrow("a", "v"), d.arrow("a", "l"), d.arrow("v", "l", **effect)
    panel_title(axes[0], _("Confounder"))
    panel_verdict(axes[0], _("Adjust for it"), GOOD, y=0.06)

    d = Dag(axes[1], (0, 10), (-0.5, 7.5))
    d.node("v", (1.9, 1.4), _("gene\nvariant"), EXPOSURE)
    d.node("m", (5, 5.4), _("receptor\nactivity"), CAUTION)
    d.node("l", (8.1, 1.4), "LDL", OUTCOME)
    d.arrow("v", "m", **effect), d.arrow("m", "l", **effect)
    panel_title(axes[1], _("Mediator"))
    panel_verdict(axes[1], _("Don't adjust for it\n(you would explain away the effect)"), CAUTION[1], y=0.06)

    d = Dag(axes[2], (0, 10), (-0.5, 7.5))
    d.node("v", (1.9, 6.0), _("gene\nvariant"), EXPOSURE)
    d.node("l", (8.1, 6.0), "LDL", OUTCOME)
    d.node("c", (5, 1.4), _("clinic\nreferral"), NEVER)
    d.arrow("v", "c"), d.arrow("l", "c"), d.arrow("v", "l", kind="absent")
    panel_title(axes[2], _("Collider"))
    panel_verdict(axes[2], _("Never adjust for it\n(it can create a fake association)"), ALERT, y=0.06)

    role_legend(fig, [(_("exposure"), EXPOSURE), (_("outcome"), OUTCOME)], y=-0.01)
    fig.legend(handles=[Line2D([0], [0], color=EXPOSURE[1], lw=3.6, label=_("effect path we want to measure")),
                        Line2D([0], [0], color=INK, lw=1.8, label=_("other causal arrow")),
                        Line2D([0], [0], color=MUTED, lw=1.6, ls=(0, (3, 3)), label=_("possibly no effect at all"))],
               loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.065), fontsize=9.5)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.9, bottom=0.12, wspace=0.05)
    return fig


def causal_diagram_mia():
    fig, ax = plt.subplots(figsize=(11.5, 7.2))
    d = Dag(ax, (0, 16), (-0.8, 9.6))
    size = (3.3, 1.5)
    d.node("anc", (3.0, 8.4), "ancestry", ADJUST, sub=_("confounder"), size=size)
    d.node("link", (13.0, 8.4), "linked_variant", ADJUST, sub=_("unmeasured confounder"), size=(3.8, 1.5), dashed=True)
    d.node("car", (2.4, 4.6), "carrier", EXPOSURE, sub=_("exposure"), size=size)
    d.node("rec", (8, 2.9), "receptor_activity", CAUTION, sub=_("mediator"), size=(3.7, 1.5))
    d.node("ldl", (13.6, 4.6), "ldl_mmol", OUTCOME, sub=_("outcome"), size=size)
    d.node("clin", (8, -0.6), "clinic_referral", NEVER, sub=_("collider"), size=(3.5, 1.5))
    d.arrow("anc", "car"), d.arrow("anc", "ldl")
    d.arrow("link", "ldl"), d.arrow("link", "car")
    d.arrow("car", "rec", kind="effect"), d.arrow("rec", "ldl", kind="effect")
    d.arrow("car", "ldl", kind="effect")
    d.arrow("car", "clin"), d.arrow("ldl", "clin")

    ax.text(8, -2.6, _("Adjust for: ancestry     Leave out: receptor_activity, clinic_referral\n"
                       "Cannot adjust for: linked_variant (state it as an assumption)"),
            ha="center", va="top", fontsize=10.5, linespacing=1.5,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#f9fafb", edgecolor=NEUTRAL[1]))
    ax.set_ylim(-4.6, 9.6)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    return fig


def randomized_vs_observational():
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))

    d = Dag(axes[0], (0, 12), (-0.5, 7.5))
    d.node("c", (6, 6.1), _("ancestry, diet, ..."), ADJUST, sub=_("other causes of LDL"), size=(4.4, 1.5))
    d.node("v", (2.2, 1.3), _("gene variant"), EXPOSURE, size=(3.6, 1.3))
    d.node("l", (9.8, 1.3), "LDL", OUTCOME, size=(3.0, 1.3))
    d.arrow("c", "v"), d.arrow("c", "l"), d.arrow("v", "l", kind="effect")
    panel_title(axes[0], _("Observational data"))
    panel_verdict(axes[0], _("Exposure arrives bundled with its confounders:\nyou must adjust for them (and hope you got them all)"),
                  INK, y=0.04)

    d = Dag(axes[1], (0, 12), (-0.5, 7.5))
    d.node("c", (8.1, 6.1), _("age, diet, baseline health"), ADJUST, sub=_("other causes of blood pressure"), size=(5.4, 1.5))
    d.node("x", (2.4, 1.3), _("drug or placebo"), EXPOSURE, size=(3.8, 1.3))
    d.node("l", (9.8, 1.3), _("blood pressure"), OUTCOME, size=(3.8, 1.3))
    d.node("coin", (1.2, 6.1), _("coin flip"), NEUTRAL, size=(2.2, 1.2), fontsize=10)
    d.arrow("c", "x", kind="absent"), d.arrow("c", "l"), d.arrow("x", "l", kind="effect"), d.arrow("coin", "x")
    d.cross_out("c", "x", 0.45)
    panel_title(axes[1], _("Randomized experiment"))
    panel_verdict(axes[1], _("Only the coin flip decides the exposure, so the other\ncauses cannot differ systematically between groups"),
                  INK, y=0.04)

    fig.subplots_adjust(left=0.01, right=0.99, top=0.9, bottom=0.12, wspace=0.04)
    return fig


def p_value():
    sd, observed = 2.3, -5.0     # SE of the difference in mean systolic BP (mmHg); Theo's observed difference
    p = 2 * stats.norm.sf(abs(observed) / sd)
    x = np.linspace(-9.5, 9.5, 600)
    y = stats.norm.pdf(x, 0, sd)
    fig, ax = plt.subplots(figsize=(9, 4.4))
    ax.plot(x, y, color=INK, lw=2)
    for side in (x <= observed, x >= -observed):
        ax.fill_between(x[side], y[side], color=ALERT, alpha=0.45, linewidth=0)
    ax.axvline(observed, color=ALERT, lw=2)
    ax.axvline(-observed, color=ALERT, lw=1.5, ls="--")
    ax.set_xlim(-9.5, 9.5)
    ax.set_ylim(0, y.max() * 1.35)
    ax.set_yticks([])
    ax.set_xlabel(_("Difference in mean blood pressure, drug minus placebo (mmHg)"))
    ax.spines["left"].set_visible(False)
    ax.set_title(_("What if the drug did nothing? How surprising would Theo's result be?"), loc="left", pad=12)
    ax.text(0, y.max() * 1.1, _("If the drug does nothing, differences scatter around 0\njust from random sampling"),
            ha="center", va="bottom", fontsize=10)
    ax.annotate(_("Theo's observed\ndifference: \u22125 mmHg"), xy=(observed, y.max() * 0.45), xytext=(-9.2, y.max() * 0.85),
                fontsize=10, color=ALERT, fontweight="bold", va="center",
                arrowprops=dict(arrowstyle="-|>", color=ALERT, lw=1.6))
    ax.annotate(_("equally extreme\nin the other direction"), xy=(-observed, y.max() * 0.25), xytext=(7.5, y.max() * 0.85),
                fontsize=10, color=ALERT, va="center", ha="center",
                arrowprops=dict(arrowstyle="-|>", color=ALERT, lw=1.2, ls="--"))
    ax.text(0, -y.max() * 0.3,
            _("p = {p:.2f}: the shaded area. If the drug did nothing, a difference at least this large\n"
              "(in either direction) would show up in about {pct:.0f}% of repeated experiments.").format(p=p, pct=p * 100),
            ha="center", va="top", fontsize=10.5, transform=ax.transData, clip_on=False)
    fig.subplots_adjust(left=0.04, right=0.97, top=0.88, bottom=0.3)
    return fig


def cross_validation():
    fig, ax = plt.subplots(figsize=(11, 6.2))
    ax.set_xlim(0, 22)
    ax.set_ylim(-9.3, 3.5)
    ax.axis("off")
    train, test = (LEARN, "#dce6f7"), (OUTCOME[1], OUTCOME[0])

    def block(x, y, w, face, edge, text, fs=10):
        ax.add_patch(Rectangle((x, y), w, 0.9, facecolor=face, edgecolor=edge, linewidth=1.6))
        ax.text(x + w / 2, y + 0.45, text, ha="center", va="center", fontsize=fs, color=INK)

    ax.text(0, 3.0, _("Train/test split"), fontsize=12, fontweight="bold", va="center")
    block(0, 1.6, 15, train[1], train[0], _("train: the model is built here"))
    block(15, 1.6, 5, test[1], test[0], _("test: held back"))
    ax.text(20.4, 2.05, _("\u2192  score once"), fontsize=10, va="center")

    ax.text(0, -0.4, _("5-fold cross-validation"), fontsize=12, fontweight="bold", va="center")
    for i in range(5):
        y = -1.9 - i * 1.4
        for j in range(5):
            held_out = i == j
            block(j * 4, y, 4, test[1] if held_out else train[1], test[0] if held_out else train[0],
                  _("held out") if held_out else _("train"), fs=9)
        ax.text(20.4, y + 0.45, _("\u2192  score {n}").format(n=i + 1), fontsize=10, va="center")
    ax.text(10, -8.6, _("every observation is held out exactly once"), ha="center", va="center", fontsize=10, color=MUTED,
            style="italic")
    ax.text(20.4, -8.6, _("\u2192  average the 5 scores"), fontsize=10, va="center", fontweight="bold")
    ax.legend(handles=[Patch(facecolor=train[1], edgecolor=train[0], label=_("used to fit the model")),
                       Patch(facecolor=test[1], edgecolor=test[0], label=_("used only to check it (the model has never seen it)"))],
              loc="upper right", bbox_to_anchor=(1.0, 1.02), frameon=False, fontsize=9.5)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.01)
    return fig


# Ten made-up studies of an LDLR variant (extra LDL in carriers, mmol/L), matching the worked
# example in the meta-analysis how-to: pooled 0.34, tau 0.13, prediction interval 0.01 to 0.67.
META_EFFECT = np.array([0.29, 0.22, 0.09, 0.09, 0.63, 0.28, 0.39, 0.45, 0.52, 0.20])
META_SE = np.array([0.19, 0.18, 0.17, 0.14, 0.13, 0.12, 0.09, 0.07, 0.07, 0.06])


def forest_plot():
    k = len(META_EFFECT)
    res = combine_effects(META_EFFECT, META_SE ** 2, method_re="iterated")
    pooled, pooled_se, tau2 = res.mean_effect_re, res.sd_eff_w_re, res.tau2
    pi_half = stats.t.ppf(0.975, k - 2) * np.sqrt(tau2 + pooled_se ** 2)
    weights = 1 / (META_SE ** 2 + tau2)
    sizes = 60 + 420 * weights / weights.max()

    fig = plt.figure(figsize=(12, 6.2))
    ax = fig.add_axes([0.14, 0.12, 0.45, 0.8])
    rows = np.arange(k, 0, -1) + 2
    for r, e, s, size in zip(rows, META_EFFECT, META_SE, sizes):
        ax.plot([e - 1.96 * s, e + 1.96 * s], [r, r], color=INK, lw=1.8, solid_capstyle="butt")
        ax.scatter([e], [r], marker="s", s=size, color=LEARN, zorder=3)
    ax.plot([0, 0], [-0.7, k + 2.1], color=MUTED, lw=1.2, ls="--")
    ax.plot([pooled, pooled], [-0.7, k + 2.1], color=GOOD, lw=1, ls=":")
    half = 1.96 * pooled_se
    ax.add_patch(Polygon([[pooled - half, 1.4], [pooled, 1.9], [pooled + half, 1.4], [pooled, 0.9]], closed=True,
                         facecolor=GOOD, edgecolor=GOOD, zorder=3))
    ax.plot([pooled - pi_half, pooled + pi_half], [0.1, 0.1], color=GOOD, lw=3, solid_capstyle="butt")
    for edge in (pooled - pi_half, pooled + pi_half):
        ax.plot([edge, edge], [-0.1, 0.3], color=GOOD, lw=3)
    ax.set_xlim(-0.55, 1.05)
    ax.set_ylim(-0.7, k + 3.0)
    ax.set_yticks(list(rows) + [1.4, 0.1])
    ax.set_yticklabels([_("Study {n}").format(n=i + 1) for i in range(k)]
                       + [_("Pooled (random effects)"), _("Prediction interval")])
    ax.set_xlabel(_("Extra LDL cholesterol in carriers (mmol/L)"))
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.text(0.0, k + 2.45, _("no effect"), ha="center", fontsize=9, color=MUTED)
    ax.set_title(_("Forest plot of ten (made-up) studies"), loc="left", pad=14)

    def callout(text, xy, y_text):
        ax.annotate(_(text), xy=xy, xytext=(1.14, y_text), xycoords="data", textcoords="data", fontsize=10,
                    va="center", ha="left", annotation_clip=False,
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.3, shrinkA=4, shrinkB=3))

    heaviest = int(np.argmax(weights))
    callout("Line: the study's 95% confidence interval.\nA wide line means an imprecise study",
            (META_EFFECT[0] + 1.96 * META_SE[0], rows[0]), rows[0])
    callout("Square: the study's estimate. Bigger square =\nmore weight, so precise studies count more",
            (META_EFFECT[heaviest] + 0.045, rows[heaviest]), rows[heaviest] + 1.6)
    callout("Diamond: the pooled average effect\nand its 95% confidence interval", (pooled + half, 1.4), 2.1)
    callout("Bar: 95% prediction interval, where a new study's\ntrue effect would likely fall. The honest summary\nof how much the studies disagree",
            (pooled + pi_half, 0.1), -0.1)
    fig.text(0.14, 0.015, _("Pooled {pooled:.2f} mmol/L (95% CI {ci_lo:.2f} to {ci_hi:.2f}); "
                            "prediction interval {pi_lo:.2f} to {pi_hi:.2f}.").format(
                 pooled=pooled, ci_lo=pooled - half, ci_hi=pooled + half, pi_lo=pooled - pi_half, pi_hi=pooled + pi_half),
             fontsize=10, color=MUTED)
    return fig


def overfitting():
    def truth(x):
        return np.sin(1.6 * x) + 0.3 * x

    def sample(rng, n):
        x = np.sort(rng.uniform(0, 3, n))
        return x, truth(x) + rng.normal(0, 0.35, n)

    def fit(x, y, degree):
        return np.polynomial.Polynomial.fit(x, y, degree)

    rng = np.random.default_rng(2)
    x_train, y_train = sample(rng, 14)
    x_test, y_test = sample(rng, 14)
    grid = np.linspace(0, 3, 300)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6), gridspec_kw={"width_ratios": [1.15, 1]})
    ax1.plot(grid, truth(grid), color=MUTED, lw=1.5, ls="--", label=_("true pattern"))
    ax1.plot(grid, fit(x_train, y_train, 3)(grid), color=GOOD, lw=2.4, label=_("simple model (cubic)"))
    ax1.plot(grid, fit(x_train, y_train, 12)(grid), color=ALERT, lw=2.4, label=_("flexible model (degree 12)"))
    ax1.scatter(x_train, y_train, color=LEARN, s=45, zorder=3, label=_("training data (model sees these)"))
    ax1.scatter(x_test, y_test, facecolor="white", edgecolor=OUTCOME[1], linewidth=1.8, s=55, zorder=3,
                label=_("new data (model has not seen these)"))
    ax1.set_ylim(-1.6, 2.4)
    ax1.set_xlabel(_("predictor"))
    ax1.set_ylabel(_("outcome"))
    ax1.set_title(_("Fitting the training data perfectly is not the goal"), loc="left")
    ax1.legend(loc="upper left", bbox_to_anchor=(0.0, -0.17), ncol=2, fontsize=8.5, frameon=False)

    degrees = np.arange(1, 13)
    train_err, test_err = [], []
    sim = np.random.default_rng(7)
    for _rep in range(300):
        xs, ys = sample(sim, 20)
        xt, yt = sample(sim, 200)
        row_train, row_test = [], []
        for degree in degrees:
            model = fit(xs, ys, degree)
            row_train.append(np.sqrt(np.mean((model(xs) - ys) ** 2)))
            row_test.append(np.sqrt(np.mean((model(xt) - yt) ** 2)))
        train_err.append(row_train)
        test_err.append(row_test)
    train_med, test_med = np.median(train_err, axis=0), np.median(test_err, axis=0)
    ax2.plot(degrees, train_med, color=LEARN, lw=2.4, marker="o", label=_("error on training data"))
    ax2.plot(degrees, test_med, color=OUTCOME[1], lw=2.4, marker="o", label=_("error on new data"))
    best = degrees[np.argmin(test_med)]
    ax2.axvline(best, color=MUTED, ls=":", lw=1.3)
    ax2.set_ylim(0, 2.0)
    ax2.text(best + 0.2, 1.95, _("best on\nnew data"), fontsize=9, color=MUTED, va="top")
    ax2.set_xlabel(_("model flexibility (polynomial degree)"))
    ax2.set_ylabel(_("typical prediction error"))
    ax2.set_title(_("More flexibility: training error keeps falling,\nerror on new data turns upward"), loc="left")
    ax2.legend(loc="upper left", fontsize=9, frameon=False, bbox_to_anchor=(0.0, 0.8))
    fig.subplots_adjust(left=0.06, right=0.98, top=0.86, bottom=0.26, wspace=0.22)
    return fig


def glm_logistic():
    import statsmodels.api as sm

    rng = np.random.default_rng(11)
    ldl = rng.uniform(1.8, 7.8, 160)
    p_true = 1 / (1 + np.exp(-1.7 * (ldl - 5.2)))
    event = rng.binomial(1, p_true)
    grid = np.linspace(1.5, 8.2, 300)
    design = sm.add_constant(ldl)
    line = sm.OLS(event, design).fit()
    logit = sm.Logit(event, design).fit(disp=0)

    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.axhspan(1, 1.35, color=NEVER[0], alpha=0.7, linewidth=0)
    ax.axhspan(-0.35, 0, color=NEVER[0], alpha=0.7, linewidth=0)
    ax.text(1.65, 1.17, _("impossible: probability above 100%"), fontsize=9, color=ALERT, va="center")
    ax.text(1.65, -0.17, _("impossible: probability below 0%"), fontsize=9, color=ALERT, va="center")
    ax.scatter(ldl, event + rng.uniform(-0.03, 0.03, ldl.size), color=LEARN, alpha=0.45, s=28, linewidth=0, zorder=3)
    ax.plot(grid, line.params[0] + line.params[1] * grid, color=ALERT, lw=2.4, label=_("straight line (ordinary regression)"))
    ax.plot(grid, logit.predict(sm.add_constant(grid)), color=GOOD, lw=2.8, label=_("logistic curve (GLM)"))
    ax.set_xlim(1.5, 8.2)
    ax.set_ylim(-0.35, 1.35)
    ax.set_yticks([0, 0.5, 1])
    ax.set_yticklabels([_("0\n(no event)"), "0.5", _("1\n(event)")])
    ax.set_xlabel(_("LDL cholesterol (mmol/L)"))
    ax.set_ylabel(_("coronary event before age 60"))
    ax.set_title(_("A yes/no outcome: the line leaves the possible range, the curve cannot"), loc="left")
    ax.legend(loc="center left", bbox_to_anchor=(0.0, 0.55), frameon=False, fontsize=10)
    fig.subplots_adjust(left=0.13, right=0.98, top=0.9, bottom=0.13)
    return fig


def regression_anatomy():
    rng = np.random.default_rng(5)
    age = rng.uniform(25, 80, 70)
    ldl = 2.4 + 0.02 * age + rng.normal(0, 0.45, age.size)
    slope, intercept = np.polyfit(age, ldl, 1)
    fig, ax = plt.subplots(figsize=(9, 5))
    grid = np.array([0, 85])
    ax.scatter(age, ldl, color=LEARN, alpha=0.7, s=36, linewidth=0, zorder=3)
    ax.plot(grid, intercept + slope * grid, color=ALERT, lw=2.4, zorder=2)
    ax.plot([0, 25], intercept + slope * np.array([0, 25]), color=ALERT, lw=2.4, ls=":", zorder=2)
    ax.scatter([0], [intercept], color=ALERT, s=60, zorder=4)
    ax.annotate(_("Intercept ({intercept:.1f}): where the line crosses age 0.\nOften just an anchor, not a real person").format(
                    intercept=intercept),
                xy=(0, intercept), xytext=(4, 1.6), fontsize=10, va="center",
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
    x0, x1 = 50, 70
    y0, y1 = intercept + slope * x0, intercept + slope * x1
    ax.plot([x0, x1, x1], [y0, y0, y1], color=INK, lw=1.8, zorder=4)
    ax.text((x0 + x1) / 2, y0 - 0.1, _("20 years older"), ha="center", va="top", fontsize=10,
            bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none"))
    ax.annotate(_("Slope ({slope:.2f} per year): a patient 20 years older\nhas on average {gain:.1f} mmol/L more LDL").format(
                    slope=slope, gain=slope * 20),
                xy=(x1, (y0 + y1) / 2), xytext=(46, 1.55), fontsize=10, va="center",
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
    i = int(np.argmax(np.abs(ldl - (intercept + slope * age)) * (age > 30) * (age < 48)))
    fitted = intercept + slope * age[i]
    ax.plot([age[i], age[i]], [fitted, ldl[i]], color=GOOD, lw=3, zorder=4)
    ax.scatter([age[i]], [ldl[i]], color=LEARN, edgecolor=INK, s=70, zorder=5)
    ax.annotate(_("Residual: gap between the observed\npatient and the line's prediction"), xy=(age[i], (fitted + ldl[i]) / 2),
                xytext=(5, 5.55), fontsize=10, color=GOOD, fontweight="bold", va="center",
                arrowprops=dict(arrowstyle="-|>", color=GOOD, lw=1.2))
    ax.set_xlim(0, 85)
    ax.set_ylim(1.0, 6.0)
    ax.set_xlabel(_("age (years)"))
    ax.set_ylabel(_("LDL cholesterol (mmol/L)"))
    ax.set_title(_("A regression line, taken apart (70 simulated patients)"), loc="left")
    fig.subplots_adjust(left=0.09, right=0.97, top=0.92, bottom=0.12)
    return fig


def funnel_plots():
    rng = np.random.default_rng(3)
    true_effect = 0.3
    se = rng.uniform(0.04, 0.38, 70)
    effect = rng.normal(true_effect, se)
    z = effect / se
    published = ~((se > 0.12) & (z < 1.96) & (rng.random(se.size) < 0.9))     # small null studies go missing

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.2), sharex=True, sharey=True)
    for ax, keep, title in zip(axes, (np.ones(se.size, bool), published),
                               (_("No publication bias"), _("Publication bias"))):
        weights = 1 / se[keep] ** 2
        centre = np.sum(weights * effect[keep]) / weights.sum()
        s = np.linspace(0, 0.4, 50)
        ax.fill_betweenx(s, centre - 1.96 * s, centre + 1.96 * s, color="#eef1f5", zorder=0)
        ax.plot(centre - 1.96 * s, s, color=MUTED, lw=1, ls="--")
        ax.plot(centre + 1.96 * s, s, color=MUTED, lw=1, ls="--")
        ax.axvline(centre, color=MUTED, lw=1.2)
        ax.scatter(effect[keep], se[keep], color=LEARN, s=34, alpha=0.8, linewidth=0, zorder=3)
        ax.set_title(title, loc="left")
        ax.set_xlabel(_("effect estimate"))
    axes[0].set_ylabel(_("standard error (small = precise study)"))
    axes[0].set_ylim(0.42, 0)
    axes[0].set_xlim(-0.55, 1.05)
    axes[0].text(0.5, -0.22, _("Symmetric funnel: precise studies cluster at the top,\nimprecise ones scatter evenly on both sides"),
                 transform=axes[0].transAxes, fontsize=10, color=MUTED, va="top", ha="center")
    lo, hi = 0.12, 0.4     # the studies that never appeared: small and not significantly positive (effect < 1.96 * se)
    axes[1].add_patch(Polygon([[true_effect - 1.96 * lo, lo], [1.96 * lo, lo], [1.96 * hi, hi], [true_effect - 1.96 * hi, hi]],
                              closed=True, facecolor=NEVER[0], edgecolor=ALERT, linestyle=(0, (4, 3)), linewidth=1.6, alpha=0.7,
                              zorder=1))
    axes[1].text(0.0, 0.385, _("missing: small studies with\nnull or negative results"), fontsize=9.5, color=ALERT,
                 va="bottom", ha="center", fontweight="bold")
    axes[1].text(0.5, -0.22, _("Lopsided funnel: a corner is empty,\nso the pooled estimate is pushed up"),
                 transform=axes[1].transAxes, fontsize=10, color=MUTED, va="top", ha="center")
    fig.subplots_adjust(left=0.08, right=0.98, top=0.9, bottom=0.22, wspace=0.06)
    return fig


def missing_data_mechanisms():
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.8))
    spec = [
        ("MCAR", _("Missing completely at random"), _("Gaps ignore your data entirely.\nDropping rows loses precision, not accuracy."),
         GOOD, None),
        ("MAR", _("Missing at random"), _("Gaps depend on something you measured.\nDropping rows can bias the result."),
         CAUTION[1], ("age", "miss")),
        ("MNAR", _("Missing not at random"), _("Gaps depend on the missing value itself.\nDropping rows biases the result."),
         ALERT, ("ldl", "miss")),
    ]
    for ax, (code, name, verdict, colour, extra) in zip(axes, spec):
        d = Dag(ax, (0, 10), (-0.5, 7.5))
        d.node("age", (1.9, 5.6), _("age"), ADJUST, size=(2.4, 1.2))
        d.node("ldl", (8.1, 5.6), _("LDL\n(true value)"), OUTCOME, size=(3.2, 1.5))
        d.node("miss", (5, 1.2), _("LDL missing?"), NEUTRAL, size=(3.6, 1.2))
        d.arrow("age", "ldl")
        if code == "MCAR":
            d.node("chance", (9, 1.2), _("chance"), NEUTRAL, size=(2.0, 1.0), dashed=True, fontsize=9)
            d.arrow("chance", "miss", kind="absent")
        else:
            d.arrow(*extra)
        panel_title(ax, code)
        ax.text(0.5, 0.995, name, transform=ax.transAxes, ha="center", va="top", fontsize=9.5, color=MUTED)
        panel_verdict(ax, verdict, colour, y=0.0)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.88, bottom=0.14, wspace=0.05)
    return fig


def time_series_autocorrelation():
    n = 120
    rng = np.random.default_rng(4)
    independent = rng.normal(0, 1, n)
    correlated = np.zeros(n)
    noise = rng.normal(0, 1, n)
    for t in range(1, n):
        correlated[t] = 0.85 * correlated[t - 1] + noise[t] * 0.6

    fig, axes = plt.subplots(2, 2, figsize=(11.5, 6.4), gridspec_kw={"height_ratios": [1, 0.9]})
    band = 1.96 / np.sqrt(n)
    for col, (series, title, colour) in enumerate(
            ((independent, _("Residuals with no time pattern"), GOOD),
             (correlated, _("Residuals that remember yesterday"), ALERT))):
        ax = axes[0, col]
        ax.plot(series, color=colour, lw=1.6)
        ax.axhline(0, color=MUTED, lw=1)
        ax.set_ylim(-3.2, 3.2)
        ax.set_xlabel(_("time"))
        ax.set_title(title, loc="left")
        if col == 0:
            ax.set_ylabel(_("residual"))
        ax = axes[1, col]
        values = acf(series, nlags=20)
        ax.bar(np.arange(1, 21), values[1:], color=colour, width=0.6)
        ax.axhspan(-band, band, color="#dde3ea", zorder=0)
        ax.axhline(0, color=MUTED, lw=1)
        ax.set_ylim(-0.4, 1.0)
        ax.set_xticks([1, 5, 10, 15, 20])
        ax.set_xlabel(_("lag (steps back in time)"))
        if col == 0:
            ax.set_ylabel(_("autocorrelation"))
        ax.text(0.98, 0.95, _("grey band: what chance alone produces") if col == 0 else _("bars far outside the band: not chance"),
                transform=ax.transAxes, ha="right", va="top", fontsize=9.5, color=MUTED)
    fig.subplots_adjust(left=0.07, right=0.98, top=0.94, bottom=0.09, hspace=0.42, wspace=0.12)
    return fig


def clustered_families():
    rng = np.random.default_rng(8)
    n_fam, per = 15, 20
    family_means = 3.4 + rng.normal(0, 0.6, n_fam)
    values = family_means[:, None] + rng.normal(0, 0.5, (n_fam, per))
    order = np.argsort(family_means)
    overall = values.mean()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8), gridspec_kw={"width_ratios": [0.7, 3]}, sharey=True)
    ax1.scatter(rng.uniform(-0.3, 0.3, values.size), values.ravel(), color=LEARN, alpha=0.45, s=18, linewidth=0)
    ax1.axhline(overall, color=INK, lw=1.4)
    ax1.set_xlim(-0.8, 0.8)
    ax1.set_xticks([])
    ax1.set_ylabel(_("LDL cholesterol (mmol/L)"))
    ax1.set_title(_("What the test assumes:\n300 independent patients"), loc="left", fontsize=10.5)

    for rank, f in enumerate(order):
        ax2.scatter(rank + rng.uniform(-0.28, 0.28, per), values[f], color=LEARN, alpha=0.5, s=18, linewidth=0)
        ax2.scatter([rank], [values[f].mean()], marker="D", color=OUTCOME[1], edgecolor=INK, s=50, zorder=4)
    ax2.axhline(overall, color=INK, lw=1.4)
    ax2.set_xticks(range(n_fam))
    ax2.set_xticklabels([str(i + 1) for i in range(n_fam)])
    ax2.set_xlabel(_("family (sorted by its average)"))
    ax2.set_title(_("What the data look like: 15 families of 20 relatives,\nwho resemble each other more than they resemble other families"),
                  loc="left", fontsize=10.5)
    ax2.legend(handles=[Line2D([0], [0], marker="D", color="none", markerfacecolor=OUTCOME[1], markeredgecolor=INK,
                               markersize=8, label=_("family average")),
                        Line2D([0], [0], color=INK, lw=1.4, label=_("overall average"))],
               loc="upper left", frameon=False, fontsize=9.5)
    fig.subplots_adjust(left=0.07, right=0.99, top=0.82, bottom=0.14, wspace=0.05)
    return fig


def partial_pooling():
    sizes = np.array([3, 5, 8, 12, 20, 35, 60, 100])
    raw = np.array([4.9, 2.3, 4.5, 3.1, 3.9, 3.2, 3.7, 3.55])     # each group's own average (made up)
    tau, sigma = 0.4, 1.2        # spread between groups, spread between patients within a group
    se = sigma / np.sqrt(sizes)
    weight = tau ** 2 / (tau ** 2 + se ** 2)
    pooled_est = np.sum(raw * sizes) / sizes.sum()
    partial = pooled_est + weight * (raw - pooled_est)

    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    rows = np.arange(len(sizes))[::-1]
    ax.errorbar(raw, rows, xerr=se, fmt="none", ecolor=ALERT, elinewidth=1.2, alpha=0.5, capsize=3, zorder=2)
    for r, a, b in zip(rows, raw, partial):
        ax.annotate("", xy=(b, r), xytext=(a, r), arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.4, shrinkA=6, shrinkB=6))
    ax.scatter(raw, rows, facecolor="white", edgecolor=ALERT, linewidth=2, s=70, zorder=3,
               label=_("no pooling: each group's own average (bar = \u00b11 standard error)"))
    ax.scatter(partial, rows, color=GOOD, s=70, zorder=3, label=_("partial pooling: pulled toward the overall average"))
    ax.axvline(pooled_est, color=INK, lw=1.4, label=_("complete pooling: one average for everyone"))
    ax.set_yticks(rows)
    ax.set_yticklabels([_("{n} patients").format(n=n) for n in sizes])
    ax.set_xlabel(_("estimated average LDL cholesterol (mmol/L)"))
    ax.set_title(_("Small, noisy groups are pulled toward the overall average the most"), loc="left")
    ax.legend(loc="upper center", bbox_to_anchor=(0.45, -0.14), ncol=1, frameon=False, fontsize=9.5)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    fig.subplots_adjust(left=0.14, right=0.98, top=0.92, bottom=0.3)
    return fig


FIGURES = {
    "causal_roles": causal_roles,
    "causal_diagram_mia": causal_diagram_mia,
    "randomized_vs_observational": randomized_vs_observational,
    "p_value": p_value,
    "cross_validation": cross_validation,
    "forest_plot": forest_plot,
    "overfitting": overfitting,
    "glm_logistic": glm_logistic,
    "regression_anatomy": regression_anatomy,
    "funnel_plots": funnel_plots,
    "missing_data_mechanisms": missing_data_mechanisms,
    "time_series_autocorrelation": time_series_autocorrelation,
    "clustered_families": clustered_families,
    "partial_pooling": partial_pooling,
}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Regenerate the explainer figures.")
    parser.add_argument("--lang", default=None,
                        help="language of the figure text: en or es (default: $COURSE_LANG, else en)")
    parser.add_argument("names", nargs="*", metavar="figure", help="figure names (default: all)")
    args = parser.parse_args(argv)

    names = args.names
    unknown = [n for n in names if n not in FIGURES]
    if unknown:
        sys.exit(f"Unknown figure(s): {', '.join(unknown)}. Available: {', '.join(FIGURES)}")
    set_lang(args.lang or os.environ.get("COURSE_LANG") or DEFAULT_LANG)
    target = out_dir(LANG)
    target.mkdir(parents=True, exist_ok=True)
    for name in names or FIGURES:
        fig = FIGURES[name]()
        fig.savefig(target / f"{name}.png", dpi=200, bbox_inches="tight", pad_inches=0.15, metadata={"Software": None})
        plt.close(fig)
        print(f"wrote {target / f'{name}.png'}")


if __name__ == "__main__":
    main()
