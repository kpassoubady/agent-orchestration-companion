# Decomposing Complex Features for Multi-Agent Execution
Reference for turning a feature brief into bounded, verifiable tasks that agents can execute with limited coordination.

## Core Mechanism

Decomposition begins with an observable product outcome, a repository map, and the contracts that connect parts of the system. The planner identifies bounded contexts, structural hub files, shared schemas, and verification commands before assigning work. Each task then produces one named deliverable and owns a clear set of files.

A task is agent-ready when a capable agent can complete it without hidden conversational context and another person can verify the result from durable evidence. The specification must name required inputs, expected outputs, non-goals, dependencies, acceptance checks, and the handoff format.

## Boundaries and Contracts

Domain-driven design provides a useful boundary test. Work inside one bounded context usually needs less shared knowledge than work that crosses domain boundaries. Event-driven systems add a second test: event schemas and application programming interface contracts should be agreed before independent workers implement producers or consumers.

Shared routers, schemas, dependency manifests, and migrations are structural hubs. Assigning several agents to a hub at the same time creates both merge conflicts and semantic conflicts. Give the hub to one owner, establish it as an upstream gate, or reserve it for human-controlled integration.

## Execution Classification

| Classification | Suitable conditions | Required control |
| :--- | :--- | :--- |
| **Parallel** | Stable contract, separate files, independent checks | Exclusive ownership and a common handoff format |
| **Sequential** | A consumer needs an upstream artifact or decision | Named dependency and completion checkpoint |
| **Human-controlled** | Ambiguous, irreversible, security-sensitive, or high-blast-radius work | Explicit approval before execution or integration |
| **Not ready** | Hidden context, unclear outcome, or no verification path | Refine the brief before delegation |

Parallelism is an outcome of low coupling, not a planning target. A dependency graph makes the minimum sequential chain visible and prevents teams from starting consumers before contracts are stable.

## Acceptance and Evidence

Implementation steps describe activity, while acceptance criteria describe observable behavior. “Add an email renderer” is a task. “The supplied shipment fixture produces the expected subject and body when the renderer check runs” is an acceptance criterion. The task card should name the exact command and the evidence that must appear.

A useful handoff records changed files, decisions, verification results, unresolved risks, and the next dependency that is now unblocked. This artifact transfers the work without copying an entire chat transcript.

Independent checks should run in continuous integration before merge. Security-sensitive work also needs an automated gate for relevant risks such as broken access control and injection, followed by human review when the blast radius is high.

## Practical Example

A retail shipment-notification feature contains email, short-message, audit, preference, and routing concerns. Channel work can proceed in parallel only after the event schema is approved. The central router remains an integration task because every channel depends on it. A safe plan therefore establishes the schema gate, assigns channel-specific files, and gives the router and full test suite to one integration owner.

## Common Pitfalls

Weak plans split work by role or file count without checking coupling. They allow overlapping file ownership, omit non-goals, or present a checklist as proof of completion. They also maximize agent count even when coordination costs exceed useful parallel work. Reduce these failures by testing every task card for transferability, ownership, dependency clarity, and executable evidence.
