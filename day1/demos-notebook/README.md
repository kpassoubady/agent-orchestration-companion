# Day 1 Demos (Notebooks)

Notebook versions of the practical demos in [`../demos/`](../demos/), for
running in Google Colab or Jupyter. Same real operations: real Git commits,
real `git diff` output, and real `unittest` runs against the notification
service in [`../../lab-workspace-solution/`](../../lab-workspace-solution/).

Each notebook splits its demo into numbered sections so you can pause between
cells and discuss the evidence before moving on. Every notebook ends with
`[verified]` evidence checks and an **Expected output** cell.

| Notebook | Topic | Goal | Colab |
| :--- | :--- | :--- | :--- |
| `demo-boundary-from-imports.ipynb` | 1 | Derive ownership and execution waves from the parsed import graph | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/agent-orchestration-companion/blob/main/day1/demos-notebook/demo-boundary-from-imports.ipynb) |
| `demo-routing-signals-measured.ipynb` | 2 | Compute blast radius, test cover, and reversibility from the repository | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/agent-orchestration-companion/blob/main/day1/demos-notebook/demo-routing-signals-measured.ipynb) |
| `demo-escalation-from-failure.ipynb` | 2 | Derive a routing decision from a genuinely failing security test | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/agent-orchestration-companion/blob/main/day1/demos-notebook/demo-escalation-from-failure.ipynb) |
| `demo-integration-gate-real-diff.ipynb` | 3 | Block a green commit whose real diff left its task-card boundary | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/agent-orchestration-companion/blob/main/day1/demos-notebook/demo-integration-gate-real-diff.ipynb) |
| `demo-two-session-orchestration.ipynb` | 3 | Run two worktree sessions through handoff, ordered merge, and conflict resolution | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/agent-orchestration-companion/blob/main/day1/demos-notebook/demo-two-session-orchestration.ipynb) |
| `demo-handoff-summary.ipynb` | 3 (optional) | Generate the handoff summary from a real diff with a local model | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/agent-orchestration-companion/blob/main/day1/demos-notebook/demo-handoff-summary.ipynb) |

## How the setup cell works

Cell 1 of every notebook locates the course files and puts `demo_support` on the
import path. On Colab nothing is present yet, so it clones this repository once;
locally it finds your existing checkout and clones nothing. It also reports the
resolved course root and the Git version, so you can confirm the environment
before the demo runs.

Colab has no global Git `user.name` or `user.email`. The demos set a local
identity on each temporary sandbox repository instead, so the real commits
succeed without any Colab-specific configuration.

## Requirements

Python 3.9 or newer and Git. No API key, no network beyond the initial clone,
and no installs for the first five notebooks.

The optional `demo-handoff-summary.ipynb` has a `%pip install` cell for
`transformers` and `torch`, used only to generate the handoff summary prose with
`google/flan-t5-base` (about a 1 GB download on first use). Skip that cell and
the notebook still completes, using a deterministic summary and recording
`summary_source` as `deterministic fallback`.

A small local model is weak. It is used here for description only, never for a
routing decision: the structural handoff fields stay measured from Git and
tests, and output that merely echoes the diff is rejected.

## Running locally

```bash
jupyter notebook day1/demos-notebook/demo-two-session-orchestration.ipynb
```

Nothing in your checkout changes. Each notebook copies the substrate into a
temporary directory and deletes it when the demo finishes.
