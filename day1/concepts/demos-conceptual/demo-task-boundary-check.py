"""
Demo - Task Boundary Check
Day 1 - Session 1, Topic 1

Goal: Compare a naive feature split with a dependency-aware plan using computed evidence.

No API key needed. Pure Python standard library.

Run: python3 day1/concepts/demos-conceptual/demo-task-boundary-check.py
"""

from collections import defaultdict, deque

NAIVE_TASKS = [
    {"id": "email", "files": ["router.py", "email.py"], "depends_on": []},
    {"id": "sms", "files": ["router.py", "sms.py"], "depends_on": []},
    {"id": "audit", "files": ["router.py", "audit.py"], "depends_on": []},
]

BOUNDED_TASKS = [
    {"id": "schema", "files": ["schemas/shipment.json"], "depends_on": []},
    {"id": "email", "files": ["channels/email.py"], "depends_on": ["schema"]},
    {"id": "sms", "files": ["channels/sms.py"], "depends_on": ["schema"]},
    {"id": "audit", "files": ["audit/recorder.py"], "depends_on": ["schema"]},
    {
        "id": "integration",
        "files": ["router.py", "tests/test_notifications.py"],
        "depends_on": ["email", "sms", "audit"],
    },
]


def find_file_conflicts(tasks):
    owners = defaultdict(list)
    for task in tasks:
        for path in task["files"]:
            owners[path].append(task["id"])
    return {path: task_ids for path, task_ids in owners.items() if len(task_ids) > 1}


def execution_waves(tasks):
    remaining = {task["id"]: set(task["depends_on"]) for task in tasks}
    waves = []
    completed = set()
    while remaining:
        ready = sorted(task_id for task_id, deps in remaining.items() if deps <= completed)
        if not ready:
            raise ValueError("Dependency cycle detected")
        waves.append(ready)
        completed.update(ready)
        for task_id in ready:
            del remaining[task_id]
    return waves


def show_plan(name, tasks):
    conflicts = find_file_conflicts(tasks)
    print(f"\n{name}")
    print("-" * len(name))
    print(f"Tasks: {len(tasks)}")
    print(f"Shared-file conflicts: {len(conflicts)}")
    for path, owners in conflicts.items():
        print(f"  {path}: {', '.join(owners)}")
    for number, wave in enumerate(execution_waves(tasks), start=1):
        print(f"Wave {number}: {', '.join(wave)}")


def main():
    print("Retail shipment-notification decomposition")
    show_plan("Naive channel split", NAIVE_TASKS)
    show_plan("Contract-first bounded plan", BOUNDED_TASKS)
    print("\nTakeaway: Parallelize cohesive work only after contracts and hub-file ownership are explicit.")


if __name__ == "__main__":
    main()
