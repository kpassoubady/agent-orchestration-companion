# Solution Demo: Custom-Agent Feature Delivery

Use this directory when you want to demonstrate the lab with ready-made Claude Code agents and a known-good implementation. You can either inspect the completed result or reset the production files and replay the complete agent workflow.

## Prerequisites

Confirm the standard course tools are available:

```bash
git --version
python3 --version
claude --version
```

Run all commands from this `solution` directory unless a step says otherwise.

## Option 1: Run the Completed Result

Create a fresh demonstration workspace:

```bash
python3 setup_lab.py agent-lab-workspace-solution
cd agent-lab-workspace-solution
```

The setup script creates the original starter as the `lab-base` Git commit and then overlays the completed agent definitions and production implementation. This makes the final diff visible without modifying the course repository.

Inspect the supplied agents:

```bash
git diff --name-only lab-base
git ls-files --others --exclude-standard
python3 -m unittest
python3 verify_lab.py
```

Expected verification evidence:

```text
CUSTOM AGENT LAB VALID
Agents: story-planner -> feature-implementer -> acceptance-reviewer
Owned implementation: preferences.py, router.py
Full acceptance suite: passed
```

The changed-file list should contain:

```text
.claude/agents/acceptance-reviewer.md
.claude/agents/feature-implementer.md
.claude/agents/story-planner.md
preferences.py
router.py
```

## Demonstrate the Agents on the Completed Result

Start Claude Code from the generated workspace:

```bash
claude
```

### Run the planning agent

```text
Use the story-planner agent to read story.md, preferences.py, router.py,
tests/test_preferences.py, and tests/test_renderers.py. Reconstruct the bounded
implementation plan and map every acceptance criterion to the code and exact
verification commands. Do not edit anything.
```

Observe the visible delegation to `story-planner`. Its result should limit production ownership to `preferences.py` and `router.py` and treat tests as immutable.

### Run the acceptance reviewer

```text
Use the acceptance-reviewer agent to independently review the completed
implementation against story.md. Inspect git diff from lab-base, confirm file
ownership, run python3 -m unittest tests.test_preferences and python3 -m
unittest, and return PASS or FAIL for every acceptance criterion. Do not edit
any file. Distinguish executed evidence from assumptions.
```

Observe the separate delegation to `acceptance-reviewer`. It should report passing focused and full checks without changing files.

After the review, run:

```bash
git diff --name-only lab-base
git ls-files --others --exclude-standard
python3 verify_lab.py
```

The reviewer must not add or modify files, and the verifier must remain valid.

## Option 2: Replay the Full Lab with Ready-Made Agents

Use this path when you want to demonstrate planning, implementation, and review without spending time creating the three agent definitions.

If you already created the completed workspace above, leave Claude Code and reset only the two production files:

```bash
git restore --source lab-base -- preferences.py router.py
python3 -m unittest tests.test_renderers
python3 -m unittest tests.test_preferences
```

The renderer baseline should pass. Four preference tests should now fail. The three project agents remain under `.claude/agents/` and are ready to run.

Start Claude Code again:

```bash
claude
```

Follow the main lab beginning with [Invoke the Planning Agent](../README.md#3-invoke-the-planning-agent). Use these checkpoints:

1. Invoke `story-planner` and approve or revise its plan.
2. Invoke `feature-implementer` to change only `preferences.py` and `router.py`.
3. Inspect the production diff and confirm the tests remain unchanged.
4. Invoke `acceptance-reviewer` to run focused and full checks.
5. Run `python3 verify_lab.py` as the independent final gate.

A successful replay restores the completed implementation and prints `CUSTOM AGENT LAB VALID`.

## Suggested Instructor Narration

Before each delegation, ask learners to predict what the agent can do with its configured tools.

- `story-planner` can inspect evidence but cannot edit.
- `feature-implementer` can edit the two approved production files and run tests.
- `acceptance-reviewer` can execute checks but cannot repair its own findings.
- The human approves the plan and judges the diff before accepting completion.

After each result, distinguish the agent's claim from independently observable evidence such as the tool call, Git diff, test output, and verifier result.

## Reset and Repeat

Create a new workspace with a different target name when you want to repeat the demonstration:

```bash
python3 setup_lab.py another-agent-demo
```

The setup script refuses to overwrite an existing directory. This protects previous demonstration evidence.

## Full Learner Lab

For the complete 30-minute activity, including agent creation prompts, approval criteria, completion levels, and share-out instructions, use the [main lab guide](../README.md).
