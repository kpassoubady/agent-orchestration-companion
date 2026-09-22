# Lab 1.1 Starter: Build an Agent-Ready Work Plan

Use the supplied feature brief, repository map, acceptance commands, and validator to turn the incomplete `task-plan.json` into a dependency-aware execution plan. You are planning the work, not implementing the notification feature.

## Start Here

Run the validator before changing anything:

```bash
python3 validate_plan.py task-plan.json
```

The starter is intentionally invalid. Read every reported violation, then inspect these files:

1. `feature-brief.md` for the required work and approval point.
2. `repository-map.md` for file boundaries and structural hubs.
3. `test-commands.md` for the only allowed acceptance commands.
4. `validate_plan.py` for the machine-checked planning contract.
5. `task-plan.json` for the incomplete plan you may edit.

Change only `task-plan.json`. Do not modify the validator to make an incomplete plan pass.

## Progressive Hints

Use one hint at a time and rerun the validator after each meaningful change.

### Hint 1: Account for the complete feature

The feature brief names six distinct outcomes: the shared event contract, two channel renderers, preference lookup, audit recording, and final router integration. A bounded task should produce one observable deliverable.

### Hint 2: Put the contract gate first

Consumers cannot safely begin until the shared shipment-event contract is approved. The validator expects the contract task to use a specific ID and to be classified as human-controlled. The feature brief tells you what the human must approve.

### Hint 3: Remove overlapping ownership

The repository map identifies `router.py` as a structural hub. It should have one integration owner, not appear in both channel tasks. Each renderer should own only its channel-specific file.

### Hint 4: Express real artifact dependencies

The channel, preference, and audit tasks consume the approved event contract and can form a parallel execution wave after it. The router integration task must wait for the artifacts it combines.

### Hint 5: Make every task verifiable and bounded

Every task needs at least one acceptance command copied exactly from `test-commands.md` and at least one non-goal. A useful non-goal prevents scope expansion or forbids edits to another task's files.

### Hint 6: Check the required integration shape

The validator expects a task named `notification-integration` to own `router.py` and depend on at least three upstream tasks. The repository map shows the integration test file that can share that owner.

## Claude Code Prompt

From this `start` directory, give Claude Code the following prompt:

```text
Read README.md, feature-brief.md, repository-map.md, test-commands.md,
task-plan.json, and validate_plan.py. Solve this planning exercise by editing only
task-plan.json.

Create a bounded task for each outcome required by the feature brief. Give every
file exactly one owner, make schema approval an upstream human-controlled gate,
keep independent consumer work parallel after that gate, and reserve router.py
and its integration test for one sequential integration task. Use only supplied
acceptance commands. Give every task an observable objective and deliverable,
explicit artifact dependencies, and at least one concrete non-goal. Record an
observable human approval point before consumer work begins.

Do not modify validate_plan.py or any context file. Do not implement production
code or invent files, commands, or platform work outside the repository map.
Run python3 validate_plan.py task-plan.json, repair all reported violations, and
stop only when it exits successfully. Then summarize the execution waves, the
critical dependency path, file ownership, and the human approval point.
```

Review the resulting diff rather than accepting it automatically. Reject changes outside `task-plan.json`, overlapping file ownership, invented acceptance commands, circular dependencies, or consumers scheduled before schema approval.

## Verify Your Plan

```bash
python3 validate_plan.py task-plan.json
```

A successful result starts with `PLAN VALID`, prints the execution waves, and ends with the recorded human approval point. Confirm that:

- the schema contract is approved before its consumers begin;
- independent channel, preference, and audit tasks can run in parallel;
- the integration task runs only after its required artifacts are ready;
- every listed file has one owner;
- every task has acceptance evidence and a non-goal.

If you are still blocked after using the hints and reading the validator output, compare your plan with `../solution/task-plan.json`.
