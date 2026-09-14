"""
Demo - Handoff Integration Gate
Day 1 - Session 1, Topic 3

Goal: Compute whether worker handoffs are safe to admit to integration.

No API key needed. Pure Python standard library.

Run: python3 day1/demos/demo-handoff-integration-gate.py
"""

EXPECTED_BASE = "8f31abc"
HANDOFFS = [
    {"task": "email", "base": EXPECTED_BASE, "files": ["channels/email.py"], "check": "passed", "risk": "none"},
    {"task": "sms", "base": EXPECTED_BASE, "files": ["channels/sms.py"], "check": "passed", "risk": "none"},
]
CONFLICTING_HANDOFF = {
    "task": "sms-broad-rewrite",
    "base": EXPECTED_BASE,
    "files": ["channels/sms.py", "router.py"],
    "check": "passed",
    "risk": "shared hub changed",
}
ALLOWED_FILES = {"email": {"channels/email.py"}, "sms": {"channels/sms.py"}}


def gate(handoff):
    errors = []
    if handoff["base"] != EXPECTED_BASE:
        errors.append("base commit differs")
    if handoff["check"] != "passed":
        errors.append("focused check did not pass")
    task_key = handoff["task"].split("-")[0]
    unexpected = set(handoff["files"]) - ALLOWED_FILES.get(task_key, set())
    if unexpected:
        errors.append(f"file ownership exceeded: {', '.join(sorted(unexpected))}")
    if handoff["risk"] != "none":
        errors.append(f"unresolved risk: {handoff['risk']}")
    return errors


def show_decision(handoff):
    errors = gate(handoff)
    print(f"{handoff['task']}: {'BLOCK' if errors else 'ACCEPT'}")
    for error in errors:
        print(f"  - {error}")


def main():
    print("Integration admission decisions")
    for handoff in HANDOFFS:
        show_decision(handoff)
    show_decision(CONFLICTING_HANDOFF)
    print("Takeaway: A passing test is insufficient when the handoff violates base, ownership, or risk gates.")


if __name__ == "__main__":
    main()
