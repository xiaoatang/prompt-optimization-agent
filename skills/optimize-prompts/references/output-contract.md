# POA Output Contract

## User-facing output

Keep the default response concise:

1. **Optimized prompt** — directly usable or explicitly parameterized.
2. **Key changes** — only changes that affect interpretation or execution.
3. **Assumptions and limitations** — especially unconfirmed domain rules and unavailable runtime capabilities.

Add audit, decision, evidence, enforcement, or validation sections only when they contain material information.

## Machine-readable case

Use `poa-case.schema.json` as the structural contract. Recommended top-level fields:

```json
{
  "schema_version": "1.0",
  "case_id": "case-001",
  "status": "COMPILED",
  "original_prompt": "...",
  "optimization_target": {},
  "intent": {},
  "requirements": [],
  "invariants": [],
  "assumptions": [],
  "conflicts": [],
  "decision_points": [],
  "evidence_claims": [],
  "enforcement_allocations": [],
  "candidate_prompts": [],
  "validation_results": [],
  "limitations": []
}
```

## Change record

For every semantic change, record:

```json
{
  "id": "CH-001",
  "type": "clarify",
  "impact": "S1",
  "before": "Write professionally",
  "after": "Write for product managers with basic statistical literacy",
  "basis": "proposed",
  "authorization_required": false,
  "authorization_status": "not_required"
}
```

Allowed change impacts:

- `S0`: wording or layout only;
- `S1`: makes evidenced meaning explicit;
- `S2`: adds a reversible, low-impact default;
- `S3`: changes scope, method, deliverable, or evaluation;
- `S4`: changes goals, rights, risk, compliance position, sensitive-data use, or irreversible action.

## Decision record

```json
{
  "id": "D-001",
  "material": true,
  "question": "Who is the audience?",
  "options": ["technical", "executive"],
  "recommendation": "executive",
  "decision_owner": "task_owner",
  "authorization_status": "pending"
}
```

## Validation language

Match the conclusion to evidence:

| Label | Permitted claim |
|---|---|
| `S0_REWRITTEN` | The prompt was rewritten |
| `S1_STATICALLY_IMPROVED` | Static checks found an improved specification |
| `S2_EVALUATOR_PREFERRED` | An isolated evaluator preferred the candidate |
| `S3_BENCHMARK_IMPROVED` | Comparable benchmark runs improved without guardrail regression |
| `S4_PRODUCTION_VALIDATED` | Repeated production evidence supports the improvement |
| `INCONCLUSIVE` | Available evidence cannot distinguish candidates reliably |
| `REJECTED` | The candidate violated a blocker or guardrail |

Never infer S2–S4 from textual self-review alone.
