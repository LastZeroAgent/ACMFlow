# Health Signals

Use the audit output to decide whether the next step is source repair, local repair, or just a report.

## Good Signals

- Each folder has the expected statement, solution, metadata, code, and testcase structure.
- Metadata titles are unique enough to identify a problem without ambiguity.
- Testcase counts are consistent with the current generation policy.

## Structural Smells

- Duplicate titles across folders
- Empty or missing testcase directories
- Empty code directories or only placeholder files
- Large pockets of bundles with the same failure pattern after a prompt or parser change

## Triage Strategy

1. Fix generator-level issues if the same defect appears across many folders.
2. Fix isolated bundle issues locally.
3. Leave legacy exceptions alone unless the user asks for normalization.
