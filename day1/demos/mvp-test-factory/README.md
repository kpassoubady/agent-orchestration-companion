# Post-Course Extension: MVP Test Factory

This optional extension applies the course's decomposition, ownership, parallel execution, handoff, and evidence-gate practices to a common development problem: an MVP that works but has no automated tests.

This activity is not part of the four-hour classroom schedule. Complete it independently after the course.

## Learning Objectives

After completing the extension, you will be able to:

- distinguish shared test setup from work that can safely run in parallel
- establish a meaningful unit-test baseline before broader test generation
- bind API, UI, and performance agents to one approved test charter
- assign non-overlapping test ownership
- sequence functional and load evidence when workers share runtime resources
- reject skipped or self-reported evidence that did not come from a real command

## Reference Repositories

You will use:

- [Password Strength Checker][password-checker], a real Node.js/TypeScript MVP whose `main` branch intentionally starts without automated tests
- [Claude Helper][claude-helper], which provides the `/mvp-test-factory` skill and its specialist agents

Work in a fresh clone of the password checker. The orchestrator writes test infrastructure and tests into your local clone.

## Additional Prerequisites

The classroom setup is not sufficient for this optional extension. You also need:

- the Claude Helper `agents`, `skills`, and `docs` modules installed
- Grafana k6 installed using its [official instructions][k6-install]
- permission to install npm development dependencies and a Playwright browser
- a clean Git working tree

Verify the additional tool before starting:

```bash
k6 version
```

The orchestrator must stop before changing the project when k6 is unavailable.

## Activity Flow

### 1. Create an isolated learning copy

```bash
git clone https://github.com/kpassoubady/password-strength-checker.git
cd password-strength-checker
npm run install:server
npm start
```

In another terminal, verify the application:

```bash
curl -s http://localhost:3000/api/health
```

Stop the server after confirming readiness. Confirm `git status --short` is empty before invoking the factory.

### 2. Invoke the factory

```text
/mvp-test-factory /absolute/path/to/password-strength-checker
```

Do not approve the first proposal immediately. Check:

1. Which manifest, lockfile, configuration, and test paths have a single shared owner?
2. Which deterministic module was chosen for unit testing, and why?
3. Are API, UI, and performance paths exclusive?
4. Which real command will prove each layer works?
5. Does the plan prohibit production-source changes?

Revise the proposal if any ownership overlaps or a command is only assumed.

### 3. Observe the foundation gate

The bootstrap and unit stages run before parallel E2E authoring. Review the first passing smoke test and the meaningful evaluator cases. Confirm that they assert existing behavior instead of using placeholder assertions or chasing a percentage without regard to risk.

If a test exposes a likely product defect, preserve the evidence and keep the production fix outside this workflow.

### 4. Review the binding charter

At the next checkpoint, inspect the shared contract for:

- real API routes and HTTP 400 behavior
- stable UI labels and IDs
- debounce behavior
- fixed dummy passwords
- k6 profile and local thresholds
- allowed and prohibited files
- targeted commands and final gate order

All three workers must consume this exact approved artifact. A worker cannot derive a conflicting contract from another worker's unfinished output.

### 5. Observe parallel authoring

The API, UI, and performance agents may author test files concurrently because their write paths do not overlap. They should not run competing server and load processes during this wave.

Record one reason why parallel authoring is safe and one reason why fully parallel execution would be unsafe on this project.

### 6. Review the fan-in gates

The final runner should verify actual Git paths and execute:

```text
build/typecheck -> unit -> API E2E -> UI E2E -> k6
```

Confirm that k6 runs after functional tests. API, UI, and performance verdicts must remain separate even when the final summary contains an overall result.

### 7. Inspect the handoff

Use the final diff and evidence to answer:

1. Did every required command execute?
2. Did any worker change a file outside its ownership?
3. Do API and UI tests assert the same product behavior?
4. Are Playwright selectors stable and waits condition-based?
5. Does the k6 test check correctness as well as latency?
6. Are the thresholds described as local smoke safeguards rather than production capacity?
7. Would you retain these changes in a real MVP? What would you revise first?

## Completion Evidence

Keep these artifacts from your local run:

- approved framework and ownership proposal
- approved E2E test charter
- generated-test diff
- separate unit, API, UI, and k6 command results
- final quality-gate report
- one accepted decision and one rejected or revised assumption

Do not submit real passwords, credentials, tokens, browser profiles, or secrets. Use only the fixed dummy values approved in the charter.

## Transfer to Your Own MVP

Repeat the reasoning before repeating the command. Identify the deterministic unit seam, public API surface, stable browser contract, safe performance target, readiness mechanism, and shared runtime resources in your project. If the application needs production credentials, destructive test data, or remote load, create a dedicated test environment before using this workflow.

[claude-helper]: https://github.com/kpassoubady/claude-helper
[k6-install]: https://grafana.com/docs/k6/latest/set-up/install-k6/
[password-checker]: https://github.com/kpassoubady/password-strength-checker
