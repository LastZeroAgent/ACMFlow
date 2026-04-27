# Problem Corpus Guide

This subtree is generated content. Treat each problem directory as a bundle whose files should stay
consistent with one another.

## Bundle Rules

- Keep the folder name, `metadata.json` title, and `problem.md` top-level heading aligned when you
  intentionally rename a problem.
- Preserve numbered testcase pairs. If `7.in` exists, `7.out` should exist too.
- Avoid normalizing every legacy bundle in one pass unless the user asks for a corpus migration.
- When fixing a single bundle, prefer validating it first with:
  `python .agents/skills/validate-problem-bundle/scripts/validate_problem_bundle.py <folder>`

## Preferred Workflow

1. Audit first if the scope is unclear.
2. Fix structural gaps second.
3. Only then do content-level cleanup or title changes.

Use `.agents/skills/audit-problem-corpus` for broad scans and
`.agents/skills/validate-problem-bundle` for focused checks.
