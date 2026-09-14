"""
Shared support helpers for the Day 1 practical demos.

Not a demo. Every demo in this folder imports these helpers so the demos work
identically on a laptop and in Google Colab.

What this solves:

1. Colab has no course checkout, so `find_substrate` walks up from the current
   directory and clones the companion repository only when the files are absent.
2. Colab has no global Git identity, so `git_init` sets `user.name` and
   `user.email` on the sandbox repository itself instead of relying on
   `~/.gitconfig`.
3. Demos must never edit the learner's real repository, so `sandbox` copies the
   substrate into a temporary directory that is deleted on exit.

No API key needed. Pure Python standard library.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

REPO_URL = "https://github.com/kpassoubady/agent-orchestration-companion.git"
SUBSTRATE = Path("lab-workspace-solution")
MARKER = SUBSTRATE / "router.py"
GIT_IDENTITY = (("user.name", "Course Demo"), ("user.email", "demo@example.invalid"))


def git(*args, cwd, check=True):
    """Run one Git command and return its trimmed stdout."""
    result = subprocess.run(
        ("git",) + args, cwd=cwd, capture_output=True, text=True, check=check
    )
    return result.stdout.strip()


def run_tests(target, cwd):
    """Run one or more unittest targets and return (passed, combined_output).

    `target` may name several targets separated by spaces, exactly as the task
    cards write them, so a card's acceptance command can be passed through
    unchanged.
    """
    targets = target.split() if isinstance(target, str) else list(target)
    result = subprocess.run(
        [sys.executable, "-m", "unittest", *targets],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0, (result.stdout + result.stderr).strip()


def find_substrate():
    """Locate lab-workspace-solution/, cloning the repo on Colab if needed."""
    directory = Path.cwd()
    for _ in range(6):
        if (directory / MARKER).exists():
            return directory / SUBSTRATE
        directory = directory.parent

    clone = Path.cwd() / "agent-orchestration-companion"
    if not (clone / MARKER).exists():
        print(f"Course files not found near {Path.cwd()}.")
        print(f"Cloning {REPO_URL} ...")
        environment = dict(os.environ, GIT_TERMINAL_PROMPT="0")  # never hang on a credential prompt
        result = subprocess.run(
            ["git", "clone", "--depth", "1", "-q", REPO_URL, str(clone)],
            capture_output=True,
            text=True,
            env=environment,
        )
        if result.returncode != 0 or not (clone / MARKER).exists():
            raise SystemExit(
                "\nCould not fetch the course files automatically.\n"
                f"  git said: {result.stderr.strip().splitlines()[-1] if result.stderr.strip() else 'clone failed'}\n\n"
                "Run the demo from inside a checkout of the companion repository,\n"
                "or clone it first and re-run from that folder:\n"
                f"  git clone {REPO_URL}\n"
                "  cd agent-orchestration-companion\n"
                "  python3 day1/demos/<demo-name>.py"
            )
    return clone / SUBSTRATE


def git_init(root, message="Approve shipment notification base"):
    """Create a real Git repository with an explicit local identity.

    A `.gitignore` is written first so compiled bytecode never reaches a diff.
    Without it every `git diff --name-only` would list `__pycache__` entries and
    the ownership gates would report noise instead of source changes.
    """
    git("init", "-b", "main", cwd=root)
    for key, value in GIT_IDENTITY:
        git("config", key, value, cwd=root)
    (root / ".gitignore").write_text("__pycache__/\n*.pyc\n")
    git("add", "-A", cwd=root)
    git("commit", "-q", "-m", message, cwd=root)
    return git("rev-parse", "--short", "HEAD", cwd=root)


@contextmanager
def sandbox(with_git=True):
    """Copy the substrate into a temporary Git repository, then clean it up."""
    source = find_substrate()
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "notification-service"
        shutil.copytree(
            source, root, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git")
        )
        base = git_init(root) if with_git else None
        yield root, base


def heading(text):
    """Print a titled section separator."""
    print(f"\n{text}\n{'-' * len(text)}")


def show_evidence(label, value):
    """Print one aligned evidence line."""
    print(f"  {label:<26} {value}")


def relative_paths(paths, root):
    """Format paths relative to the sandbox root for readable output."""
    return sorted(str(Path(path).relative_to(root)) if Path(path).is_absolute() else str(path)
                  for path in paths)


def python_files(root):
    """Return every tracked Python module under the sandbox, excluding tests."""
    return sorted(
        path for path in root.rglob("*.py")
        if "__pycache__" not in path.parts
        and not path.name.startswith("test_")
        and path.name != "__init__.py"
    )


def assert_true(condition, message):
    """Fail loudly when a demo's core claim does not hold."""
    if not condition:
        raise AssertionError(f"Demo evidence check failed: {message}")
    print(f"  [verified] {message}")


def colab_note():
    """Identify the runtime so instructors know which environment produced the output."""
    runtime = "Google Colab" if "google.colab" in sys.modules or os.path.isdir("/content") else "local machine"
    print(f"Runtime: {runtime} | Python {sys.version_info.major}.{sys.version_info.minor}")
