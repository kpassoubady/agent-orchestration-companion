"""Validate the machine-readable task contract for Lab 1.1."""

import json
import sys
from collections import defaultdict
from pathlib import Path

REQUIRED_FIELDS = {
    "id",
    "objective",
    "deliverable",
    "files",
    "depends_on",
    "classification",
    "acceptance",
    "non_goals",
}
ALLOWED_CLASSIFICATIONS = {"parallel", "sequential", "human-controlled"}
ALLOWED_COMMANDS = {
    "python3 -m unittest tests.test_schema",
    "python3 -m unittest tests.test_email",
    "python3 -m unittest tests.test_sms",
    "python3 -m unittest tests.test_preferences",
    "python3 -m unittest tests.test_audit",
    "python3 -m unittest tests.test_notifications",
    "python3 -m unittest tests.test_security",
}


def contains_todo(value):
    if isinstance(value, str):
        return "todo" in value.lower()
    if isinstance(value, list):
        return any(contains_todo(item) for item in value)
    if isinstance(value, dict):
        return any(contains_todo(item) for item in value.values())
    return False


def execution_waves(tasks):
    remaining = {task["id"]: set(task["depends_on"]) for task in tasks}
    completed = set()
    waves = []
    while remaining:
        ready = sorted(task_id for task_id, deps in remaining.items() if deps <= completed)
        if not ready:
            return None
        waves.append(ready)
        completed.update(ready)
        for task_id in ready:
            del remaining[task_id]
    return waves


def validate(plan):
    errors = []
    tasks = plan.get("tasks", [])
    if len(tasks) < 5:
        errors.append("Define at least five bounded tasks.")
    if contains_todo(plan.get("human_approval_point", "")) or not plan.get("human_approval_point"):
        errors.append("Replace the human approval TODO with an observable checkpoint.")

    task_ids = [task.get("id") for task in tasks]
    if len(task_ids) != len(set(task_ids)):
        errors.append("Task IDs must be unique.")

    owners = defaultdict(list)
    for index, task in enumerate(tasks, start=1):
        missing = REQUIRED_FIELDS - task.keys()
        if missing:
            errors.append(f"Task {index} is missing: {', '.join(sorted(missing))}.")
            continue
        if contains_todo(task):
            errors.append(f"Task {task['id']} still contains TODO text.")
        if task["classification"] not in ALLOWED_CLASSIFICATIONS:
            errors.append(f"Task {task['id']} has an invalid classification.")
        if not task["files"]:
            errors.append(f"Task {task['id']} must own at least one file.")
        if not task["acceptance"]:
            errors.append(f"Task {task['id']} needs an acceptance command.")
        for command in task["acceptance"]:
            if command not in ALLOWED_COMMANDS:
                errors.append(f"Task {task['id']} uses an unsupplied command: {command}")
        if not task["non_goals"]:
            errors.append(f"Task {task['id']} needs at least one non-goal.")
        for path in task["files"]:
            owners[path].append(task["id"])
        for dependency in task["depends_on"]:
            if dependency not in task_ids:
                errors.append(f"Task {task['id']} has unknown dependency {dependency}.")

    for path, task_owners in owners.items():
        if len(task_owners) > 1:
            errors.append(f"File {path} has multiple owners: {', '.join(task_owners)}.")

    by_id = {task.get("id"): task for task in tasks}
    schema = by_id.get("schema-contract")
    if not schema or schema.get("classification") != "human-controlled":
        errors.append("schema-contract must be human-controlled.")
    integration = by_id.get("notification-integration")
    if not integration or "router.py" not in integration.get("files", []):
        errors.append("notification-integration must own router.py.")
    if integration and len(integration.get("depends_on", [])) < 3:
        errors.append("notification-integration needs at least three upstream dependencies.")

    waves = execution_waves(tasks) if not any(task_id is None for task_id in task_ids) else None
    if waves is None:
        errors.append("Dependencies contain a cycle or an unreachable task.")
    return errors, waves


def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "task-plan.json")
    plan = json.loads(path.read_text())
    errors, waves = validate(plan)
    if errors:
        print("PLAN INVALID")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("PLAN VALID")
    for number, wave in enumerate(waves, start=1):
        print(f"Wave {number}: {', '.join(wave)}")
    print(f"Human approval: {plan['human_approval_point']}")


if __name__ == "__main__":
    main()
