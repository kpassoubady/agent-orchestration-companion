# Optional Lab: Custom-Agent Feature Delivery

Use your installed Claude Code to create three project-scoped specialist agents, run them as an evidence-gated delivery chain, and implement a real notification-preference user story.

This optional 30-minute lab is not part of the fixed four-hour schedule. An instructor may select it when learners want more direct practice creating and running agents for development work.

## Learning Objectives

After completing the lab, you will be able to:

- create reusable project agents under `.claude/agents/`;
- restrict planning and review agents to read-only tools;
- route planning, implementation, and acceptance review to different agents;
- approve a bounded plan before production files change;
- verify agent claims with tests and a Git-backed ownership check;
- explain when a specialized agent is preferable to another general prompt.

## Scenario

A retail notification service currently sends every shipment update through email and SMS. Implement the supplied user story so shoppers receive only their selected channels. The tests, renderer behavior, and standard-library-only constraint are fixed.

You will orchestrate this development chain:

```text
story-planner -> human approval -> feature-implementer -> acceptance-reviewer -> final verifier
```

## Time Budget

| Time | Activity |
| :--- | :--- |
| 0-4 min | Create the workspace and observe the intentional feature failures. |
| 4-10 min | Ask Claude to create three project agents and inspect their definitions. |
| 10-14 min | Invoke the planning agent and approve or revise its bounded plan. |
| 14-22 min | Invoke the implementation agent on the approved user story. |
| 22-27 min | Invoke the read-only reviewer and inspect its evidence. |
| 27-30 min | Run the independent verifier and share one orchestration decision. |

## Prerequisites

Use the Git, Python 3, and Claude Code installation from the course setup. Confirm Claude Code is available:

```bash
claude --version
```

This lab uses file-based project agents because that workflow works consistently across current Claude Code versions. The `.claude/agents/` directory already exists in the generated workspace so agents created during the session can be detected.

## 1. Create a Fresh Workspace

From this extension directory:

```bash
python3 start/setup_lab.py agent-lab-workspace
cd agent-lab-workspace
python3 -m unittest tests.test_renderers
python3 -m unittest tests.test_preferences
```

The renderer baseline must pass. The preference suite must fail four tests because the user story is not implemented. Do not change the tests.

Start Claude Code from `agent-lab-workspace`:

```bash
claude
```

## 2. Create the Project Agents

Give Claude this prompt:

```text
Create exactly three project-scoped Claude Code subagents under
.claude/agents/. Create only the agent definition files; do not change
production code, tests, or story.md.

1. story-planner: use Haiku with only Read, Glob, and Grep. It must analyze a
user story, acceptance tests, ownership, risks, and verification commands. It
must not edit files or report unexecuted checks as passing.
2. feature-implementer: use Sonnet with Read, Glob, Grep, Edit, and Bash. It
must implement only an approved bounded plan, preserve tests and dependencies,
run focused checks, and report changed files and actual results.
3. acceptance-reviewer: use Sonnet with only Read, Glob, Grep, and Bash. It
must independently inspect the diff, run focused and full checks, grade every
acceptance criterion, and never edit files.

Use the names story-planner, feature-implementer, and acceptance-reviewer in
the YAML frontmatter. Give each definition a specific description that tells
Claude when to delegate to it. After creating the files, summarize each
agent's model, tools, and prohibited actions.
```

Open the three generated files before continuing. Confirm that each contains YAML frontmatter followed by an operating prompt. Reject any definition that gives editing tools to the planner or reviewer, omits the model, or permits tests to be changed.

Run this check in another terminal or ask Claude to run it:

```bash
python3 verify_lab.py
```

It should still fail because the feature is incomplete, but it should no longer report missing or invalid agents.

## 3. Invoke the Planning Agent

Give the main Claude Code session this prompt:

```text
Use the story-planner agent to read story.md, preferences.py, router.py,
tests/test_preferences.py, and tests/test_renderers.py. Return a bounded plan
that maps every acceptance criterion to owned files and exact verification
commands. Do not edit anything. Stop after the plan so I can approve or revise
it.
```

Look for a visible delegation to `story-planner` in the transcript. Review the returned plan before approving it.

Approve only if the plan:

- limits production changes to `preferences.py` and `router.py`;
- treats tests as immutable;
- preserves renderer behavior and required-field validation;
- includes both `python3 -m unittest tests.test_preferences` and `python3 -m unittest`;
- handles absent, empty, invalid, single-channel, and reordered preferences.

If a condition is missing, ask the planner to revise the plan. Record one assumption you accepted or rejected.

## 4. Invoke the Implementation Agent

After approving the plan, give Claude this prompt:

```text
Use the feature-implementer agent to execute the approved plan for story.md.
Change only preferences.py and router.py. Do not modify tests, agent
definitions, dependencies, or renderer files. Run
python3 -m unittest tests.test_preferences and report the changed files plus
the real result. If the check fails, repair the smallest root cause within the
same ownership boundary.
```

Inspect the diff rather than accepting the summary alone:

```bash
git diff -- preferences.py router.py
git diff -- tests
```

The production diff should be bounded, and the tests diff should be empty.

## 5. Invoke the Acceptance Reviewer

Give Claude this prompt:

```text
Use the acceptance-reviewer agent to independently review the implementation
against story.md. Inspect git diff from lab-base, confirm file ownership, run
python3 -m unittest tests.test_preferences and python3 -m unittest, and return
PASS or FAIL for every acceptance criterion. Do not edit any file. Distinguish
executed evidence from assumptions.
```

Look for a separate delegation to `acceptance-reviewer`. If it reports a failure, send the exact failure back to `feature-implementer` and request the smallest correction. Run the reviewer again after any correction.

## 6. Run the Independent Gate

Exit Claude Code or use another terminal in the workspace:

```bash
python3 verify_lab.py
git diff --name-only lab-base
git ls-files --others --exclude-standard
```

Successful verification prints:

```text
CUSTOM AGENT LAB VALID
Agents: story-planner -> feature-implementer -> acceptance-reviewer
Owned implementation: preferences.py, router.py
Full acceptance suite: passed
```

The changed-file list must contain only the three agent definitions and the two owned production files.

## Human Review Checkpoints

Do not continue automatically at these points:

1. Agent-definition approval: confirm that tool access matches each role.
2. Plan approval: confirm scope, acceptance criteria, and commands before implementation.
3. Diff approval: confirm tests and unrelated files remain unchanged.
4. Evidence approval: trust executed commands and inspectable diffs, not an agent's completion claim.

## Completion Levels

- Basic: Create the three valid project agents and obtain an approved bounded plan.
- Intermediate: Implement the story through the specialist chain and pass `python3 verify_lab.py`.
- Stretch: Introduce one reversible defect in `preferences.py`, ask the reviewer to identify it, and route the exact failure back to the implementer before restoring a passing result.

## Definition of Done

- Three valid project agents exist under `.claude/agents/` with role-appropriate tool access.
- The transcript shows separate planner, implementer, and reviewer delegations.
- A human approved the plan before implementation.
- Only the allowed production and agent-definition files changed.
- The preference and full test suites pass.
- `python3 verify_lab.py` prints `CUSTOM AGENT LAB VALID`.
- You can explain one agent decision you rejected, revised, or verified independently.

## Share-Out

Show the three agent definitions, the final changed-file list, and the verifier result. Explain:

1. why the planner and reviewer are read-only;
2. what the human approval prevented;
3. which evidence proved the feature rather than merely claiming completion.

## Help Order

1. Read the exact failing test and `story.md`.
2. Check the agent's model and tools in `.claude/agents/`.
3. Confirm Claude visibly delegated to the named agent.
4. Inspect tracked changes with `git diff --name-only lab-base` and untracked files with `git ls-files --others --exclude-standard`.
5. Give the exact failure to the smallest relevant agent.
6. Compare your work with `solution/project/` only after attempting the evidence-driven repair.

Do not submit credentials, tokens, personal data, or Claude conversation exports. The lab uses only local dummy shipment data.
