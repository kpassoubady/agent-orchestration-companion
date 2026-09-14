"""
Demo - Evidence-Based Escalation
Day 1 - Session 1, Topic 2

Goal: Show how execution evidence changes one routing decision without blind retries.

No API key needed. Pure Python standard library.

Run: python3 day1/demos/demo-evidence-based-escalation.py
"""

INITIAL_ROUTE = {"model": "Claude Sonnet 5", "effort": "high"}
TRAJECTORY = [
    {"signal": "focused_test_failed", "detail": "Duplicate event reproduced in notification router."},
    {"signal": "cross_service_scope", "detail": "Trace enters order events and customer preferences."},
    {"signal": "security_boundary", "detail": "Preference lookup affects customer authorization."},
]


def escalation_action(signal):
    actions = {
        "focused_test_failed": ("keep", "Use the exact failure to inspect the smallest relevant files."),
        "cross_service_scope": ("escalate", "Move to Claude Opus 5 at high effort for wider reasoning."),
        "security_boundary": ("human", "Pause for a human security and authorization review."),
    }
    return actions[signal]


def replay_trajectory(route, trajectory):
    print(f"Initial route: {route['model']}, {route['effort']} effort")
    for number, event in enumerate(trajectory, start=1):
        action, explanation = escalation_action(event["signal"])
        print(f"\nEvidence {number}: {event['detail']}")
        print(f"Decision: {action.upper()} - {explanation}")
        if action == "human":
            print("Execution stopped before another model attempt.")
            break


def main():
    replay_trajectory(INITIAL_ROUTE, TRAJECTORY)
    print("\nTakeaway: Escalate on actionable evidence, and stop when risk requires human control.")


if __name__ == "__main__":
    main()
