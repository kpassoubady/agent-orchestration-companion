"""
Demo - Escalation Driven by a Real Test Failure
Day 1 - Session 1, Topic 2

Goal: Break the email renderer for real, capture the actual unittest failure,
and derive the routing decision from that captured evidence.

Nothing about the decision is pre-written. The demo edits `channels/email.py`
in a throwaway copy so untrusted input stops being escaped, runs the real
security test, and reads the genuine failure text. The routing rule is then
applied to measured facts: which test failed, how many modules the change can
reach, and whether a security assertion was involved. Repair the file, re-run,
and the same rule returns a different answer.

No API key needed. Pure Python standard library.

Run: python3 day1/demos/demo-escalation-from-failure.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from demo_support import (  # noqa: E402
    assert_true,
    colab_note,
    heading,
    run_tests,
    sandbox,
    show_evidence,
)

TARGET = Path("channels") / "email.py"
SECURITY_TEST = "tests.test_security.ChannelSecurityTest.test_email_escapes_untrusted_html"
FOCUSED_TEST = "tests.test_email"
REGRESSION = ('escape(str(event["customer_name"]))', 'str(event["customer_name"])')


def break_escaping(root):
    """Introduce a real regression: stop escaping the untrusted field."""
    path = root / TARGET
    source = path.read_text()
    path.write_text(source.replace(*REGRESSION))
    return path


def restore(path, original):
    """Put the approved implementation back."""
    path.write_text(original)


def first_assertion_line(output):
    """Pull the real assertion message out of the unittest output."""
    for line in output.splitlines():
        if line.startswith("AssertionError"):
            return line.strip()
    return "(no assertion line found)"


def failing_test_names(output):
    """Extract the actual test identifiers unittest reported as failures."""
    return re.findall(r"^(?:FAIL|ERROR): (\S+)", output, flags=re.MULTILINE)


def blast_radius(root, module_relative):
    """Count how many real modules import the changed module."""
    dotted = str(module_relative.with_suffix("")).replace("/", ".")
    importers = []
    for path in root.rglob("*.py"):
        if "__pycache__" in path.parts or path == root / module_relative:
            continue
        if dotted in path.read_text():
            importers.append(str(path.relative_to(root)))
    return sorted(importers)


def route(security_failed, importer_count, focused_failed):
    """Apply the routing rule to measured evidence only."""
    if security_failed:
        return (
            "STOP - human review",
            "A security assertion failed, so a stronger model is not the remedy.",
        )
    if importer_count >= 1 and focused_failed:
        return (
            "ESCALATE - stronger model, high effort",
            "The failure reaches other modules, so widen reasoning before retrying.",
        )
    if focused_failed:
        return (
            "KEEP - same model, narrowed scope",
            "The failure is local and reproducible, so inspect the smallest file set.",
        )
    return ("KEEP - no change needed", "Checks pass, so no routing change is justified.")


def main():
    colab_note()
    with sandbox(with_git=False) as (root, _):
        original = (root / TARGET).read_text()

        heading("Baseline: the approved implementation")
        security_ok, _ = run_tests(SECURITY_TEST, root)
        focused_ok, _ = run_tests(FOCUSED_TEST, root)
        show_evidence("security assertion", "passed" if security_ok else "FAILED")
        show_evidence("focused email tests", "passed" if focused_ok else "FAILED")

        heading("Inject a real regression")
        path = break_escaping(root)
        show_evidence("file edited", str(TARGET))
        show_evidence("change made", "removed escape() from the untrusted field")

        heading("Run the real tests and capture the genuine failure")
        security_ok, security_output = run_tests(SECURITY_TEST, root)
        focused_ok, _ = run_tests(FOCUSED_TEST, root)
        failures = failing_test_names(security_output)
        show_evidence("security assertion", "passed" if security_ok else "FAILED")
        show_evidence("focused email tests", "passed" if focused_ok else "FAILED")
        show_evidence("unittest reported", ", ".join(failures) or "(none)")
        show_evidence("actual assertion text", first_assertion_line(security_output))

        importers = blast_radius(root, TARGET)
        show_evidence("modules importing it", ", ".join(importers) or "(none)")

        heading("Routing decision derived from that evidence")
        decision, reason = route(not security_ok, len(importers), not focused_ok)
        show_evidence("decision", decision)
        show_evidence("because", reason)

        heading("Repair the file and re-apply the identical rule")
        restore(path, original)
        security_ok, _ = run_tests(SECURITY_TEST, root)
        focused_ok, _ = run_tests(FOCUSED_TEST, root)
        repaired, repaired_reason = route(not security_ok, len(importers), not focused_ok)
        show_evidence("security assertion", "passed" if security_ok else "FAILED")
        show_evidence("decision", repaired)
        show_evidence("because", repaired_reason)

        heading("Evidence checks")
        assert_true(failures, "unittest produced real failure identifiers")
        assert_true(
            "STOP" in decision, "a failing security assertion stopped execution for a human"
        )
        assert_true(
            decision != repaired, "the same rule changed answer when the evidence changed"
        )
        assert_true(
            "router.py" in " ".join(importers), "blast radius was measured from real imports"
        )

    print(
        "\nTakeaway: Escalate on captured evidence, not on repeated attempts,"
        "\nand stop for a human when the evidence is a security failure."
    )


if __name__ == "__main__":
    main()
