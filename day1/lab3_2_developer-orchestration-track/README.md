# Breakout Lab 3.2: Developer Orchestration Track

This lab provides an alternative to the Python-based orchestration track. Instead of writing custom orchestration scripts, you will use the `claude-helper` toolkit to orchestrate agents in a standard developer workflow. You will decompose tasks, define model strategies, and leverage parallel testing.

## Mission
Add a "Hair Salon Home Page with Username/Password Login Flow" to the existing `password-strength-checker` application.

## Prerequisites
- A local clone of [password-strength-checker](https://github.com/kpassoubady/password-strength-checker)
- `claude-helper` available in your workspace (provides `/dev-workflow` and `/mvp-test-factory` skills).

## The Developer Factory Chain
Before beginning, review the simplified orchestration architecture in `claude-helper/docs/developer-factory-chain.md`. This breaks down the workflow into Research, Specification, Parallel Builders, and Parallel Validation.

---

### Step 1: Research and Setup (Haiku Model)
Use your cheapest model (`haiku`) as per the `claude-credits/model-selection-strategy.md`. Have the agent map out the existing application:
1. Open a session in `password-strength-checker`.
2. Select the **Haiku** model.
3. Prompt: *"Map the current structure of this application. I want to add a new home page for a hair salon with a login form (username and password). Outline what folders and files will be affected."*

### Step 2: Establish the Contract
Create a simple specification file (`docs/hair-salon-spec.md`) that outlines:
- The API endpoints (e.g., `POST /api/login`)
- The UI components needed (e.g., `<LoginForm />`)

### Step 3: Implement Feature using `/dev-workflow` (Sonnet Model)
Switch to the **Sonnet** model. This is your mid-tier model for robust code generation.
1. Invoke the `/dev-workflow` command.
2. Direct the agent to build the backend logic for the login endpoint based on your contract.
3. In a separate branch (or worktree), use another Sonnet agent to build the UI frontend.
4. Merge both branches and start the server to visually verify the new Hair Salon login flow.

### Step 4: Validate in Parallel using `/mvp-test-factory`
With the feature built, we need tests. Instead of a single agent doing all the work, we will launch parallel validation agents.
1. Invoke `/mvp-test-factory /absolute/path/to/password-strength-checker`.
2. Follow the factory's proposal to spin up specialized agents for:
   - **API Testing**
   - **UI E2E Testing** (using Playwright)
   - **Performance Testing** (using k6)
3. Ensure these agents run concurrently and output their respective reports.

## Expected Outcomes
- A working hair salon login flow.
- A well-structured test suite produced by parallel agents.
- An understanding of how to assign the right model to the right task (`haiku` vs. `sonnet`).
