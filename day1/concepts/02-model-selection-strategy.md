# Model Selection Strategy for Agentic Development
Reference for choosing a model and effort level from task evidence, verification cost, risk, latency, and completed-task economics.

---

## Selection Is a Task Decision

Model selection starts with the task card and repository evidence. A localized reversible edit with a focused check has a different capability requirement from ambiguous debugging across services. Score the task's complexity, uncertainty, blast radius, verification cost, latency sensitivity, and reversibility before choosing a model.

The strongest model is not automatically the safest option. Safety comes from bounded permissions, acceptance checks, security gates, and human approval. Capability can reduce some errors, but it cannot authorize a destructive or security-sensitive change.

## Model and Effort

Model tier and effort are separate levers. The model establishes a capability, latency, and price profile. Effort controls how many response tokens the model can spend on text, thinking, and tool calls. A routine change may use a fast model at low or medium effort. Difficult repository reasoning may use a stronger model at high effort.

Current model names, availability, prices, and defaults change. Record the date and the fallback policy. Evaluate the models available to your organization instead of assuming every learner sees the same selector.

| Task shape | Initial strategy | Control |
| :--- | :--- | :--- |
| **Localized and reversible** | Efficiency-first model; low or medium effort | Focused check and scoped diff review |
| **Repository-wide but specified** | Balanced or strong model; high effort | Focused and regression checks |
| **Ambiguous debugging** | Capability-first exploration | Reproduction and falsified hypotheses |
| **High blast radius** | Strong model with human control | Security review, approval, and full checks |

## Cost per Completed Task

Per-token price does not measure engineering cost. A lower-cost attempt can become expensive after repeated searches, retries, review, and rework. Compare candidate configurations using pass rate, attempts, latency, tokens, review time, and total cost per accepted outcome.

Reduce waste before trading away capability. Prompt caching, concise context, and relevant repository instructions can lower cost without intentionally lowering quality. Then sweep effort or model tier against a representative evaluation set.

## Outcome-Based Evaluation

A model's completion message is not proof. Grade the repository outcome with deterministic checks where possible, use calibrated rubric graders for nuanced behavior, and retain human review for risk. Run multiple trials when behavior varies and keep prompts, tools, sandbox resources, and time limits consistent.

Infrastructure can change benchmark results. A comparison made with different memory, tools, or time budgets measures the complete harness, not only the model. Record these conditions with the result.

## Escalation

Escalation requires new evidence. Useful triggers include failure to reproduce, repeated failure on the same check, unexpected cross-module scope, missing context, or newly discovered security risk. Change one relevant lever: effort, model, context, task boundary, or human control.

An unchanged retry provides little information and can repeat the same failure. Stop when the trajectory contains no actionable signal and ask a human to refine the task or acceptance contract.

## Practical Scenario

An e-commerce queue contains copy editing, carrier mapping, duplicate-notification diagnosis, and refund-authorization work. The first tasks may be cheap to verify. Duplicate notifications add uncertainty and cross-service scope. Refund authorization has high blast radius and needs human approval regardless of model choice. A selection record should explain these differences and name the evidence that would trigger escalation.
