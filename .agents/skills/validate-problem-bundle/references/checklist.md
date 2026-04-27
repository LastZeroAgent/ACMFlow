# Manual Checklist

Run the script first. Then use this checklist for the folders that still matter.

## Statement Files

- Does `problem.md` have a clear top-level title?
- Does it still include problem description, input, and output sections?
- Does `solution.md` read like analysis rather than duplicated statement text?

## Metadata

- Is `metadata.json` valid UTF-8 JSON?
- Does the `title` roughly match the folder name and `problem.md` title?
- Are time and memory limit fields present?

## Code And Cases

- Is there at least one implementation in `code/`?
- If multiple languages are expected, are the missing ones intentional?
- Do testcase numbers form complete `.in` and `.out` pairs?
- Are testcase files non-empty and reasonably varied?

## Triage Hint

If several folders fail in the same way after a prompt or parser edit, fix the generator path first.
