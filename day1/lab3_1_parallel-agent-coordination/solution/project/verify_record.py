"""Verify Lab 3.1 handoff and integration evidence."""

import json
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
EXPECTED = {
    "email": {
        "task_id": "email-renderer",
        "files": {"channels/email.py", "handoffs/email.json"},
        "implementation_file": "channels/email.py",
        "branch": "agent/email",
        "command": "python3 -m unittest tests.test_email tests.test_security.ChannelSecurityTest.test_email_escapes_untrusted_html",
    },
    "sms": {
        "task_id": "sms-renderer",
        "files": {"channels/sms.py", "handoffs/sms.json"},
        "implementation_file": "channels/sms.py",
        "branch": "agent/sms",
        "command": "python3 -m unittest tests.test_sms tests.test_security.ChannelSecurityTest.test_sms_normalizes_control_whitespace",
    },
}


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def resolve_commit(ref):
    result = git("rev-parse", "--verify", f"{ref}^{{commit}}")
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def is_ancestor(ancestor, descendant):
    return git("merge-base", "--is-ancestor", ancestor, descendant).returncode == 0


def changed_files(base, head):
    result = git("diff", "--name-only", f"{base}..{head}")
    if result.returncode != 0:
        return None
    return set(result.stdout.split())


def run_recorded(command):
    tokens = shlex.split(command)
    if tokens[:3] != ["python3", "-m", "unittest"]:
        return False
    tokens[0] = sys.executable
    return subprocess.run(tokens, cwd=ROOT, capture_output=True, text=True).returncode == 0


def branch_contains_order(ref):
    result = git("show", f"{ref}:router.py")
    if result.returncode != 0:
        return False
    return 'CHANNEL_ORDER = ("email", "sms")' in result.stdout


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


def verify_handoff(name, actual_base, errors):
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
    recorded_base = resolve_commit(handoff.get("base_commit", ""))
    if actual_base is None or recorded_base != actual_base:
        errors.append(f"{name} handoff base commit does not match lab-base.")
    impl = resolve_commit(handoff.get("implementation_commit", ""))
    if impl is None:
        errors.append(f"{name} implementation commit does not resolve to a real commit.")
    else:
        base_ref = actual_base if actual_base is not None else recorded_base
        if base_ref is not None and impl == base_ref:
            errors.append(f"{name} implementation commit equals the base commit.")
        else:
            if recorded_base is not None and not is_ancestor(recorded_base, impl):
                errors.append(f"{name} base commit is not an ancestor of the implementation commit.")
            own = git("diff-tree", "--no-commit-id", "--name-only", "-r", impl)
            if own.returncode != 0 or set(own.stdout.split()) != {expected["implementation_file"]}:
                errors.append(
                    f"{name} implementation commit does not change exactly {expected['implementation_file']}."
                )
    branch = resolve_commit(expected["branch"])
    if branch is None:
        errors.append(f"{name} worker branch {expected['branch']} does not resolve.")
    elif actual_base is not None and changed_files(actual_base, branch) != expected["files"]:
        errors.append(f"{name} worker branch changed files do not match the handoff inventory.")
    if verification.get("status") == "passed" and not run_recorded(verification.get("command", "")):
        errors.append(f"{name} recorded focused command fails on rerun.")
    return handoff


def schema_is_unchanged(actual_base):
    if actual_base is None:
        return False
    return git("diff", "--quiet", actual_base, "--", "schemas/shipment-event.json").returncode == 0


def main():
    errors = []
    actual_base = resolve_commit("lab-base")
    if actual_base is None:
        errors.append("The lab-base tag does not resolve to a commit.")
    email = verify_handoff("email", actual_base, errors)
    sms = verify_handoff("sms", actual_base, errors)
    if resolve_commit(email.get("base_commit", "")) != resolve_commit(sms.get("base_commit", "")):
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
    if not schema_is_unchanged(actual_base):
        errors.append("The locked shipment-event schema changed from lab-base.")

    for name, handoff in (("email", email), ("sms", sms)):
        impl = resolve_commit(handoff.get("implementation_commit", ""))
        if impl is not None and not is_ancestor(impl, "HEAD"):
            errors.append(f"{name} implementation commit is not an ancestor of HEAD.")

    if not run_recorded("python3 -m unittest"):
        errors.append("Full combined check fails on rerun.")
    if not run_recorded("python3 -m unittest tests.test_security"):
        errors.append("Security check fails on rerun.")

    conflict = resolve_commit("conflict-practice")
    if conflict is None:
        errors.append("The conflict-practice branch does not resolve.")
    else:
        for fixture in ("fixture/conflict-email", "fixture/conflict-sms"):
            fixture_commit = resolve_commit(fixture)
            if fixture_commit is None or not is_ancestor(fixture_commit, conflict):
                errors.append(f"{fixture} is not an ancestor of conflict-practice.")
        if not branch_contains_order("conflict-practice"):
            errors.append("conflict-practice does not preserve the approved channel order.")

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
