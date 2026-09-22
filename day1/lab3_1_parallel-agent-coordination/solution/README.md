# Lab 3.1 Reference Solution: Parallel Agent Coordination

This directory can generate a complete, runnable reference repository for the parallel-agent coordination lab. The generated repository contains real worker branches, implementation and handoff commits, integration merges, a human-approval record, a resolved conflict-practice branch, and executable verification evidence.

Use this reference to inspect the intended orchestration outcome or compare it with your own lab workspace. The setup script completes the workflow automatically; it is not a replacement for practicing the steps in `../start`.

## Prerequisites

You need:

- Python 3;
- Git;
- a terminal that can run standard Git commands.

The project uses only the Python standard library. No package installation is required.

## Generate the Reference Workspace

From the companion repository root:

```bash
cd day1/lab3_1_parallel-agent-coordination/solution
python3 setup_lab.py lab-workspace-solution
```

The target directory must not already exist. If `lab-workspace-solution` exists, choose a different target name rather than overwriting it.

The setup command creates a new Git repository and prints output similar to:

```text
Created /absolute/path/to/lab-workspace-solution
Base commit: <generated-short-commit>
Fixture branches: fixture/conflict-email, fixture/conflict-sms
Worker branches: agent/email, agent/sms
Conflict-practice branch: conflict-practice
```

The absolute path and base commit vary between runs.

## Run the Completed Solution

Enter the generated repository and run both completion checks:

```bash
cd lab-workspace-solution
python3 -m unittest
python3 verify_record.py
```

The test suite should report six passing tests:

```text
......
----------------------------------------------------------------------
Ran 6 tests in <time>s

OK
```

The orchestration verifier should exit with status 0 and print:

```text
ORCHESTRATION RECORD VALID
Merge order: agent/email -> agent/sms
Human checkpoint: approved before second merge
Combined and security checks: passed
```

`ORCHESTRATION RECORD VALID` means more than the renderer tests passed. The verifier also confirms that the recorded commits exist, branch changes respect ownership, both handoffs share the same base, implementation commits are integrated into `main`, the schema is unchanged, approval occurred before the second merge, and the conflict-practice branch preserves the approved channel order.

## What the Setup Script Builds

The generated history represents the completed coordination workflow:

1. `lab-base` marks the shared starting commit.
2. `agent/email` implements only the email renderer and records a separate email handoff.
3. `agent/sms` implements only the SMS renderer and records a separate SMS handoff.
4. `main` merges email first, records the human checkpoint, then merges SMS.
5. The combined and security checks run after integration.
6. `conflict-practice` contains both fixture branches and the resolved router conflict.
7. `main` records the final integration evidence without merging the disposable conflict-practice branch.

The worker branches remain available after setup so you can inspect their boundaries and evidence.

## Inspect the Git Evidence

From the generated repository, run:

```bash
git branch --list
git log --graph --oneline --decorate --all
git diff --name-only lab-base..agent/email
git diff --name-only lab-base..agent/sms
git show conflict-practice:router.py
```

The email branch should differ from `lab-base` only in `channels/email.py` and `handoffs/email.json`. The SMS branch should differ only in `channels/sms.py` and `handoffs/sms.json`. The router shown from `conflict-practice` should preserve:

```python
CHANNEL_ORDER = ("email", "sms")
```

## Inspect the Durable Handoffs

Open `handoffs/email.json` and `handoffs/sms.json` in the generated repository. Each handoff should contain:

- the correct task and base commit;
- a real implementation commit;
- an exact changed-file inventory;
- the supplied focused verification command and a passing status;
- implementation decisions and remaining risks;
- the next human checkpoint.

The implementation commit is intentionally separate from the handoff commit. This allows a reviewer to prove that the implementation commit changed exactly one owned renderer file before trusting the handoff evidence.

## Inspect the Integration Record

Open `integration-record.json` and confirm that it records:

- the worker-to-workspace assignments;
- the merge order `agent/email` then `agent/sms`;
- human approval before the second merge;
- the evidence reviewed at that checkpoint;
- passing combined and security checks;
- the router conflict decision and the fact that `conflict-practice` was not merged into `main`.

The verifier reruns recorded checks and examines Git ancestry. Editing the JSON without creating the required commits and branches would not produce a valid result.

## Lab Outcomes

After completing or reviewing this solution, you should be able to:

1. Isolate parallel agent tasks with branches, worktrees, and exclusive file ownership.
2. Give each agent a bounded prompt with explicit non-goals and focused acceptance checks.
3. Produce a durable handoff backed by real commits and reproducible test evidence.
4. Review branch diffs and handoffs before trusting an agent's completion claim.
5. Insert a human approval point between integration steps.
6. Merge parallel work in a deliberate order and rerun combined security checks.
7. Resolve a prepared conflict without weakening an approved shared contract.
8. Distinguish a clean merge from evidence that integrated behavior is correct.

## About the `project` Directory

Do not run `project/verify_record.py` directly from this solution directory. Files under `project` are templates used by `setup_lab.py`; their commit fields are populated while the generated Git history is created. Run verification from the generated `lab-workspace-solution` repository instead.

## Compare with Your Workspace

Your commit hashes and handoff wording will differ from the reference. Compare the structural evidence rather than literal hashes: owned files, focused checks, separate implementation and handoff commits, merge order, approval timing, unchanged schema, conflict resolution, and final verifier result.
