# Lab 1.1: Build an Agent-Ready Work Plan in Colab

## Objectives

By the end of this lab you will be able to:

1. Decompose a feature into bounded tasks with observable deliverables.
2. Establish a human-controlled contract gate before parallel consumer work.
3. Assign exclusive file ownership and reserve structural hubs for integration.
4. Validate dependencies, acceptance commands, non-goals, and execution waves.

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

1. Open `start/lab1_1_agent-ready-work-plan-colab.ipynb` in Google Colab or locally in Jupyter.
2. Run the setup, context, and starter-plan cells in order.
3. Find each `# TODO` comment and complete the task cards and approval point.
4. Run the validator after each meaningful change.
5. Finish when the acceptance cell prints `PLAN VALID` and three execution waves.

**Run command (local Jupyter):**

```bash
jupyter notebook start/lab1_1_agent-ready-work-plan-colab.ipynb
```

**Open in Colab:**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/agent-orchestration-companion/blob/main/day1/lab1_1_agent-ready-work-plan-colab/start/lab1_1_agent-ready-work-plan-colab.ipynb)

## Acceptance Check

The final validation cell must print:

```text
PLAN VALID
Wave 1: schema-contract
Wave 2: audit-recorder, email-renderer, preference-reader, sms-renderer
Wave 3: notification-integration
Human approval: A human architect approves the schema check before consumer tasks enter Wave 2.
```

The unmodified starter intentionally fails at the acceptance cell. This exposes missing contract, dependency, ownership, and verification details for you to repair.

## Getting Stuck?

The `solution/` directory contains a fully working reference notebook. Try each TODO on your own first, then compare your decisions with the solution. The reference is one valid decomposition; equivalent wording is acceptable when the validator passes and the same boundaries are preserved.
