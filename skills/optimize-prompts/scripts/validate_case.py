#!/usr/bin/env python3
"""Validate a POA case JSON using only the Python standard library.

This checks structural and selected governance invariants. It is deliberately
not a factual, safety, domain-applicability, or empirical-performance validator.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_KEYS = {
    "schema_version",
    "case_id",
    "status",
    "original_prompt",
    "optimization_target",
    "intent",
    "requirements",
    "invariants",
    "assumptions",
    "conflicts",
    "decision_points",
    "evidence_claims",
    "enforcement_allocations",
    "candidate_prompts",
    "validation_results",
    "limitations",
}

ARRAY_KEYS = {
    "requirements",
    "invariants",
    "assumptions",
    "conflicts",
    "decision_points",
    "evidence_claims",
    "enforcement_allocations",
    "candidate_prompts",
    "validation_results",
    "limitations",
}

STATUSES = {
    "RECEIVED",
    "INTERPRETED",
    "AUDITED",
    "NEEDS_USER_DECISION",
    "NEEDS_DOMAIN_REVIEW",
    "NOT_A_PROMPT_PROBLEM",
    "READY_TO_COMPILE",
    "COMPILED",
    "STATICALLY_CHECKED",
    "EMPIRICALLY_TESTED",
    "CONDITIONALLY_APPROVED",
    "APPROVED",
    "REJECTED",
    "EXPIRED",
}

ASSURANCE_LEVELS = {
    "S0_REWRITTEN",
    "S1_STATICALLY_IMPROVED",
    "S2_EVALUATOR_PREFERRED",
    "S3_BENCHMARK_IMPROVED",
    "S4_PRODUCTION_VALIDATED",
    "INCONCLUSIVE",
    "REJECTED",
}

MATERIAL_IMPACTS = {"S3", "S4"}
AUTHORIZED = {"approved", "authorized", "not_required"}


def add_error(errors: list[str], location: str, message: str) -> None:
    errors.append(f"{location}: {message}")


def validate(case: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(case, dict):
        return (["$: root must be a JSON object"], warnings)

    missing = sorted(REQUIRED_KEYS - case.keys())
    for key in missing:
        add_error(errors, "$", f"missing required key {key!r}")

    if case.get("schema_version") != "1.0":
        add_error(errors, "$.schema_version", "must equal '1.0'")

    if not isinstance(case.get("case_id"), str) or not case.get("case_id", "").strip():
        add_error(errors, "$.case_id", "must be a non-empty string")

    if not isinstance(case.get("original_prompt"), str) or not case.get("original_prompt", "").strip():
        add_error(errors, "$.original_prompt", "must be a non-empty string")

    if case.get("status") not in STATUSES:
        add_error(errors, "$.status", "contains an unsupported status")

    target = case.get("optimization_target")
    if not isinstance(target, dict) or not isinstance(target.get("type"), str):
        add_error(errors, "$.optimization_target", "must be an object with a string 'type'")

    if not isinstance(case.get("intent"), dict):
        add_error(errors, "$.intent", "must be an object")

    for key in ARRAY_KEYS:
        if key in case and not isinstance(case[key], list):
            add_error(errors, f"$.{key}", "must be an array")

    decisions = case.get("decision_points", [])
    pending_material = set()
    if isinstance(decisions, list):
        for index, decision in enumerate(decisions):
            location = f"$.decision_points[{index}]"
            if not isinstance(decision, dict):
                add_error(errors, location, "must be an object")
                continue
            if decision.get("material") is True and decision.get("authorization_status") not in AUTHORIZED:
                decision_id = str(decision.get("id", index))
                pending_material.add(decision_id)

    candidates = case.get("candidate_prompts", [])
    if isinstance(candidates, list):
        for c_index, candidate in enumerate(candidates):
            c_location = f"$.candidate_prompts[{c_index}]"
            if not isinstance(candidate, dict):
                add_error(errors, c_location, "must be an object")
                continue
            changes = candidate.get("semantic_changes", [])
            if not isinstance(changes, list):
                add_error(errors, f"{c_location}.semantic_changes", "must be an array")
                continue
            for ch_index, change in enumerate(changes):
                location = f"{c_location}.semantic_changes[{ch_index}]"
                if not isinstance(change, dict):
                    add_error(errors, location, "must be an object")
                    continue
                if change.get("impact") in MATERIAL_IMPACTS and change.get("authorization_status") not in AUTHORIZED:
                    add_error(errors, location, "S3/S4 change lacks recorded authorization")

    if pending_material and case.get("status") in {
        "READY_TO_COMPILE",
        "COMPILED",
        "STATICALLY_CHECKED",
        "EMPIRICALLY_TESTED",
        "CONDITIONALLY_APPROVED",
        "APPROVED",
    }:
        add_error(
            errors,
            "$.status",
            "cannot advance while material decisions are pending: " + ", ".join(sorted(pending_material)),
        )

    validations = case.get("validation_results", [])
    if isinstance(validations, list):
        for index, result in enumerate(validations):
            location = f"$.validation_results[{index}]"
            if not isinstance(result, dict):
                add_error(errors, location, "must be an object")
                continue
            level = result.get("assurance_level")
            if level is not None and level not in ASSURANCE_LEVELS:
                add_error(errors, f"{location}.assurance_level", "contains an unsupported assurance level")
            if level in {"S3_BENCHMARK_IMPROVED", "S4_PRODUCTION_VALIDATED"}:
                if not result.get("empirical_evidence"):
                    add_error(errors, location, f"{level} requires empirical_evidence")
            if level == "S4_PRODUCTION_VALIDATED" and not result.get("production_evidence"):
                add_error(errors, location, "S4_PRODUCTION_VALIDATED requires production_evidence")

    evidence = case.get("evidence_claims", [])
    if isinstance(evidence, list):
        for index, claim in enumerate(evidence):
            location = f"$.evidence_claims[{index}]"
            if not isinstance(claim, dict):
                add_error(errors, location, "must be an object")
                continue
            if claim.get("requirement_strength") == "mandatory" and claim.get("support_relation") not in {
                "direct_entailment",
                "user_explicit",
                "system_policy",
                "organization_policy",
            }:
                warnings.append(
                    f"{location}: mandatory requirement lacks direct or policy support"
                )

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Prompt Optimization Agent case JSON file.")
    parser.add_argument("case_file", type=Path)
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable results.")
    args = parser.parse_args()

    try:
        with args.case_file.open("r", encoding="utf-8") as handle:
            case = json.load(handle)
    except FileNotFoundError:
        print(f"error: file not found: {args.case_file}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON: {exc}", file=sys.stderr)
        return 2

    errors, warnings = validate(case)
    payload = {"valid": not errors, "errors": errors, "warnings": warnings}

    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for warning in warnings:
            print(f"WARNING: {warning}")
        for error in errors:
            print(f"ERROR: {error}")
        print("VALID" if not errors else "INVALID")

    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
