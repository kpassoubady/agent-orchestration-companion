"""
Demo - Two Coordinated Sessions End to End
Day 1 - Session 1, Topic 3

Goal: Run two isolated worktree sessions through commit, handoff, dependency-
ordered merge, and a real acceptance gate, then resolve a genuine conflict.

This is the full orchestration loop with nothing simulated. Each session gets
its own Git worktree and branch, edits only the files its task card owns, runs
its own focused tests, and writes a handoff file recording its real commit and
real verification result. Integration merges in dependency order, runs the full
suite on the combined tree, and pauses at one human approval point. A third
branch then creates a true merge conflict on the shared router so the recorded
channel order decides the resolution.

No API key needed. Requires Git. Pure Python standard library.

Run: python3 day1/demos/demo-two-session-orchestration.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from demo_support import (  # noqa: E402
    assert_true,
    colab_note,
    git,
    heading,
    run_tests,
    sandbox,
    show_evidence,
)

SESSIONS = (
    {
        "name": "email",
        "branch": "agent/email",
        "file": Path("channels") / "email.py",
        "edit": ("your order shipped", "your order has shipped"),
        "tests": "tests.test_email",
    },
    {
        "name": "sms",
        "branch": "agent/sms",
        "file": Path("channels") / "sms.py",
        "edit": ("MAX_LENGTH = 160", "MAX_LENGTH = 150"),
        "tests": "tests.test_security.ChannelSecurityTest.test_sms_normalizes_control_whitespace",
    },
)
MERGE_ORDER = ("agent/email", "agent/sms")
APPROVED_ORDER = 'CHANNEL_ORDER = ("email", "sms")'


def open_session(root, base, session):
    """Create a real worktree and branch for one agent session."""
    worktree = root.parent / f"work-{session['name']}"
    git("worktree", "add", "-q", "-b", session["branch"], str(worktree), base, cwd=root)
    return worktree


def do_work(worktree, session):
    """Edit only the owned file, run the focused tests, and commit."""
    path = worktree / session["file"]
    path.write_text(path.read_text().replace(*session["edit"]))
    passed, _ = run_tests(session["tests"], worktree)
    git("add", "-A", cwd=worktree)
    git("commit", "-q", "-m", f"Complete {session['branch']}", cwd=worktree)
    commit = git("rev-parse", "--short", "HEAD", cwd=worktree)
    changed = git("diff", "--name-only", "HEAD~1..HEAD", cwd=worktree).splitlines()
    return passed, commit, changed


def write_handoff(worktree, session, base, commit, changed, passed):
    """Record real evidence in the handoff file the next session will read."""
    path = worktree / "handoffs" / f"{session['name']}.json"
    handoff = json.loads(path.read_text())
    handoff.update(
        {
            "base_commit": base,
            "implementation_commit": commit,
            "changed_files": sorted(changed),
            "verification": {
                "command": f"python3 -m unittest {session['tests']}",
                "status": "passed" if passed else "failed",
                "summary": "Focused acceptance command run inside the session worktree.",
            },
        }
    )
    path.write_text(json.dumps(handoff, indent=2) + "\n")
    git("add", "-A", cwd=worktree)
    git("commit", "-q", "-m", f"Record {session['name']} handoff", cwd=worktree)
    return handoff, git("rev-parse", "--short", "HEAD", cwd=worktree)


def main():
    colab_note()
    with sandbox() as (root, base):
        show_evidence("approved base commit", base)

        heading("Open two isolated sessions")
        worktrees, handoffs = {}, {}
        for session in SESSIONS:
            worktree = open_session(root, base, session)
            worktrees[session["name"]] = worktree
            show_evidence(f"{session['branch']} worktree", worktree.name)
        show_evidence("git worktree count", len(git("worktree", "list", cwd=root).splitlines()))

        heading("Each session works inside its own boundary")
        for session in SESSIONS:
            worktree = worktrees[session["name"]]
            passed, commit, changed = do_work(worktree, session)
            handoff, handoff_commit = write_handoff(
                worktree, session, base, commit, changed, passed
            )
            handoffs[session["name"]] = handoff
            show_evidence(f"{session['name']} commit", commit)
            show_evidence(f"{session['name']} changed", ", ".join(changed))
            show_evidence(f"{session['name']} focused test", "passed" if passed else "FAILED")
            show_evidence(f"{session['name']} handoff commit", handoff_commit)

        heading("Isolation proof before any merge")
        main_email = (root / "channels" / "email.py").read_text()
        show_evidence("main has email wording change", SESSIONS[0]["edit"][1] in main_email)
        show_evidence("main still at base", git("rev-parse", "--short", "HEAD", cwd=root) == base)

        heading("Integrate in dependency order with one approval point")
        for index, branch in enumerate(MERGE_ORDER, start=1):
            if index == 2:
                evidence_ok = all(
                    handoff["verification"]["status"] == "passed"
                    for handoff in handoffs.values()
                )
                show_evidence("human approval point", "review both handoffs before merge 2")
                show_evidence("handoff evidence complete", evidence_ok)
            git("merge", "-q", "--no-edit", branch, cwd=root)
            show_evidence(f"merge {index}", f"{branch} -> main")

        combined_ok, combined_output = run_tests("discover", root)
        ran = [line for line in combined_output.splitlines() if line.startswith("Ran ")]
        show_evidence("combined suite", "passed" if combined_ok else "FAILED")
        show_evidence("tests executed", ran[0] if ran else "(unknown)")

        heading("Resolve a real merge conflict on the shared router")
        # Build the conflict honestly: the practice branch and main each change
        # the same line of router.py, which is what Git needs to conflict.
        git("checkout", "-q", "-b", "conflict-practice", cwd=root)
        router = root / "router.py"
        router.write_text(router.read_text().replace(APPROVED_ORDER, 'CHANNEL_ORDER = ("sms", "email")'))
        git("commit", "-q", "-am", "Reorder channels on a practice branch", cwd=root)
        git("checkout", "-q", "main", cwd=root)
        router.write_text(
            router.read_text().replace(APPROVED_ORDER, f'{APPROVED_ORDER}  # order approved at integration')
        )
        git("commit", "-q", "-am", "Annotate the approved channel order", cwd=root)

        conflicted = git("merge", "conflict-practice", cwd=root, check=False)
        status = git("status", "--porcelain", cwd=root)
        show_evidence("merge exit", "conflict" if "UU" in status else "clean")
        show_evidence("git reported", [line for line in conflicted.splitlines() if "CONFLICT" in line])
        show_evidence("conflicted path", [line for line in status.splitlines() if line.startswith("UU")])

        git("checkout", "--ours", "router.py", cwd=root)
        git("add", "router.py", cwd=root)
        git("commit", "-q", "-m", "Keep approved channel order", cwd=root)
        final_order = APPROVED_ORDER in (root / "router.py").read_text()
        final_ok, _ = run_tests("discover", root)
        show_evidence("approved order preserved", final_order)
        show_evidence("suite after resolution", "passed" if final_ok else "FAILED")

        heading("Evidence checks")
        assert_true(
            SESSIONS[0]["edit"][1] not in main_email,
            "worktrees kept session edits out of main before merge",
        )
        assert_true(
            all(h["implementation_commit"] != h["base_commit"] for h in handoffs.values()),
            "each handoff recorded a real commit distinct from the base",
        )
        assert_true(combined_ok, "the full suite passed on the merged tree")
        assert_true("UU router.py" in status, "Git produced a genuine merge conflict")
        assert_true(final_order and final_ok, "resolution kept the approved order and stayed green")

        for session in SESSIONS:
            git("worktree", "remove", "--force", str(worktrees[session["name"]]), cwd=root)

    print(
        "\nTakeaway: Isolated worktrees, durable handoffs, ordered merges, and one"
        "\napproval point turn parallel sessions into a verifiable integration."
    )


if __name__ == "__main__":
    main()
