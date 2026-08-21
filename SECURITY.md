# Security Policy

## Supported versions

Security fixes are provided for the latest released minor version.

| Version | Supported |
|---|---|
| 0.2.x | Yes |
| 0.1.x and earlier | No |

## Reporting a vulnerability

Do not disclose a suspected vulnerability in a public issue, discussion, pull request, or social-media post.

Use GitHub private vulnerability reporting for this repository:

https://github.com/xiaoatang/prompt-optimization-agent/security/advisories/new

If that page is unavailable, contact the repository owner through the GitHub profile before sending sensitive details. Include only the minimum information needed to establish a private reporting channel.

When reporting, include:

- affected version and file;
- impact and realistic attack scenario;
- reproduction steps or a minimal proof of concept;
- whether credentials, personal data, tool execution, or permission expansion are involved;
- any suggested mitigation.

Do not include real credentials, private prompts, customer data, or unnecessary personal information.

## Security scope

Security-relevant reports include:

- embedded prompt content overriding the Skill's control instructions;
- unintended tool execution or permission expansion;
- sensitive-data disclosure caused by repository code or instructions;
- bypasses of material-decision authorization checks;
- validator behavior that incorrectly accepts a prohibited state as valid;
- installation or update instructions that execute untrusted code unexpectedly.

Prompt quality disagreements, unsupported use cases, and ordinary model-output errors are normally not security vulnerabilities unless they cross a documented security boundary.

## Disclosure

Please allow maintainers a reasonable opportunity to investigate and publish a fix before public disclosure. No response-time or bounty commitment is currently offered.
