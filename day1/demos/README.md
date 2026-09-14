# Day 1 Demos (Practical)

These demos run real operations against the real notification service in
[`lab-workspace-solution/`](../../lab-workspace-solution/): actual Git commits,
actual `git diff` output, and actual `unittest` runs. Each demo copies that
codebase into a temporary directory first, so nothing in your checkout changes.

Every demo ends with `[verified]` evidence checks. If a claim stops holding, the
demo fails loudly instead of printing a takeaway that is no longer true.

For notebook versions of these demos, see
[`../demos-notebook/`](../demos-notebook/). For the print-only concept demos,
see [`../demos-conceptual/`](../demos-conceptual/).

| File | Topic | Goal | Run |
| :--- | :--- | :--- | :--- |
| `demo-boundary-from-imports.py` | 1 | Derive file ownership and execution waves from the parsed import graph | `python3 day1/demos/demo-boundary-from-imports.py` |
| `demo-routing-signals-measured.py` | 2 | Compute blast radius, test cover, and reversibility from the repository | `python3 day1/demos/demo-routing-signals-measured.py` |
| `demo-escalation-from-failure.py` | 2 | Derive a routing decision from a genuinely failing security test | `python3 day1/demos/demo-escalation-from-failure.py` |
| `demo-integration-gate-real-diff.py` | 3 | Block a green commit whose real diff left its task-card boundary | `python3 day1/demos/demo-integration-gate-real-diff.py` |
| `demo-two-session-orchestration.py` | 3 | Run two worktree sessions through handoff, ordered merge, and conflict resolution | `python3 day1/demos/demo-two-session-orchestration.py` |
| `demo-handoff-summary-nokey.py` | 3 (optional) | Generate the handoff summary field from a real diff with a local model | `python3 day1/demos/demo-handoff-summary-nokey.py` |

`demo_support.py` is a shared helper module, not a demo. It locates the
substrate, builds the temporary Git sandbox, and runs test targets.

## Requirements

Python 3.9 or newer and Git. No API key, no network, and no installs for the
first five demos.

The optional `demo-handoff-summary-nokey.py` uses the local model
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
