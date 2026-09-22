"""
Demo - Task Card Transfer Test
Day 1 - Session 1, Topic 1

Goal: Compute whether a task card contains enough durable context for independent execution.

No API key needed. Pure Python standard library.

Run: python3 day1/concepts/demos-conceptual/demo-task-card-transfer.py
"""

REQUIRED_FIELDS = {
    "objective",
    "deliverable",
    "context",
    "files",
    "dependencies",
    "acceptance",
    "non_goals",
    "handoff",
}
INCOMPLETE_CARD = {
    "objective": "Handle shipment email",
    "files": ["channels/email.py"],
    "acceptance": "Make sure it works",
}
TRANSFERABLE_CARD = {
    "objective": "Render email content from the approved shipment event.",
    "deliverable": "channels/email.py",
    "context": ["schemas/shipment-event.json", "tests/test_email.py"],
    "files": ["channels/email.py"],
    "dependencies": ["schema-contract approved"],
    "acceptance": "python3 -m unittest tests.test_email",
    "non_goals": ["Do not edit router.py", "Do not call a delivery vendor"],
    "handoff": ["changed files", "test result", "unresolved risks"],
}


def transfer_gaps(card):
    gaps = sorted(REQUIRED_FIELDS - card.keys())
    if card.get("acceptance") == "Make sure it works":
        gaps.append("executable acceptance command")
    return gaps


def show_card(name, card):
    gaps = transfer_gaps(card)
    print(f"\n{name}: {'NOT READY' if gaps else 'READY'}")
    for gap in gaps:
        print(f"  missing: {gap}")
    if not gaps:
        print(f"  command: {card['acceptance']}")
        print(f"  owned files: {', '.join(card['files'])}")


def main():
    print("Task-card transfer test")
    show_card("Conversational card", INCOMPLETE_CARD)
    show_card("Durable card", TRANSFERABLE_CARD)
    print("\nTakeaway: A transferable card replaces hidden conversation with scope, evidence, and handoff fields.")


if __name__ == "__main__":
    main()
