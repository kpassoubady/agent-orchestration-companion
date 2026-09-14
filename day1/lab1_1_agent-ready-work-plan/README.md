# Lab 1.1: Agent-Ready Work Plan

## Scenario

A retail platform must add shipment notifications through email and short messages while preserving customer preferences and an audit record. The shared event schema and notification router are structural hubs. Your group will create a dependency-aware execution plan, not implement the notification system.

## Goal

Complete a machine-checked `task-plan.json` that gives each task a bounded deliverable, explicit ownership, dependencies, acceptance commands, non-goals, and an execution classification.

## Time Budget

| Time | Activity |
| :--- | :--- |
| 0-3 min | Read privately and mark the likely contract gate and hub files. |
| 3-8 min | Compare observations and assign a driver and navigator. |
| 8-18 min | Complete task cards and dependencies in `task-plan.json`. |
| 18-24 min | Run the validator and repair the smallest failing fields. |
| 24-27 min | Review classifications and record the human approval point. |
| 27-30 min | Prepare a 60-second evidence-based share-out. |

Rotate the driver after the first validator run.

## Start

```bash
cd day1/lab1_1_agent-ready-work-plan/start
python3 validate_plan.py task-plan.json
```

The starter must fail. Read the reported contract violations before editing the plan.

## Supplied Context

Read `feature-brief.md`, `repository-map.md`, and `test-commands.md`. You may change only `task-plan.json`. Do not weaken or modify `validate_plan.py`.

## Planning Task

1. Define at least five tasks with one observable deliverable each.
2. Establish the shipment-event schema as an upstream decision gate.
3. Give every file one owner and reserve the central router for integration.
4. Classify each task as `parallel`, `sequential`, or `human-controlled`.
5. Attach one or more supplied acceptance commands to every task.
6. Record a human approval point before integration begins.

## Bounded Claude Code Prompt

```text
Read feature-brief.md, repository-map.md, test-commands.md, task-plan.json,
and validate_plan.py. Propose changes only to task-plan.json. Create bounded
work items with exclusive file ownership, explicit artifact dependencies,
non-goals, supplied acceptance commands, and parallel, sequential, or
human-controlled classifications. Keep schema approval upstream of channel
work and reserve router.py for one integration owner. Do not change the
validator or invent implementation details. Run python3 validate_plan.py
task-plan.json and explain how the plan satisfies each reported rule.
```

Review the proposal before applying it. Reject any plan that assigns a shared hub file to several agents or starts consumers before the schema gate.

## Completion Levels

- Basic: The validator passes with five complete task cards and no ownership conflict.
- Intermediate: The dependency graph exposes contract, parallel, and integration waves with a clear critical path.
- Stretch: Add a customer-preference task without creating a shared-file conflict or circular dependency.

## Definition of Done

`python3 validate_plan.py task-plan.json` exits with status 0 and prints the execution waves. The group can identify the contract gate, the integration owner, one rejected parallelization choice, and the recorded human approval point.

## Share-Out

Show the validator result. Name one task your group kept sequential or human-controlled, the strongest alternative you rejected, and the evidence that supported the decision.

If blocked, inspect the validator message, compare it with the repository map, ask another group for one hint, and only then consult `../solution/task-plan.json`.
