# Orchestrating Multiple Agent Sessions
Reference for coordinating parallel Claude Code work through isolated worktrees, durable handoffs, ordered integration, and verification gates.

---

## Isolation and Coordination

A Git worktree gives a session its own working directory, index, and branch while sharing repository history. Uncommitted edits in one worktree do not appear in another. This prevents accidental filesystem interference, but it does not prevent two branches from making incompatible assumptions or changing the same logical contract.

Every workspace assignment should record the base commit, branch, path, task identifier, allowed files, prohibited shared files, dependency state, and focused verification command. Start all parallel tasks from the same approved base.

## Choosing a Claude Code Approach

Current Claude Code versions provide several parallel execution surfaces. The stable planning decision is who coordinates and how workers exchange evidence.

| Approach | Coordinator | Best fit |
| :--- | :--- | :--- |
| **Subagents** | Main session | Focused side tasks whose results return to one caller |
| **Agent view** | Human | Independent sessions that a person monitors and redirects |
| **Agent teams** | Lead agent | Experimental collaborative work with direct messaging |
| **Dynamic workflows** | Script | Repeatable, large, multi-pass orchestration |

Agent teams are experimental and do not automatically give every teammate a worktree. Explicit file ownership remains necessary. A manual Git worktree workflow is a portable fallback across product changes.

## Durable Handoffs

A completion message should identify the task, base commit, resulting commit, changed files, decisions, focused checks, unresolved risks, and next dependency checkpoint. This evidence lets an integration owner review work without replaying the complete conversation.

Progress states should describe events such as ready, running, blocked, ready for review, accepted, and integrated. A blocked task names the missing artifact or failed command. A ready-for-review task names a commit and supplies check output.

## Integration

Merge in dependency order rather than finish order. Inspect one handoff, merge one branch, run its focused check, and then decide whether to accept the next branch. Run the full suite and security checks against the combined state.

A clean Git merge proves only that lines did not conflict. It does not prove behavioral compatibility. A textual conflict is a signal to restore contract ownership and involve the integration owner. The person or integration agent resolving it must preserve the approved schema and rerun all gates.

## Enterprise Practice

Production teams often run agents in ephemeral cloud workspaces and submit short-lived pull requests. Trunk-based development, protected branches, continuous integration, security scanning, and merge queues turn the same local controls into enforced policy. GitOps adds auditable, reviewable changes for operational configuration.

The lab uses local worktrees and standard-library tests to remove network and dependency-installation delays. The control pattern remains applicable to hosted workspaces: isolate, claim scope, attach evidence, review, merge in order, and verify the combined result.

## Common Pitfalls

Separate directories do not guarantee independent work. Common failures include dirty or different base commits, overlapping router or schema ownership, missing handoff evidence, and integration in completion order. Teams also run focused checks on each branch but skip the combined suite. Preserve one integration owner and one human approval point before accepting the second worker.
