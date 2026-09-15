"""Create a fresh local Git repository for Lab 3.1 with real worker history."""

import json
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

START_SOURCE = Path(__file__).parents[1] / "start" / "project"
SOLUTION_SOURCE = Path(__file__).parent / "project"
DEFAULT_TARGET = "lab-workspace-solution"

FOCUSED = {
    "email": "python3 -m unittest tests.test_email tests.test_security.ChannelSecurityTest.test_email_escapes_untrusted_html",
    "sms": "python3 -m unittest tests.test_sms tests.test_security.ChannelSecurityTest.test_sms_normalizes_control_whitespace",
}


def run(*args, cwd):
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def run_soft(*args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


def commit(root, message):
    run("git", "add", ".", cwd=root)
    run("git", "commit", "-m", message, cwd=root)


def unittest_status(root, *args):
    result = run_soft(sys.executable, "-m", "unittest", *args, cwd=root)
    return "passed" if result.returncode == 0 else "failed"


def recorded_status(root, command):
    tokens = shlex.split(command)
    tokens[0] = sys.executable
    result = run_soft(*tokens, cwd=root)
    return "passed" if result.returncode == 0 else "failed"


def create_conflict_fixtures(root):
    router = root / "router.py"
    original = router.read_text()
    run("git", "switch", "-c", "fixture/conflict-email", cwd=root)
    router.write_text(original.replace('CHANNEL_ORDER = ("email", "sms")', 'CHANNEL_ORDER = ("email", "sms", "email")'))
    commit(root, "Add conflicting email routing preference")
    run("git", "switch", "main", cwd=root)
    run("git", "switch", "-c", "fixture/conflict-sms", cwd=root)
    router.write_text(original.replace('CHANNEL_ORDER = ("email", "sms")', 'CHANNEL_ORDER = ("sms", "email")'))
    commit(root, "Add conflicting SMS routing preference")
    run("git", "switch", "main", cwd=root)


COMMIT_MESSAGES = {"email": "Complete email renderer", "sms": "Complete SMS renderer"}


def complete_worker(root, name, base_hash):
    run("git", "switch", "-c", f"agent/{name}", "main", cwd=root)
    shutil.copy(SOLUTION_SOURCE / "channels" / f"{name}.py", root / "channels" / f"{name}.py")
    commit(root, COMMIT_MESSAGES[name])
    impl_hash = run("git", "rev-parse", "HEAD", cwd=root)
    status = recorded_status(root, FOCUSED[name])
    if status != "passed":
        raise SystemExit(f"{name} focused check failed; aborting setup.")
    handoff = json.loads((SOLUTION_SOURCE / "handoffs" / f"{name}.json").read_text())
    handoff["base_commit"] = base_hash
    handoff["implementation_commit"] = impl_hash
    handoff["verification"]["status"] = status
    (root / "handoffs" / f"{name}.json").write_text(json.dumps(handoff, indent=2) + "\n")
    commit(root, f"Record {name} handoff")
    run("git", "switch", "main", cwd=root)


def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TARGET).resolve()
    if target.exists():
        raise SystemExit(f"Target already exists: {target}")
    shutil.copytree(START_SOURCE, target)
    run("git", "init", "-b", "main", cwd=target)
    run("git", "config", "user.name", "Course Learner", cwd=target)
    run("git", "config", "user.email", "learner@example.invalid", cwd=target)
    commit(target, "Create Lab 3.1 base")
    run("git", "tag", "lab-base", cwd=target)
    base_hash = run("git", "rev-parse", "lab-base", cwd=target)
    create_conflict_fixtures(target)

    complete_worker(target, "email", base_hash)
    complete_worker(target, "sms", base_hash)

    run("git", "merge", "--no-edit", "--no-ff", "agent/email", cwd=target)
    run("git", "merge", "--no-edit", "--no-ff", "agent/sms", cwd=target)
    full_status = unittest_status(target)
    security_status = unittest_status(target, "tests.test_security")
    if full_status != "passed" or security_status != "passed":
        raise SystemExit("Integrated workspace checks failed; aborting setup.")

    run("git", "switch", "-c", "conflict-practice", "main", cwd=target)
    run("git", "merge", "--no-edit", "fixture/conflict-email", cwd=target)
    conflict = run_soft("git", "merge", "--no-edit", "fixture/conflict-sms", cwd=target)
    if (conflict.returncode == 0
            or "CONFLICT (content)" not in conflict.stdout + conflict.stderr
            or "UU router.py" not in run("git", "status", "--short", cwd=target)):
        raise SystemExit("Expected router.py conflict was not produced; aborting setup.")
    shutil.copy(SOLUTION_SOURCE / "router.py", target / "router.py")
    run("git", "add", "router.py", cwd=target)
    run("git", "commit", "--no-edit", cwd=target)
    if unittest_status(target) != "passed":
        raise SystemExit("Conflict-practice workspace checks failed; aborting setup.")
    run("git", "switch", "main", cwd=target)

    record = json.loads((SOLUTION_SOURCE / "integration-record.json").read_text())
    record["full_check"]["status"] = unittest_status(target)
    record["security_check"]["status"] = unittest_status(target, "tests.test_security")
    (target / "integration-record.json").write_text(json.dumps(record, indent=2) + "\n")
    commit(target, "Record integration evidence")

    print(f"Created {target}")
    print(f"Base commit: {run('git', 'rev-parse', '--short', 'lab-base', cwd=target)}")
    print("Fixture branches: fixture/conflict-email, fixture/conflict-sms")
    print("Worker branches: agent/email, agent/sms")
    print("Conflict-practice branch: conflict-practice")


if __name__ == "__main__":
    main()
