---
name: audit-problem-corpus
description: Use when scanning `problem/normal` for duplicate titles, sparse testcases, missing files, or uneven code coverage across many generated bundles before cleanup or migration work.
---

# Audit Problem Corpus

Use this skill for a broad health pass across the generated problem library. It is best before large
cleanup work, parser migrations, or reporting on corpus quality.

## Quick Start

- Default scan:
  `python .agents/skills/audit-problem-corpus/scripts/audit_problem_corpus.py problem/normal`
- Stricter testcase threshold:
  `python .agents/skills/audit-problem-corpus/scripts/audit_problem_corpus.py problem/normal --min-testcases 10`
- JSON output:
  `python .agents/skills/audit-problem-corpus/scripts/audit_problem_corpus.py problem/normal --json`

## Workflow

1. Run the audit across `problem/normal`.
2. Group the findings by issue type instead of fixing folders in random order.
3. If many folders share the same defect pattern, trace it back to prompt or parser behavior.
4. Use `$validate-problem-bundle` on any folder you are about to modify.

## What The Audit Highlights

- Missing required files
- Zero or low testcase coverage
- Empty code directories
- Duplicate metadata titles
- Folder-level issue counts that help prioritize cleanup

## Guardrails

- Report corpus-wide patterns before bulk rewriting legacy content.
- Keep audit output separate from repair work so the user can choose the cleanup scope.
- Treat this as structural triage, not proof that the generated algorithms are correct.

## References

- Read `references/health-signals.md` when you need triage rules.
