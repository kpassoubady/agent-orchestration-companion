# Lab 1.1 Reference Solution: Agent-Ready Work Plan

This directory contains one complete, valid work plan for the shipment-notification scenario. Use it to inspect the intended planning outcome, compare it with your own plan, or run the validator directly.

The lab produces a machine-checked execution plan. It does not implement or run the notification feature.

## Prerequisite

You need Python 3. The validator uses only the Python standard library, so no package installation is required.

## Run the Solution

From the companion repository root:

```bash
cd day1/lab1_1_agent-ready-work-plan/solution
python3 validate_plan.py task-plan.json
```

If you are already in this `solution` directory, run only the second command.

## Expected Result

The command should exit with status 0 and print:

```text
PLAN VALID
Wave 1: schema-contract
Wave 2: audit-recorder, email-renderer, preference-reader, sms-renderer
Wave 3: notification-integration
Human approval: A human architect approves the schema check before channel tasks enter Wave 2.
```

`PLAN VALID` means the plan satisfies the machine-checked contract: required fields are complete, task IDs are unique, dependencies are reachable and acyclic, files have exclusive owners, acceptance commands are supplied, and the required contract and integration gates are present.

## How to Read the Execution Waves

### Wave 1: Approve the Shared Contract

`schema-contract` is human-controlled because every downstream worker consumes the shipment-event schema. A human architect approves that contract before consumer work begins.

### Wave 2: Run Independent Work in Parallel

The email renderer, SMS renderer, preference reader, and audit recorder depend on the approved schema but own separate files. They can therefore proceed concurrently without creating file-ownership conflicts.

### Wave 3: Integrate Sequentially

`notification-integration` waits for all four consumer artifacts. One integration owner controls `router.py` and `tests/test_notifications.py`, then runs the notification and security acceptance checks.

The critical dependency path is:

```text
schema-contract -> parallel consumer tasks -> notification-integration
```

## Lab Outcomes

After completing or reviewing this solution, you should be able to:

1. Decompose a feature into bounded tasks with one observable deliverable each.
2. Identify a shared contract as an upstream decision and human-approval gate.
3. Separate parallel work by exclusive file ownership.
4. Express artifact dependencies as valid execution waves.
5. Reserve structural hub files for a single sequential integration owner.
6. Attach executable acceptance commands and explicit non-goals to every task.
7. Explain why technically independent work may still require a human-controlled checkpoint.

## What to Inspect

Open `task-plan.json` and verify that every task includes:

- a unique `id`;
- a bounded `objective` and `deliverable`;
- exclusively owned `files`;
- explicit `depends_on` relationships;
- a `parallel`, `sequential`, or `human-controlled` classification;
- one or more commands from `test-commands.md`;
- at least one concrete non-goal.

Also compare the plan with `feature-brief.md` and `repository-map.md`. Every required outcome is represented, `router.py` has one owner, and no platform infrastructure work has been invented.

## About the Acceptance Commands

The commands in `task-plan.json` are acceptance contracts for the later implementation tasks. This planning snapshot does not contain the production files or test modules, so do not run those `python3 -m unittest` commands from this directory. For this lab, `python3 validate_plan.py task-plan.json` is the executable completion check.

## Compare with Your Plan

The reference is one valid decomposition, not the only possible wording. Your objectives, deliverables, and non-goals may differ while still preserving the same boundaries and dependency structure. Use the validator first, then compare decisions such as file ownership, approval placement, parallelism, and integration sequencing.
