"""Create a fresh local Git repository for Lab 3.1."""

import shutil
import subprocess
import sys
from pathlib import Path

SOURCE = Path(__file__).parent / "project"
DEFAULT_TARGET = "lab-workspace"


def run(*args, cwd):
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def commit(root, message):
    run("git", "add", ".", cwd=root)
    run("git", "commit", "-m", message, cwd=root)


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


def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TARGET).resolve()
    if target.exists():
        raise SystemExit(f"Target already exists: {target}")
    shutil.copytree(SOURCE, target)
    run("git", "init", "-b", "main", cwd=target)
    run("git", "config", "user.name", "Course Learner", cwd=target)
    run("git", "config", "user.email", "learner@example.invalid", cwd=target)
    commit(target, "Create Lab 3.1 base")
    run("git", "tag", "lab-base", cwd=target)
    create_conflict_fixtures(target)
    print(f"Created {target}")
    print(f"Base commit: {run('git', 'rev-parse', '--short', 'lab-base', cwd=target)}")
    print("Fixture branches: fixture/conflict-email, fixture/conflict-sms")


if __name__ == "__main__":
    main()
