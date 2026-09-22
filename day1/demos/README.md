# Day 1 Demos (Practical)

These demos run real operations against the real notification service in
[`lab-workspace-solution/`](../../lab-workspace-solution/): actual Git commits,
actual `git diff` output, and actual `unittest` runs. Each demo copies that
codebase into a temporary directory first, so nothing in your checkout changes.

Every demo ends with `[verified]` evidence checks. If a claim stops holding, the
demo fails loudly instead of printing a takeaway that is no longer true.

For notebook versions of these demos, see
[`../demos-notebook/`](../demos-notebook/). For the print-only concept demos,
see [`../concepts/demos-conceptual/`](../concepts/demos-conceptual/).

| File | Topic | Goal | Run |
| :--- | :--- | :--- | :--- |
| `demo-boundary-from-imports.py` | 1 | Derive file ownership and execution waves from the parsed import graph | `python3 day1/demos/demo-boundary-from-imports.py` |
| `demo-routing-signals-measured.py` | 2 | Compute blast radius, test cover, and reversibility from the repository | `python3 day1/demos/demo-routing-signals-measured.py` |
| `demo-escalation-from-failure.py` | 2 | Derive a routing decision from a genuinely failing security test | `python3 day1/demos/demo-escalation-from-failure.py` |
| `demo-integration-gate-real-diff.py` | 3 | Block a green commit whose real diff left its task-card boundary | `python3 day1/demos/demo-integration-gate-real-diff.py` |
| `demo-two-session-orchestration.py` | 3 | Run two worktree sessions through handoff, ordered merge, and conflict resolution | `python3 day1/demos/demo-two-session-orchestration.py` |
| `demo-handoff-summary.py` | 3 (optional) | Generate the handoff summary field from a real diff with a local model | `python3 day1/demos/demo-handoff-summary.py` |
| `interactive-shipment-notification-decomposition.html` | 1 (supplemental) | Explore runtime flow, the contract-first gate, bounded consumers, and single-owner integration | Open `day1/demos/interactive-shipment-notification-decomposition.html` in a browser |
| `interactive-model-selection.html` | 2 (supplemental) | Route tasks by evidence and risk, enforce human control, grade outcomes, and escalate with new evidence | Open `day1/demos/interactive-model-selection.html` in a browser |
| `interactive-multi-agent-coordination.html` | 3 (supplemental) | Compare four coordination surfaces and the workspace, handoff, and integration controls shared by all | Open `day1/demos/interactive-multi-agent-coordination.html` in a browser |
| `interactive-parallel-orchestration.html` | 3 (supplemental) | Explore isolated workers, evidence handoffs, ordered admission, combined gates, and repair | Open `day1/demos/interactive-parallel-orchestration.html` in a browser |

`demo_support.py` is a shared helper module, not a demo. It locates the
substrate, builds the temporary Git sandbox, and runs test targets.

## Interactive Diagrams

Open any HTML file directly in a modern browser. All four files are
self-contained and need no server, install, API key, or network connection.
Select nodes or relationships to inspect their upstream and downstream context.

- `interactive-shipment-notification-decomposition.html` uses guided views and
  a reader-controlled trace to connect runtime architecture to contract-first
  tasks, parallel consumer work, and single-owner router integration.
- `interactive-model-selection.html` shows evidence-based model and effort
  selection, mandatory human approval for high-risk work, outcome grading, and
  escalation that changes one lever only when new evidence exists.
- `interactive-multi-agent-coordination.html` compares Subagents, Agent view,
  agent teams, and dynamic workflows while showing the controls none replaces.
- `interactive-parallel-orchestration.html` includes chapter controls for the
  control path, parallel work, and repair loop, plus a reader-controlled trace.

The editable Archify sources are the matching `.workflow.json` or
`.architecture.json` files.

## Requirements

Python 3.9 or newer and Git. No API key, no network, and no installs for the
first five demos.

The optional `demo-handoff-summary.py` uses the local model
`google/flan-t5-base` when `transformers` and the cached model are both
present. When either is missing it prints why and falls back to a deterministic
summary, so the demo always completes. To enable the model path once:

```bash
pip install transformers torch
python3 -c "from transformers import AutoModelForSeq2SeqLM, AutoTokenizer; \
AutoTokenizer.from_pretrained('google/flan-t5-base'); \
AutoModelForSeq2SeqLM.from_pretrained('google/flan-t5-base')"
```

The first download is about 1 GB. Generation is greedy, so output is
deterministic on repeated runs.

## Running in Google Colab

Prefer the notebooks in [`../demos-notebook/`](../demos-notebook/), which carry
an "Open In Colab" badge and split each demo into numbered sections.

These scripts also run on Colab unchanged. They discover the course files by
walking up from the working directory and clone the companion repository when
the files are not present, and they set a local Git `user.name` and
`user.email` on the sandbox repository rather than relying on a global Git
config.

```python
!git clone -q https://github.com/kpassoubady/agent-orchestration-companion.git
%cd agent-orchestration-companion
!python3 day1/demos/demo-two-session-orchestration.py
```
