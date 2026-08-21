# POA Protocol

Use this protocol for cross-domain, high-risk, current-standard-dependent, or materially ambiguous prompts.

## 1. Establish the task boundary

Identify the optimization target:

- user prompt;
- system instruction;
- reusable template;
- tool contract;
- evaluator prompt;
- retrieval policy;
- agent workflow;
- full application specification.

Record the target runtime when known: model/version, system-instruction support, tools, browsing, structured output, context limits, permissions, and interaction mode.

Do not assume a natural-language prompt is the correct enforcement layer.

## 2. Build a candidate task specification

Extract:

- primary goal and supporting goals;
- requester, executor, audience, and approver;
- required, optional, provided, and missing inputs;
- deliverable and output contract;
- hard constraints, soft constraints, exclusions, and priorities;
- success criteria and unacceptable failures;
- external-knowledge and freshness requirements;
- assumptions and unresolved questions.

Attach one epistemic status to each important field:

| Status | Meaning |
|---|---|
| `explicit` | Directly stated by the user |
| `entailed` | Reliably follows from supplied context |
| `proposed` | Suggested by POA |
| `assumed` | Temporary working assumption |
| `unknown` | Not established |

Require evidence text for `explicit` and `entailed`. Do not fill unknown fields merely to complete a schema.

## 3. Diagnose the problem type

Return all applicable categories:

| Category | Meaning |
|---|---|
| `PROMPT_PROBLEM` | Wording, structure, ambiguity, or missing contract |
| `REQUIREMENT_PROBLEM` | Goal or requirements are contradictory or defective |
| `KNOWLEDGE_PROBLEM` | Necessary facts or standards are unavailable |
| `CAPABILITY_PROBLEM` | Target runtime lacks a required capability |
| `PROCESS_PROBLEM` | Requires approval, tools, data, or organizational workflow |
| `EVALUATION_PROBLEM` | No trustworthy success measure is available |

Do not disguise a non-prompt problem with a longer prompt.

## 4. Route by domain, capability, and consequence

Identify all three:

1. domain context: primary, supporting, regulatory, and validation domains;
2. required capabilities: retrieval, calculation, causal inference, professional interpretation, personal-data processing, or external action;
3. failure modes: hallucination, staleness, jurisdiction mismatch, privacy leakage, discriminatory impact, or irreversible side effect.

Use these dimensions to decide whether external evidence or human review is required.

## 5. Resolve evidence claim by claim

For each important domain constraint, record:

- exact proposition;
- claim type and evidence role;
- publisher and original source;
- version and status;
- jurisdiction, subject, scenario, audience, and channel;
- valid time, task time, and retrieval time;
- support relation;
- omitted conditions and counterevidence;
- derived prompt requirement.

Prefer the source best qualified for the specific proposition. Do not use a single global source ranking.

Applicability states:

- `applicable`;
- `probably_applicable`;
- `contextual`;
- `not_applicable`;
- `unknown`.

If current information cannot be obtained, state the limitation and leave version-sensitive requirements conditional.

## 6. Detect decisions and conflicts

Classify conflicts as:

- logical;
- priority;
- evidence;
- jurisdiction;
- resource;
- value;
- runtime.

For each material decision, provide options, consequences, recommendation, basis, required decision owner, and authorization status.

Do not treat requester silence as authorization. Preserve a parameter or multiple candidates when confirmation is unavailable.

## 7. Allocate enforcement

Assign each requirement to the strongest appropriate layer:

| Requirement | Preferred layer |
|---|---|
| Style, emphasis, content coverage | Prompt |
| Fields and types | Schema |
| Arithmetic and deterministic rules | Code |
| Current facts | Retrieval or database |
| Access restrictions | Permission system |
| Step order and retries | Workflow/state machine |
| Irreversible decisions | Human approval |
| Professional judgment | Qualified review plus supporting prompt |

Report any requirement that remains prompt-only despite needing a stronger layer.

## 8. Compile candidates

Preserve confirmed invariants. Generate a compact candidate for the target runtime. Separate system instruction, user template, variables, reference context, output schema, and validation rules when the runtime supports them.

Use Pareto candidates when objectives conflict, such as:

- concise versus strict;
- exploratory versus deterministic;
- portable versus model-specific;
- low-cost versus high-assurance.

Do not manufacture a unique optimum when the objective weights are unknown.

## 9. Validate proportionally

Run checks in this order:

1. schema and variable validation;
2. invariant preservation;
3. constraint consistency;
4. evidence traceability;
5. runtime compatibility;
6. adversarial and boundary cases;
7. baseline comparison when execution is available;
8. production monitoring only after deployment.

For empirical comparison, hold model version, tools, retrieval context, sampling settings, inputs, and metrics constant. Report critical failures and worst cases, not only averages.

## 10. Stop honestly

Stop when the core evidenced intent is sufficiently established, blocking conflicts are resolved, material decisions are authorized or parameterized, required evidence meets the risk threshold, the runtime can execute the candidate, and additional work has low expected value.

Budget exhaustion is not success. Return a conditional candidate with unresolved items when necessary.
