"""Verify Lab 3.1 handoff and integration evidence."""

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
EXPECTED = {
    "email": {
        "task_id": "email-renderer",
        "files": {"channels/email.py", "handoffs/email.json"},
        "command": "python3 -m unittest tests.test_email tests.test_security.ChannelSecurityTest.test_email_escapes_untrusted_html",
    },
    "sms": {
        "task_id": "sms-renderer",
        "files": {"channels/sms.py", "handoffs/sms.json"},
        "command": "python3 -m unittest tests.test_sms tests.test_security.ChannelSecurityTest.test_sms_normalizes_control_whitespace",
    },
}


def load(path):
    return json.loads((ROOT / path).read_text())


def contains_todo(value):
    if isinstance(value, str):
        return "todo" in value.lower()
    if isinstance(value, list):
        return any(contains_todo(item) for item in value)
    if isinstance(value, dict):
        return any(contains_todo(item) for item in value.values())
    return False


def verify_handoff(name, errors):
    handoff = load(f"handoffs/{name}.json")
    expected = EXPECTED[name]
    if contains_todo(handoff):
        errors.append(f"{name} handoff contains TODO evidence.")
    if handoff.get("task_id") != expected["task_id"]:
        errors.append(f"{name} handoff has the wrong task ID.")
    if set(handoff.get("changed_files", [])) != expected["files"]:
        errors.append(f"{name} handoff changed-file inventory violates ownership.")
    if len(handoff.get("implementation_commit", "")) < 7:
        errors.append(f"{name} handoff needs an implementation commit.")
    verification = handoff.get("verification", {})
    if verification.get("command") != expected["command"] or verification.get("status") != "passed":
        errors.append(f"{name} handoff lacks passing focused evidence.")
    return handoff


def schema_is_unchanged():
    tag = subprocess.run(
        ["git", "rev-parse", "--verify", "lab-base"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if tag.returncode != 0:
        return True
    diff = subprocess.run(
        ["git", "diff", "--quiet", "lab-base", "--", "schemas/shipment-event.json"],
        cwd=ROOT,
    )
    return diff.returncode == 0


def main():
    errors = []
    email = verify_handoff("email", errors)
    sms = verify_handoff("sms", errors)
    if email.get("base_commit") != sms.get("base_commit"):
        errors.append("Worker handoffs do not share a base commit.")

    record = load("integration-record.json")
    if contains_todo(record):
        errors.append("Integration record contains TODO evidence.")
    if record.get("merge_order") != ["agent/email", "agent/sms"]:
        errors.append("Merge order must be agent/email then agent/sms.")
    if record.get("approved_before_second_merge") is not True:
        errors.append("Human approval before the second merge is missing.")
    if record.get("full_check", {}).get("status") != "passed":
        errors.append("Full combined check is not recorded as passed.")
    if record.get("security_check", {}).get("status") != "passed":
        errors.append("Security check is not recorded as passed.")
    if not schema_is_unchanged():
        errors.append("The locked shipment-event schema changed from lab-base.")

    if errors:
        print("ORCHESTRATION RECORD INVALID")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("ORCHESTRATION RECORD VALID")
    print("Merge order: agent/email -> agent/sms")
    print("Human checkpoint: approved before second merge")
    print("Combined and security checks: passed")


if __name__ == "__main__":
    main()
