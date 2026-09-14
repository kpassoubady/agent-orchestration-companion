# Lab 3.1: Parallel Agent Coordination

## Scenario

A retail platform has approved a shipment-event schema and a working in-memory router. Email and short-message renderers are incomplete. Your group will assign each renderer to an isolated Claude Code session, review durable handoffs, integrate both branches, and resolve a prepared router conflict.

## Goal

Finish the two channel workers in separate Git worktrees and produce an orchestration record backed by focused tests, full tests, a security check, commit evidence, and one human approval point.

## Time Budget

| Time | Activity |
| :--- | :--- |
| 0-3 min | Create the fresh repository and privately inspect both task cards. |
| 3-6 min | Assign driver, navigator, worktrees, branches, and file boundaries. |
| 6-15 min | Run two Claude Code sessions in parallel and collect handoffs. |
| 15-20 min | Review diffs, focused checks, commits, and schema preservation. |
| 20-25 min | Merge email, approve the checkpoint, merge SMS, and run all gates. |
| 25-28 min | Resolve the prepared conflict on a disposable practice branch. |
| 28-30 min | Complete the integration record and share one evidence-based decision. |

## Setup

From this lab directory, create a zero-dependency working repository:

```bash
python3 start/setup_lab.py lab-workspace
cd lab-workspace
python3 -m unittest
```

The initial suite should fail only for the two incomplete renderers. The setup script also creates `fixture/conflict-email` and `fixture/conflict-sms` branches.

## Create Isolated Workspaces

```bash
git worktree add ../work-email -b agent/email
git worktree add ../work-sms -b agent/sms
git worktree list
```

Open one terminal in each worktree. The driver owns the email session and the navigator owns the SMS session. Each person reviews the other session's handoff before integration.

## Email Session Prompt

```text
Read task-cards/email.md, schemas/shipment-event.json, channels/email.py,
tests/test_email.py, tests/test_security.py, and handoffs/email.json.
Implement only channels/email.py and complete handoffs/email.json. Preserve the
schema, router, tests, signatures, and standard-library-only constraint. Escape
untrusted HTML content. Run python3 -m unittest tests.test_email
 tests.test_security.ChannelSecurityTest.test_email_escapes_untrusted_html. Commit the implementation, record its commit and exact
check result in the handoff, then commit the handoff. Do not edit any other file.
```

## SMS Session Prompt

```text
Read task-cards/sms.md, schemas/shipment-event.json, channels/sms.py,
tests/test_sms.py, tests/test_security.py, and handoffs/sms.json. Implement only
channels/sms.py and complete handoffs/sms.json. Preserve the schema, router,
tests, signatures, 160-character limit, and standard-library-only constraint.
Normalize control whitespace. Run python3 -m unittest tests.test_sms
 tests.test_security.ChannelSecurityTest.test_sms_normalizes_control_whitespace. Commit the implementation, record its commit and exact
check result in the handoff, then commit the handoff. Do not edit any other file.
```

Review both diffs with `git diff lab-base..HEAD --stat` and inspect the handoff files. Reject unrelated changes, modified tests, schema edits, or unsupported completion claims.

## Integrate with a Human Checkpoint

Return to `lab-workspace` and merge in dependency order:

```bash
git merge --no-edit agent/email
python3 -m unittest tests.test_email tests.test_security.ChannelSecurityTest.test_email_escapes_untrusted_html
```

Before the second merge, a human reviewer must approve the email and SMS handoffs, changed-file boundaries, focused results, and unchanged schema. Record the approval in `integration-record.json`, then continue:

```bash
git merge --no-edit agent/sms
python3 -m unittest
```

Complete the workspace, merge-order, approval, full-check, and security-check fields in `integration-record.json`. Leave only `conflict_resolution` pending.

## Prepared Conflict

Create a disposable branch from the integrated state, merge both conflict fixtures, and resolve the conflict in `router.py` to preserve `CHANNEL_ORDER = ("email", "sms")`:

```bash
git switch -c conflict-practice
git merge --no-edit fixture/conflict-email
git merge --no-edit fixture/conflict-sms
git status --short
```

After resolving, run `git add router.py`, `git commit --no-edit`, and `python3 -m unittest`. Do not merge `conflict-practice` back into `main`. Switch back to `main`, record the conflict decision in `integration-record.json`, and run `python3 verify_record.py`.

## Completion Levels

- Basic: Two isolated worktrees produce passing focused checks and bounded diffs.
- Intermediate: Both branches integrate in order, all checks pass, and `verify_record.py` accepts the evidence.
- Stretch: The prepared conflict is resolved on `conflict-practice` with the full suite still passing.

## Definition of Done

The main branch contains both renderer commits, `python3 -m unittest` passes, `python3 verify_record.py` passes, the approved schema is unchanged, and the integration record names the merge order, approval point, full check, and conflict decision.

## Share-Out

Show one handoff and the combined test output. Explain one boundary you enforced, the evidence used before the second merge, and why a clean merge alone would not prove compatibility.

If blocked, read the exact failing test, inspect the smallest owned file, compare the handoff with its task card, ask another group for one hint, and only then inspect `solution/`.
