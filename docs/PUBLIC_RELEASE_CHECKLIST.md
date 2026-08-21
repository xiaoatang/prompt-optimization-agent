# Public Release Checklist

This checklist prevents a repository visibility change from being mistaken for a security review or a marketplace publication.

## Repository contents

- [x] README describes purpose, installation, usage, limitations, and validation levels.
- [x] Detectable `LICENSE` file matches the plugin manifest.
- [x] `SECURITY.md` defines supported versions and private reporting guidance.
- [x] `CONTRIBUTING.md` defines contribution and validation expectations.
- [x] Code of Conduct and structured issue templates are present.
- [x] Repository contains no personal marketplace file or installed Codex cache.
- [x] No tracked symbolic links or unexpectedly large files.
- [x] Runtime code has no third-party Python dependency.

## Security verification

- [x] Current tree scanned for common secret patterns and local absolute paths.
- [x] Git history scanned for common secret patterns.
- [x] JSON files parsed and Python files compiled.
- [x] Valid fixture accepted and invalid fixture rejected.
- [x] Codex Skill validator passed.
- [x] Codex plugin validator passed.
- [ ] GitHub private vulnerability reporting enabled after the repository becomes public.
- [ ] GitHub secret scanning and push protection settings reviewed after visibility change.
- [ ] Default branch protection or ruleset reviewed after visibility change.

## Distribution

- [x] Public Skill installation procedure documented.
- [x] README states that this repository is not yet a public marketplace catalog.
- [ ] Public Codex marketplace catalog or listing created, if plugin-store distribution is desired.
- [ ] Clean installation tested from the public repository after visibility change.

## Release

- [ ] Repository owner reviews the consequences of public visibility.
- [ ] Repository visibility changed explicitly by the owner.
- [ ] Security settings reviewed immediately after the change.
- [ ] Version tag and GitHub release created from the reviewed commit.

Do not mark the repository public merely because all automated checks pass. Public visibility makes the complete Git history available for reading and forking.
