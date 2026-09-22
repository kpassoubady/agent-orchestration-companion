# Agent Orchestration Companion

Student companion repository for **Orchestration Fundamentals for Agentic
Development**.

This repository contains the hands-on materials for two scheduled breakout
labs and instructor-selected optional practice. Learners create a
dependency-aware work plan, coordinate parallel Claude Code sessions through
isolated Git workspaces, and can create project-scoped specialist agents that
implement and review a real feature.

## Prerequisites

Learners should be comfortable using Claude Code or a similar AI coding
assistant, working with Git branches and merges, and running commands in a
terminal.

## Optional Hands-On Lab

Use the [Custom-Agent Feature Delivery lab][custom-agent-lab] when the class
wants direct practice creating and running Claude Code agents. Learners define
planner, implementer, and reviewer agents, deliver a bounded Python user story,
and verify the result with tests and Git evidence. It uses only the standard
course setup.

## Post-Course Extension

After the classroom session, use the optional [MVP Test Factory extension][test-factory]
to apply orchestration controls to a real testless application. The extension
bootstraps unit testing, coordinates parallel API/UI/k6 test authoring, and
reviews real execution evidence. It requires additional tools that are not part
of the classroom setup.

## Related Repositories

- [Course setup][setup] — complete the pre-class environment setup before using
  these labs

[custom-agent-lab]: day1/extensions/custom-agent-feature-delivery/README.md
[setup]: https://github.com/kpassoubady/agent-orchestration-setup
[test-factory]: day1/extensions/mvp-test-factory/README.md
