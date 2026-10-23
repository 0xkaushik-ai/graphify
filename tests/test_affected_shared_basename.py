"""#4698 — `affected <path>` must resolve a file whose basename is shared with
another file (so its label was disambiguated to `alpha/hooks.py`) when a second
node, such as a module docstring's rationale node, also sits on L1.
"""
from __future__ import annotations

import networkx as nx

from graphify.affected import resolve_seed


def _g():
    g = nx.DiGraph()
    for prefix in ("alpha", "beta"):
        src = f"app/{prefix}/hooks.py"
        g.add_node(f"app_{prefix}_hooks", label=f"{prefix}/hooks.py",
                   source_file=src, source_location="L1", file_type="code")
        g.add_node(f"app_{prefix}_hooks_rationale_1", label="Checks a request before it runs.",
                   source_file=src, source_location="L1", file_type="rationale")
        g.add_node(f"app_{prefix}_hooks_check", label="check()",
                   source_file=src, source_location="L4", file_type="code")
    return g


def test_disambiguated_file_label_resolves_by_path():
    g = _g()
    assert resolve_seed(g, "app/alpha/hooks.py") == "app_alpha_hooks"
    assert resolve_seed(g, "app/beta/hooks.py") == "app_beta_hooks"


def test_label_suffix_must_align_with_a_path_component():
    g = _g()
    # `lpha/hooks.py` is a string suffix of the query but not a path suffix.
    g.nodes["app_alpha_hooks"]["label"] = "lpha/hooks.py"
    assert resolve_seed(g, "app/alpha/hooks.py") is None


def test_unique_basename_with_docstring_still_resolves():
    g = nx.DiGraph()
    g.add_node("app_hooks", label="hooks.py", source_file="app/hooks.py", source_location="L1")
    g.add_node("app_hooks_rationale_1", label="Doc.", source_file="app/hooks.py", source_location="L1")
    assert resolve_seed(g, "app/hooks.py") == "app_hooks"
