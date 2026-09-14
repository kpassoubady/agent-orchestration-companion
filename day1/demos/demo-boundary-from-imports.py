"""
Demo - Task Boundaries From the Real Import Graph
Day 1 - Session 1, Topic 1

Goal: Derive file ownership, shared-hub conflicts, and safe execution waves by
parsing the real notification service instead of a hand-written task list.

The plan is not written into this file. The demo parses every module in the
course codebase with Python's own `ast` module, builds the internal import
graph, finds the module that more than one channel task would have to edit, and
computes the execution waves from that measured graph. Change the code and the
plan changes with it.

No API key needed. Pure Python standard library.

Run: python3 day1/demos/demo-boundary-from-imports.py
"""

import ast
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from demo_support import (  # noqa: E402
    assert_true,
    colab_note,
    heading,
    python_files,
    sandbox,
    show_evidence,
)

CHANNEL_DIR = "channels"


def module_name(path, root):
    """Convert a file path into its dotted module name."""
    relative = path.relative_to(root).with_suffix("")
    parts = [part for part in relative.parts if part != "__init__"]
    return ".".join(parts)


def internal_imports(path, known_modules):
    """Parse one file and return the internal modules it imports."""
    tree = ast.parse(path.read_text())
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            candidate = node.module
        elif isinstance(node, ast.Import):
            candidate = node.names[0].name
        else:
            continue
        root_package = candidate.split(".")[0]
        for module in known_modules:
            if module == candidate or module.split(".")[0] == root_package:
                found.add(module)
    return found


def build_graph(root):
    """Return {module: {imported internal modules}} for the real codebase."""
    files = python_files(root)
    modules = {module_name(path, root): path for path in files}
    return {name: internal_imports(path, set(modules)) for name, path in modules.items()}, modules


def find_hub(graph):
    """The hub is the module importing the most internal modules."""
    return max(graph.items(), key=lambda item: len(item[1]))


def derive_tasks(graph, hub_name):
    """Create one task per channel module plus one integration task for the hub."""
    channel_modules = sorted(name for name in graph if name.startswith(f"{CHANNEL_DIR}."))
    tasks = [
        {"id": name.split(".")[-1], "owns": [f"{name.replace('.', '/')}.py"], "depends_on": ["schema"]}
        for name in channel_modules
    ]
    tasks.insert(0, {"id": "schema", "owns": ["schemas/shipment-event.json"], "depends_on": []})
    tasks.append(
        {
            "id": "integration",
            "owns": [f"{hub_name}.py"],
            "depends_on": [task["id"] for task in tasks if task["id"] != "schema"],
        }
    )
    return tasks


def naive_conflicts(graph, hub_name, tasks):
    """Show what breaks when each channel task also edits the shared hub."""
    owners = defaultdict(list)
    for task in tasks:
        if task["id"] in {"schema", "integration"}:
            continue
        for path in task["owns"] + [f"{hub_name}.py"]:
            owners[path].append(task["id"])
    return {path: ids for path, ids in owners.items() if len(ids) > 1}


def execution_waves(tasks):
    """Compute dependency waves from the derived task graph."""
    remaining = {task["id"]: set(task["depends_on"]) for task in tasks}
    waves, done = [], set()
    while remaining:
        ready = sorted(task for task, deps in remaining.items() if deps <= done)
        if not ready:
            raise ValueError("Dependency cycle detected")
        waves.append(ready)
        done.update(ready)
        for task in ready:
            del remaining[task]
    return waves


def main():
    colab_note()
    with sandbox(with_git=False) as (root, _):
        graph, modules = build_graph(root)

        heading("Measured import graph (parsed, not declared)")
        for name in sorted(graph):
            imports = ", ".join(sorted(graph[name])) or "(none)"
            show_evidence(f"{name}.py imports", imports)

        hub_name, hub_imports = find_hub(graph)
        heading("Shared hub detected from the graph")
        show_evidence("hub module", f"{hub_name}.py")
        show_evidence("internal modules it wires", len(hub_imports))
        show_evidence("why it is the hub", "highest internal fan-out of any module")

        tasks = derive_tasks(graph, hub_name)
        conflicts = naive_conflicts(graph, hub_name, tasks)

        heading("Naive split: every channel task also edits the hub")
        for path, ids in sorted(conflicts.items()):
            show_evidence(path, f"contested by {', '.join(ids)}")
        show_evidence("parallel-safe", "no: concurrent edits to one file")

        heading("Contract-first plan: the hub has a single owner")
        for task in tasks:
            depends = ", ".join(task["depends_on"]) or "(none)"
            show_evidence(task["id"], f"owns {', '.join(task['owns'])} | after {depends}")

        waves = execution_waves(tasks)
        heading("Execution waves computed from the derived dependencies")
        for number, wave in enumerate(waves, start=1):
            show_evidence(f"wave {number}", ", ".join(wave))

        heading("Evidence checks")
        assert_true(len(conflicts) >= 1, f"the naive split contests {hub_name}.py")
        assert_true(
            sum(len(wave) for wave in waves) == len(tasks),
            "every derived task is scheduled exactly once",
        )
        assert_true(
            len(waves[1]) > 1, f"wave 2 runs {len(waves[1])} channel tasks concurrently"
        )
        assert_true(
            modules[hub_name].exists(), f"{hub_name}.py was read from disk, not assumed"
        )

    print(
        "\nTakeaway: Parse the codebase to find the shared hub, give it one owner,"
        "\nand parallelism follows from the measured dependency graph."
    )


if __name__ == "__main__":
    main()
