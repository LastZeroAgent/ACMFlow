---
name: validate-problem-bundle
description: Use when validating a generated problem folder under `problem/normal`, checking parser output after `ProblemHelper.py` changes, or confirming that one saved bundle is structurally complete before you trust it.
---

# Validate Problem Bundle

This skill gives you a deterministic structural check before or after parser changes. Use the script
first, then inspect the flagged files.

## Quick Start

- Single bundle:
  `python .agents/skills/validate-problem-bundle/scripts/validate_problem_bundle.py problem/normal/<title>`
- Whole corpus with a stricter testcase floor:
  `python .agents/skills/validate-problem-bundle/scripts/validate_problem_bundle.py problem/normal --min-testcases 10`
- JSON output for tooling:
  `python .agents/skills/validate-problem-bundle/scripts/validate_problem_bundle.py problem/normal --json`

## Workflow

1. Run the validator on the target folder or corpus root.
2. Fix hard structural failures first: missing files, invalid JSON, empty code directories, and
   unmatched testcase pairs.
3. Review warnings such as title mismatches or missing section markers.
4. If a broken bundle came from prompt or parser work, fix the source of generation before
   hand-editing many generated files.

## What The Script Checks

- Required files and directories
- Valid `metadata.json`
- Problem title and metadata title presence
- At least one code file in `code/`
- Matching numbered `.in` and `.out` testcase pairs
- Minimum testcase count

## Guardrails

- The validator is structural, not an algorithmic correctness proof.
- Legacy corpus folders may have warnings that are useful to report before large cleanup work.
- If the user only asked for one bundle, keep the repair scope local to that folder.

## References

- Read `references/checklist.md` for the manual follow-up checklist.
