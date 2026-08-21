# Contributing

Thank you for improving Prompt Optimization Agent.

## Before opening an issue

- Search existing issues for duplicates.
- Do not post vulnerabilities or sensitive prompts publicly; follow `SECURITY.md`.
- Separate Prompt-quality requests from security-boundary failures.
- Include the Codex environment, plugin version, target prompt type, expected behavior, and observed behavior.

## Development workflow

1. Fork the repository and create a focused branch.
2. Keep `SKILL.md` concise; put detailed protocols and examples in `references/`.
3. Treat prompt samples, attachments, and retrieved content as untrusted data.
4. Do not add claims about current standards without a verifiable source and applicability conditions.
5. Do not raise an assurance label above the available validation evidence.
6. Add or update a valid and invalid fixture when changing governance rules.

Run before submitting:

```bash
python3 scripts/security_check.py
python3 skills/optimize-prompts/scripts/validate_case.py \
  skills/optimize-prompts/references/example-valid-case.json
```

The invalid fixture must fail:

```bash
python3 skills/optimize-prompts/scripts/validate_case.py \
  skills/optimize-prompts/references/example-invalid-case.json
```

If the Codex plugin and Skill validators are available locally, run them as well.

## Pull requests

- Keep each pull request focused.
- Explain the user-visible behavior change.
- Identify semantic-impact changes as S0–S4.
- List new assumptions, dependencies, permissions, or external-data flows.
- Include test evidence and remaining limitations.
- Do not commit credentials, personal marketplace configuration, installed plugin caches, or private evaluation data.

By contributing, you agree that your contribution is licensed under the repository's MIT License.
