# Lab 3.1: Coordinate Parallel Agent Work in Colab

## Objectives

By the end of this lab you will be able to:

1. Separate email and short-message work with exclusive ownership boundaries.
2. Verify each worker with focused behavioral and security checks.
3. Create durable handoffs that connect implementation decisions to reproducible evidence.
4. Apply a human approval gate before integration and preserve an approved decision during conflict resolution.

## Setup

No third-party packages or API keys are required. Google Colab can run the notebook as-is.

If you run the notebook locally, activate your Python environment first:

```bash
# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

See the [companion repository guide](../../README.md) for course prerequisites.

## Instructions

1. Open `start/lab3_1_parallel-agent-coordination-colab.ipynb` in Google Colab or locally in Jupyter.
2. Run the scenario and validation cells in order.
3. Find each `# TODO` comment and complete both bounded worker implementations.
4. Run the focused checks, complete both handoffs, and review the evidence before approving integration.
5. Finish the integration record and conflict decision, then rerun the final acceptance cell.

**Run command (local Jupyter):**

```bash
jupyter notebook start/lab3_1_parallel-agent-coordination-colab.ipynb
```

**Open in Colab:**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/agent-orchestration-companion/blob/main/day1/lab3_1_parallel-agent-coordination-colab/start/lab3_1_parallel-agent-coordination-colab.ipynb)

## Colab Adaptation

The terminal version of this lab uses real Git worktrees, Claude Code sessions, commits, and merges. A Colab runtime is not an appropriate environment for coordinating multiple interactive Claude Code sessions, so this notebook models the same control points with isolated Python functions and machine-checked evidence records. Use the [terminal lab](../lab3_1_parallel-agent-coordination/README.md) when you need practice with real worktrees and Git history.

## Acceptance Check

The final validation cell must print:

```text
ORCHESTRATION RECORD VALID
Parallel tasks: email-renderer, sms-renderer
Human checkpoint: approved before integration
Merge order: agent/email -> agent/sms
Conflict decision: preserve email -> sms
Lab complete.
Takeaway: Parallel speed is trustworthy only when ownership, evidence, approval, and integration checks remain explicit.
```

The unmodified starter intentionally reports invalid orchestration evidence. Repair the smallest failing boundary or record, rerun the relevant focused check, and then rerun final validation.

## Getting Stuck?

The `solution/` directory contains a fully working reference notebook. Try each TODO on your own first, then compare your implementation and evidence with the solution. Equivalent implementation details are acceptable when all focused and final checks pass.
