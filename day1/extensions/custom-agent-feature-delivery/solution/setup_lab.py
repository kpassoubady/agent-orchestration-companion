import shutil
import subprocess
import sys
from pathlib import Path

SOURCE = Path(__file__).parent / "project"
STARTER = Path(__file__).parents[1] / "start" / "project"
DEFAULT_TARGET = "agent-lab-workspace-solution"


def run(*args, cwd):
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TARGET).resolve()
    if target.exists():
        raise SystemExit(f"Target already exists: {target}")
    shutil.copytree(STARTER, target)
    run("git", "init", "-b", "main", cwd=target)
    run("git", "config", "user.name", "Course Learner", cwd=target)
    run("git", "config", "user.email", "learner@example.invalid", cwd=target)
    run("git", "add", ".", cwd=target)
    run("git", "commit", "-m", "Create custom agent lab base", cwd=target)
    run("git", "tag", "lab-base", cwd=target)
    shutil.copytree(SOURCE, target, dirs_exist_ok=True)
    print(f"Created {target}")
    print(f"Base commit: {run('git', 'rev-parse', '--short', 'lab-base', cwd=target)}")


if __name__ == "__main__":
    main()
