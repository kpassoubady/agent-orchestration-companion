"""
Demo - Git Worktree Isolation
Day 1 - Session 1, Topic 3

Goal: Create two real Git worktrees, commit independent changes, and integrate them.

Requires Git and Python. No API key or network access needed.

Run: python3 day1/concepts/demos-conceptual/demo-git-worktree-isolation.py
"""

import subprocess
import tempfile
from pathlib import Path

BRANCHES = (("agent/email", "email.txt", "email renderer\n"), ("agent/sms", "sms.txt", "sms renderer\n"))


def run(*args, cwd):
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def initialize_repository(root):
    run("git", "init", "-b", "main", cwd=root)
    run("git", "config", "user.name", "Course Demo", cwd=root)
    run("git", "config", "user.email", "demo@example.invalid", cwd=root)
    (root / "README.md").write_text("shipment notification demo\n")
    run("git", "add", "README.md", cwd=root)
    run("git", "commit", "-m", "Create demo base", cwd=root)


def create_worker(root, branch, filename, content):
    worktree = root.parent / branch.replace("/", "-")
    run("git", "worktree", "add", str(worktree), "-b", branch, cwd=root)
    (worktree / filename).write_text(content)
    run("git", "add", filename, cwd=worktree)
    run("git", "commit", "-m", f"Complete {branch}", cwd=worktree)
    return worktree


def integrate(root):
    for branch, _, _ in BRANCHES:
        run("git", "merge", "--no-edit", branch, cwd=root)
    return run("git", "log", "--oneline", "--decorate", "-3", cwd=root)


def main():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "notification-repo"
        root.mkdir()
        initialize_repository(root)
        workers = [create_worker(root, *definition) for definition in BRANCHES]
        print("Isolated worktrees:")
        print(run("git", "worktree", "list", cwd=root))
        print(f"\nMain sees worker files before merge: {[(root / name).exists() for _, name, _ in BRANCHES]}")
        print(f"Worker paths: {', '.join(str(path.name) for path in workers)}")
        print("\nIntegration history:")
        print(integrate(root))
        print(f"Combined files exist: {[(root / name).exists() for _, name, _ in BRANCHES]}")
    print("Takeaway: Worktrees isolate edits; explicit merges and checks create the combined result.")


if __name__ == "__main__":
    main()
