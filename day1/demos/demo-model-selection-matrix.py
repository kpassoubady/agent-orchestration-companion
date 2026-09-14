"""
Demo - Model Selection Matrix
Day 1 - Session 1, Topic 2

Goal: Compute dated model and effort recommendations from task evidence.

No API key needed. Pure Python standard library.

Run: python3 day1/demos/demo-model-selection-matrix.py
"""

RESEARCH_DATE = "2026-09-13"
TASKS = [
    {"name": "Update delivery copy", "complexity": 1, "uncertainty": 1, "blast_radius": 1, "verification_cost": 1, "reversible": True},
    {"name": "Add carrier mapping", "complexity": 2, "uncertainty": 1, "blast_radius": 2, "verification_cost": 1, "reversible": True},
    {"name": "Diagnose duplicate notifications", "complexity": 4, "uncertainty": 5, "blast_radius": 3, "verification_cost": 4, "reversible": True},
    {"name": "Change refund authorization", "complexity": 5, "uncertainty": 3, "blast_radius": 5, "verification_cost": 5, "reversible": False},
]


def recommend(task):
    score = sum(task[key] for key in ("complexity", "uncertainty", "blast_radius", "verification_cost"))
    if task["blast_radius"] >= 5 or not task["reversible"]:
        return score, "Claude Opus 5", "high", "required"
    if task["uncertainty"] >= 4 or score >= 14:
        return score, "Claude Opus 5", "high", "on escalation"
    if score >= 8:
        return score, "Claude Sonnet 5", "medium", "risk-based"
    return score, "Claude Haiku 4.5", "low", "not required"


def show_recommendations(tasks):
    print(f"Model-selection baseline researched {RESEARCH_DATE}")
    print("Model names are dated examples; task evidence is the durable rule.\n")
    for task in tasks:
        score, model, effort, approval = recommend(task)
        print(f"Task: {task['name']}")
        print(f"  evidence score: {score:>2} / 20")
        print(f"  initial route:  {model}, {effort} effort")
        print(f"  human approval: {approval}")


def main():
    show_recommendations(TASKS)
    print("Takeaway: Select model and effort from task evidence, then verify the outcome under controlled conditions.")


if __name__ == "__main__":
    main()
