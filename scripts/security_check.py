#!/usr/bin/env python3
"""Run deterministic public-release checks for this repository.

The scanner is intentionally conservative and dependency-free. Passing does
not prove that the plugin, prompts, or model outputs are secure.
"""

from __future__ import annotations

import json
import os
import py_compile
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
MAX_FILE_SIZE = 1_000_000
REQUIRED_FILES = {
    "README.md",
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    ".codex-plugin/plugin.json",
    "skills/optimize-prompts/SKILL.md",
}
ALLOWED_EXECUTABLES = {
    "scripts/security_check.py",
    "skills/optimize-prompts/scripts/validate_case.py",
}
FORBIDDEN_PATH_FRAGMENTS = (
    "/" + "Users/",
    "C:" + "\\Users\\",
    ".codex/plugins/" + "cache",
)
SECRET_PATTERNS = {
    "GitHub token": re.compile(r"gh" + r"[pousr]_[A-Za-z0-9]{20,}"),
    "GitHub fine-grained token": re.compile(r"github_" + r"pat_[A-Za-z0-9_]{20,}"),
    "OpenAI-style secret": re.compile(r"sk" + r"-[A-Za-z0-9_-]{20,}"),
    "AWS access key": re.compile(r"AK" + r"IA[0-9A-Z]{16}"),
    "Google API key": re.compile(r"AI" + r"za[0-9A-Za-z_-]{30,}"),
    "Slack token": re.compile(r"xo" + r"x[baprs]-[A-Za-z0-9-]{10,}"),
    "Private key": re.compile(r"BEGIN " + r"(?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY"),
}


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [ROOT / item.decode() for item in result.stdout.split(b"\0") if item]


def scan_bytes(label: str, data: bytes, errors: list[str]) -> None:
    text = data.decode("utf-8", errors="ignore")
    for name, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            errors.append(f"{label}: possible {name}")
    for fragment in FORBIDDEN_PATH_FRAGMENTS:
        if fragment in text:
            errors.append(f"{label}: contains local path fragment {fragment!r}")


def scan_history(errors: list[str]) -> None:
    revisions = subprocess.run(
        ["git", "rev-list", "--all"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.split()
    for revision in revisions:
        listing = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", revision],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        for relative in listing:
            if relative == str(SELF.relative_to(ROOT)):
                continue
            blob = subprocess.run(
                ["git", "show", f"{revision}:{relative}"],
                cwd=ROOT,
                capture_output=True,
            )
            if blob.returncode == 0 and len(blob.stdout) <= MAX_FILE_SIZE:
                scan_bytes(f"history {revision[:12]}:{relative}", blob.stdout, errors)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    tracked = tracked_files()
    relative_names = {str(path.relative_to(ROOT)) for path in tracked}

    for required in sorted(REQUIRED_FILES - relative_names):
        errors.append(f"missing required file: {required}")

    for path in tracked:
        relative = str(path.relative_to(ROOT))
        if path.is_symlink():
            errors.append(f"tracked symbolic link: {relative}")
            continue
        if not path.is_file():
            continue
        size = path.stat().st_size
        if size > MAX_FILE_SIZE:
            errors.append(f"unexpectedly large tracked file: {relative} ({size} bytes)")
            continue
        data = path.read_bytes()
        if path.resolve() != SELF:
            scan_bytes(relative, data, errors)
        if os.access(path, os.X_OK) and relative not in ALLOWED_EXECUTABLES:
            errors.append(f"unexpected executable file: {relative}")
        if path.suffix == ".json":
            try:
                json.loads(data)
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                errors.append(f"invalid JSON {relative}: {exc}")
        if path.suffix == ".py":
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as exc:
                errors.append(f"Python compilation failed for {relative}: {exc.msg}")

    scan_history(errors)

    if not revisions_exist():
        warnings.append("repository has no committed revision to scan")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print("PUBLIC-RELEASE CHECKS PASSED" if not errors else "PUBLIC-RELEASE CHECKS FAILED")
    return 0 if not errors else 1


def revisions_exist() -> bool:
    return subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


if __name__ == "__main__":
    raise SystemExit(main())
