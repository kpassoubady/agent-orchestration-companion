# Optional Lab: Custom-Agent Feature Delivery in Colab

## Objectives

By the end of this lab you will be able to:

1. Define three specialist agent contracts with role-appropriate models and tools.
2. Establish a bounded delivery plan with explicit file ownership and immutable tests.
3. Preserve a human approval point before implementation begins.
4. Implement notification preferences against an executable acceptance contract.
5. Distinguish agent claims from independently executed verification evidence.

## Setup

No third-party packages or API keys are required. Google Colab can run the notebook as-is.

If you run the notebook locally, activate your Python environment first:

```bash
# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

See the [companion repository guide](../../../README.md) for course prerequisites.

## Instructions

1. Open `start/custom-agent-feature-delivery-colab.ipynb` in Google Colab or locally in Jupyter.
2. Run the context and validation cells in order to observe the incomplete contracts.
3. Complete every `# TODO` in the agent specifications, delivery plan, approval gate, and feature implementation.
4. Run the focused and full acceptance checks after each meaningful change.
5. Finish when the independent gate prints `CUSTOM AGENT COLAB LAB VALID`.

This Colab version machine-checks the artifacts and decisions behind the original Claude Code extension. It does not require a Claude account or invoke live agents. Use the source lab in `../custom-agent-feature-delivery/` when you want to run the same chain through installed Claude Code.

**Run command (local Jupyter):**

```bash
jupyter notebook start/custom-agent-feature-delivery-colab.ipynb
```

**Open in Colab:**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/agent-orchestration-companion/blob/main/day1/extensions/custom-agent-feature-delivery-colab/start/custom-agent-feature-delivery-colab.ipynb)

## Acceptance Check

The final validation cell must print:

```text
CUSTOM AGENT COLAB LAB VALID
Agents: story-planner -> feature-implementer -> acceptance-reviewer
Owned implementation: preferences.py, router.py
Human approval: recorded before implementation
Full acceptance suite: 9 tests passed
```

The unmodified starter intentionally reports invalid agent contracts, an unapproved plan, and failing feature tests. These failures are evidence to guide the repair.

## Getting Stuck?

The `solution/` directory contains a fully working reference notebook. Try each TODO first, then compare your decisions with the solution. The model assignments, tool boundaries, owned files, immutable tests, and acceptance commands are fixed by the lab contract.
