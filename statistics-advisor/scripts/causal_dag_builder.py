"""
Template: elicit, store, visualize, and sanity-check an approximate causal DAG.

Use this after references/analysis-triage.md (Question 2) concludes the
analysis goal is causal interpretation, not pure prediction -- and, per
Question 2a, the exposure was NOT assigned by a well-designed experiment (if
it was, a full confounding-oriented DAG isn't required; this is still usable
to pick optional pre-treatment precision covariates). Workflow:

1. Call `create_schema_template()` with the recorded column names from the
   user's dataset to generate a prefilled, editable schema (saved as JSON) --
   one node per column already in hand, so nothing is silently forgotten.
2. Walk the user through the elicitation questions in
   references/analysis-triage.md (role of each variable, direction of each
   suspected edge, any unrecorded/unmeasured variables with a plausible
   causal role) and fill in `role`, `edges`, and `unrecorded_variables`
   together -- unmeasured confounders can and should be added as nodes even
   though there's no data for them, to make that assumption explicit.
3. Call `validate_schema()` -- it rejects cycles and edges that reference
   unknown variables, both of which make everything below meaningless.
4. Call `draw_dag()` to visualize the result and sanity-check it with the user.
5. Call `naive_adjustment_set()` for a *first-pass* suggestion of which
   variables to condition on when estimating the exposure -> outcome effect.
   This is a simplification of Pearl's backdoor criterion (PEARL_CAUSALITY),
   not a substitute for it -- for anything beyond a small/simple DAG, verify
   with a dedicated tool (e.g. R's `dagitty`) or a domain expert.

Requires: matplotlib. (json and pathlib are stdlib.)
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


def create_schema_template(recorded_variables, path="causal_dag_schema.json", outcome=None, exposure=None):
    """Generate an empty/prefilled DAG elicitation schema and save it as JSON.

    `recorded_variables`: list of column names from the actual dataset -- one
    node is pre-created per column. The user (with the agent's help) then
    fills in `role` for each, adds any `unrecorded_variables` believed to
    matter causally, and lists `edges` between all of them.
    """
    schema = {
        "outcome": outcome,
        "exposure": exposure,
        "variables": [
            {"name": v, "recorded": True, "role": "unknown", "notes": ""}
            for v in recorded_variables
        ],
        "unrecorded_variables": [],
        "edges": [],
        "open_questions": [],
    }
    Path(path).write_text(json.dumps(schema, indent=2))
    return schema


def load_schema(path="causal_dag_schema.json") -> dict:
    return json.loads(Path(path).read_text())


def save_schema(schema: dict, path="causal_dag_schema.json"):
    Path(path).write_text(json.dumps(schema, indent=2))


def _all_node_names(schema: dict):
    recorded = [v["name"] for v in schema["variables"]]
    unrecorded = [v["name"] for v in schema.get("unrecorded_variables", [])]
    return recorded, unrecorded


def _topological_layers(schema: dict) -> list:
    """Kahn's algorithm, grouped into generations -- also doubles as validation.

    Raises ValueError if an edge references a variable not in the schema, or if
    the edges form a cycle (both make the DAG-based functions below meaningless).
    """
    recorded, unrecorded = _all_node_names(schema)
    nodes = recorded + unrecorded
    node_set = set(nodes)

    dangling = {
        name
        for e in schema.get("edges", [])
        for name in (e["from"], e["to"])
        if name not in node_set
    }
    if dangling:
        raise ValueError(
            f"Edge(s) reference variable(s) not present in the schema: {sorted(dangling)}. "
            "Add them to 'variables'/'unrecorded_variables' before drawing or computing an adjustment set."
        )

    children: dict = {n: set() for n in nodes}
    in_degree: dict = {n: 0 for n in nodes}
    for e in schema.get("edges", []):
        children[e["from"]].add(e["to"])
        in_degree[e["to"]] += 1

    remaining = set(nodes)
    layers = []
    while remaining:
        ready = sorted(n for n in remaining if in_degree[n] == 0)
        if not ready:
            raise ValueError(
                f"Schema contains a cycle among: {sorted(remaining)}. A causal DAG cannot have "
                "cycles -- fix the edge directions before drawing or computing an adjustment set."
            )
        layers.append(ready)
        for n in ready:
            remaining.remove(n)
            for c in children[n]:
                in_degree[c] -= 1
    return layers


def validate_schema(schema: dict) -> None:
    """Raise ValueError if the schema isn't a valid DAG (dangling edges or a cycle).

    Call this before trusting `draw_dag()` or `naive_adjustment_set()` -- both assume
    a valid DAG and will give silently wrong answers (or crash) on one that isn't.
    """
    _topological_layers(schema)


def draw_dag(schema: dict, ax=None):
    """Draw the DAG with a layered (topological-generation) layout -- no networkx dependency.

    Nodes are grouped into rows by topological generation (sources at the top),
    which keeps most edges pointing the same direction and reads better than an
    arbitrary layout once the DAG has more than a handful of nodes. Recorded
    variables are solid-filled circles; unrecorded/unmeasured variables are
    drawn with a dashed outline, to keep the "this isn't in the data" assumption
    visually explicit.
    """
    layers = _topological_layers(schema)  # also validates (raises on cycle/dangling edges)
    recorded, unrecorded = _all_node_names(schema)
    recorded_set = set(recorded)

    n_layers = len(layers)
    pos = {}
    for layer_idx, layer_nodes in enumerate(layers):
        y = 1.0 - (2.0 * layer_idx / max(n_layers - 1, 1)) if n_layers > 1 else 0.0
        width = len(layer_nodes)
        for i, name in enumerate(layer_nodes):
            x = (i - (width - 1) / 2.0) * 1.6
            pos[name] = (x, y)

    if ax is None:
        _, ax = plt.subplots(figsize=(max(7, 1.6 * max(len(layer) for layer in layers)), 7))

    for edge in schema.get("edges", []):
        x0, y0 = pos[edge["from"]]
        x1, y1 = pos[edge["to"]]
        ax.annotate(
            "", xy=(x1, y1), xycoords="data", xytext=(x0, y0), textcoords="data",
            arrowprops=dict(arrowstyle="-|>", color="black", lw=1.5,
                             shrinkA=18, shrinkB=18, connectionstyle="arc3,rad=0.08"),
        )

    for name, (x, y) in pos.items():
        if name in recorded_set:
            ax.scatter([x], [y], s=1800, facecolor="#cfe8ff", edgecolor="black", zorder=3)
            ax.text(x, y, name, ha="center", va="center", zorder=4, fontsize=9)
        else:
            ax.scatter([x], [y], s=1800, facecolor="white", edgecolor="black", linestyle="--", zorder=3)
            ax.text(x, y, name, ha="center", va="center", zorder=4, fontsize=9, style="italic")

    xs = [x for x, _ in pos.values()]
    ax.set_xlim(min(xs) - 1.2, max(xs) + 1.2)
    ax.set_ylim(-1.3, 1.3)
    ax.axis("off")
    ax.set_title("Elicited causal DAG (top = sources; dashed = unrecorded / unmeasured)")
    return ax


def _ancestors(schema: dict, target: str) -> set:
    parents: dict = {}
    for e in schema.get("edges", []):
        parents.setdefault(e["to"], set()).add(e["from"])
    seen, frontier = set(), [target]
    while frontier:
        node = frontier.pop()
        for p in parents.get(node, ()):
            if p not in seen:
                seen.add(p)
                frontier.append(p)
    return seen


def _descendants(schema: dict, source: str) -> set:
    children: dict = {}
    for e in schema.get("edges", []):
        children.setdefault(e["from"], set()).add(e["to"])
    seen, frontier = set(), [source]
    while frontier:
        node = frontier.pop()
        for c in children.get(node, ()):
            if c not in seen:
                seen.add(c)
                frontier.append(c)
    return seen


def naive_adjustment_set(schema: dict, exposure: str, outcome: str) -> list:
    """First-pass suggestion of a backdoor-style adjustment set.

    Heuristic: common ancestors of exposure and outcome, minus anything that
    is a descendant of the exposure (a mediator/collider, not a confounder --
    adjusting for it would bias the estimate, not clean it up).

    This is NOT a full implementation of Pearl's backdoor criterion -- it
    does not verify that every backdoor path is actually blocked and will not
    catch collider-induced bias outside this simple case. Validate with a
    dedicated tool (e.g. R's `dagitty`) before trusting it on a nontrivial DAG.
    """
    validate_schema(schema)
    exposure_ancestors = _ancestors(schema, exposure)
    outcome_ancestors = _ancestors(schema, outcome)
    exposure_descendants = _descendants(schema, exposure)
    candidates = (exposure_ancestors & outcome_ancestors) - exposure_descendants
    return sorted(candidates)


if __name__ == "__main__":
    demo_schema = create_schema_template(
        recorded_variables=["exposure", "outcome", "confounder", "mediator"],
        path="_demo_causal_dag_schema.json",
        outcome="outcome",
        exposure="exposure",
    )
    demo_schema["edges"] = [
        {"from": "confounder", "to": "exposure", "confidence": "high", "rationale": "demo"},
        {"from": "confounder", "to": "outcome", "confidence": "high", "rationale": "demo"},
        {"from": "exposure", "to": "mediator", "confidence": "high", "rationale": "demo"},
        {"from": "mediator", "to": "outcome", "confidence": "high", "rationale": "demo"},
        {"from": "exposure", "to": "outcome", "confidence": "medium", "rationale": "demo direct effect"},
    ]
    save_schema(demo_schema, "_demo_causal_dag_schema.json")
    validate_schema(demo_schema)
    print("Suggested naive adjustment set:", naive_adjustment_set(demo_schema, "exposure", "outcome"))
    draw_dag(demo_schema)
    plt.show()
