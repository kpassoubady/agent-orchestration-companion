"""
Demo - Integration Gate Against a Real Diff
Day 1 - Session 1, Topic 3

Goal: Admit or block two real commits by comparing each task card's declared
file ownership with the actual `git diff --name-only` of that commit.

The blocked case is produced, not described. One simulated agent stays inside
its card and one also edits the shared router. Both commits pass their focused
tests, so the demo shows the gate catching a boundary violation that a green
test suite cannot see. Ownership comes from the real task-card files and the
changed paths come from Git.

No API key needed. Requires Git. Pure Python standard library.

Run: python3 day1/demos/demo-integration-gate-real-diff.py
"""

import re
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

OWNED_PATTERN = re.compile(r"^-\s+`([^`]+)`", flags=re.MULTILINE)
SMS_MAX = "MAX_LENGTH = 160"


def declared_ownership(root, card_name):
    """Read allowed files from the real task card instead of a literal."""
    card = (root / "task-cards" / card_name).read_text()
    owned = OWNED_PATTERN.findall(card)
    command = re.search(r"```bash\n(.+?)\n```", card, flags=re.DOTALL)
    return set(owned), (command.group(1).strip() if command else "")


def commit_compliant_change(root, base):
    """The email agent edits only what its card allows."""
    git("checkout", "-q", "-b", "agent/email", base, cwd=root)
    path = root / "channels" / "email.py"
    path.write_text(path.read_text().replace("your order shipped", "your order has shipped"))
    git("add", "-A", cwd=root)
    git("commit", "-q", "-m", "Refine email wording", cwd=root)
    return git("rev-parse", "--short", "HEAD", cwd=root)


def commit_overreaching_change(root, base):
    """The SMS agent edits its own file and also the shared router."""
    git("checkout", "-q", "-b", "agent/sms", base, cwd=root)
    sms = root / "channels" / "sms.py"
    sms.write_text(sms.read_text().replace(SMS_MAX, "MAX_LENGTH = 140"))
    router = root / "router.py"
    router.write_text(router.read_text().replace(
        'CHANNEL_ORDER = ("email", "sms")', 'CHANNEL_ORDER = ("sms", "email")'
    ))
    git("add", "-A", cwd=root)
    git("commit", "-q", "-m", "Shorten SMS and reorder channels", cwd=root)
    return git("rev-parse", "--short", "HEAD", cwd=root)


def changed_files(root, base, commit):
    """Ask Git which files the commit actually changed."""
    output = git("diff", "--name-only", f"{base}..{commit}", cwd=root)
    return set(output.splitlines()) if output else set()


def gate(root, base, commit, card_name):
    """Compare real changed files with the card's declared ownership."""
    owned, command = declared_ownership(root, card_name)
    actual = changed_files(root, base, commit)
    outside = actual - owned
    git("checkout", "-q", commit, cwd=root)  # test the commit under review
    passed, _ = run_tests(command.replace("python3 -m unittest ", ""), root) if command else (False, "")
    git("checkout", "-q", "main", cwd=root)
    return {
        "owned": owned,
        "actual": actual,
        "outside": outside,
        "tests_passed": passed,
        "command": command,
    }


def report(name, result):
    """Print the gate decision with its evidence."""
    heading(f"Gate: {name}")
    show_evidence("card allows", ", ".join(sorted(result["owned"])))
    show_evidence("git diff changed", ", ".join(sorted(result["actual"])))
    show_evidence("focused tests", "passed" if result["tests_passed"] else "FAILED")
    if result["outside"]:
        show_evidence("outside ownership", ", ".join(sorted(result["outside"])))
    decision = "ACCEPT" if result["tests_passed"] and not result["outside"] else "BLOCK"
    show_evidence("decision", decision)
    if decision == "BLOCK":
        reason = (
            "tests are green but the diff left the card's boundary"
            if result["tests_passed"]
            else "the focused acceptance command did not pass"
        )
        show_evidence("reason", reason)
    return decision


def main():
    colab_note()
    with sandbox() as (root, base):
        show_evidence("approved base commit", base)

        email_commit = commit_compliant_change(root, base)
        git("checkout", "-q", "main", cwd=root)
        sms_commit = commit_overreaching_change(root, base)
        git("checkout", "-q", "main", cwd=root)

        heading("Two real commits from two simulated agent sessions")
        show_evidence("agent/email commit", email_commit)
        show_evidence("agent/sms commit", sms_commit)

        email_result = gate(root, base, email_commit, "email.md")
        email_decision = report("agent/email", email_result)

        sms_result = gate(root, base, sms_commit, "sms.md")
        sms_decision = report("agent/sms", sms_result)

        heading("Evidence checks")
        assert_true(email_decision == "ACCEPT", "the compliant commit was admitted")
        assert_true(sms_decision == "BLOCK", "the overreaching commit was blocked")
        assert_true(
            sms_result["tests_passed"],
            "the blocked commit's own tests passed, so tests alone would have admitted it",
        )
        assert_true(
            "router.py" in sms_result["outside"],
            "Git reported the out-of-bounds file, it was not hardcoded",
        )

    print(
        "\nTakeaway: Gate on the real diff against declared ownership,"
        "\nbecause a passing test cannot detect a boundary violation."
    )


if __name__ == "__main__":
    main()
