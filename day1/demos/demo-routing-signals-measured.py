"""
Demo - Model Routing From Measured Repository Signals
Day 1 - Session 1, Topic 2

Goal: Compute blast radius, verification cover, and reversibility from the real
repository so the routing tier is an output of measurement, not an opinion.

Earlier planning demos scored each task by hand, which makes the score the
answer. Here every signal is measured: blast radius counts the modules that
really import the target, verification cover counts the real test methods that
exercise it, and reversibility is read from the schema contract on disk. Two
candidate changes are scored with one rule, and they land in different tiers
because the repository differs, not because the tiers were typed in.

Model names are dated examples. The durable rule is the measured evidence.

No API key needed. Pure Python standard library.

Run: python3 day1/demos/demo-routing-signals-measured.py
"""

import ast
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from demo_support import (  # noqa: E402
    assert_true,
    colab_note,
    heading,
    sandbox,
    show_evidence,
)

RESEARCH_NOTE = "Tier names are examples; the measured signals are the durable rule."
CANDIDATES = [
    {
        "task": "Reword the shipment email subject line",
        "target": Path("channels") / "email.py",
        "touches_contract": False,
    },
    {
        "task": "Add a task-card note for the SMS owner",
        "target": Path("task-cards") / "sms.md",
        "touches_contract": False,
    },
    {
        "task": "Change the locked shipment event contract",
        "target": Path("schemas") / "shipment-event.json",
        "touches_contract": True,
    },
]


def importers_of(root, target):
    """Count modules that genuinely import the target module."""
    if target.suffix != ".py":
        return []
    dotted = str(target.with_suffix("")).replace("/", ".")
    found = []
    for path in root.rglob("*.py"):
        if "__pycache__" in path.parts or path == root / target:
            continue
        if path.name.startswith("test_"):
            continue  # tests verify the change; they are not downstream consumers
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            elif isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            if any(name == dotted or name.startswith(f"{dotted}.") for name in names):
                found.append(str(path.relative_to(root)))
                break
    return sorted(set(found))


def contract_consumers(root, target):
    """Count modules that read a non-Python contract file by name."""
    needle = target.name
    return sorted(
        str(path.relative_to(root))
        for path in root.rglob("*.py")
        if "__pycache__" not in path.parts and needle in path.read_text()
    )


def imports_target(source, target):
    """True when the parsed source really imports the target module."""
    dotted = str(target.with_suffix("")).replace("/", ".")
    for node in ast.walk(ast.parse(source)):
        names = []
        if isinstance(node, ast.ImportFrom) and node.module:
            names = [node.module]
        elif isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        if any(name == dotted or name.startswith(f"{dotted}.") for name in names):
            return True
    return False


def test_methods_covering(root, target):
    """Count real test methods in modules that import the target module."""
    covering = []
    for path in sorted((root / "tests").rglob("test_*.py")):
        source = path.read_text()
        direct = target.suffix == ".py" and imports_target(source, target)
        indirect = target.suffix != ".py" and target.name in source
        if not (direct or indirect):
            continue
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                covering.append(f"{path.relative_to(root)}::{node.name}")
    return sorted(covering)


def reversibility(root, candidate):
    """Read the schema contract to decide whether the change is reversible."""
    if not candidate["touches_contract"]:
        return True, "module-local change, revert by restoring the file"
    schema = json.loads((root / "schemas" / "shipment-event.json").read_text())
    locked = schema.get("additionalProperties") is False
    return (
        not locked,
        f"schema version {schema['version']} locks additionalProperties={schema.get('additionalProperties')}",
    )


def tier(blast, cover, reversible):
    """One rule, applied to measured signals."""
    if not reversible:
        return "Strong model, high effort, human approval required"
    if blast >= 2 or cover >= 5:
        return "Strong model, high effort, risk-based approval"
    if cover >= 3:
        return "Mid model, medium effort, focused check"
    return "Efficient model, low effort, no approval"


def main():
    colab_note()
    print(RESEARCH_NOTE)
    with sandbox(with_git=False) as (root, _):
        results = []
        for candidate in CANDIDATES:
            target = candidate["target"]
            heading(f"Candidate: {candidate['task']}")
            show_evidence("target file", str(target))

            if target.suffix == ".py":
                reached = importers_of(root, target)
                blast_label = "modules importing it"
            else:
                reached = contract_consumers(root, target)
                blast_label = "modules reading it"

            cover = test_methods_covering(root, target)
            reversible, why = reversibility(root, candidate)

            show_evidence(blast_label, ", ".join(reached) or "(none)")
            show_evidence("blast radius (measured)", len(reached))
            show_evidence("test methods covering", len(cover))
            for name in cover:
                show_evidence("", name)
            show_evidence("reversible", "yes" if reversible else "NO")
            show_evidence("evidence", why)

            decision = tier(len(reached), len(cover), reversible)
            show_evidence("routing tier", decision)
            results.append((candidate["task"], len(reached), len(cover), reversible, decision))

        heading("Side-by-side: one rule, different measured inputs")
        for task, blast, cover, reversible, decision in results:
            show_evidence(task[:24], f"blast={blast} cover={cover} reversible={reversible} -> {decision.split(',')[0]}")

        heading("Evidence checks")
        assert_true(
            results[0][1] >= 1, "the email change's blast radius came from real imports"
        )
        assert_true(
            any("Efficient" in result[4] for result in results),
            "a change nothing imports stayed in the cheap tier",
        )
        assert_true(results[0][2] >= 1, "real test methods were counted, not estimated")
        assert_true(
            any(result[3] is False for result in results),
            "the schema file on disk proved one change irreversible",
        )
        assert_true(
            len({result[4] for result in results}) >= 3,
            "measured signals produced three distinct tiers",
        )

    print(
        "\nTakeaway: Measure blast radius, verification cover, and reversibility"
        "\nfrom the repository, then let one rule assign the tier."
    )


if __name__ == "__main__":
    main()
