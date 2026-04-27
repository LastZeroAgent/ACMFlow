---
name: tune-problem-prompt
description: Use when editing `config.ini` prompt templates, changing the markdown response format expected by `/promblemserve`, or debugging why model output no longer parses cleanly in `ProblemHelper.py` or `test.py`.
---

# Tune Problem Prompt

Keep the LLM output format and the parser expectations aligned. This skill is for structural prompt
work, not for general copy polishing.

## When To Use It

- You are editing `[prompt].system_prompt` or `[prompt].format_instruction` in `config.ini`
- You want to change headings, code fences, testcase formatting, or saved bundle structure
- A change in prompt wording caused `ProblemHelper.py` or `test.py` to stop parsing reliably

## Workflow

1. Read `config.ini`, `main.py`, `ProblemHelper.py`, and `test.py` to see the current contract.
2. Load `references/parser-contract.md` before changing headings, fenced blocks, or testcase syntax.
3. Prefer the smallest contract-preserving change that solves the issue.
4. If you change a structural token, update the parser in the same change.
5. Validate locally with `python test.py` or a focused `process_problem()` smoke test before any
   live Spark request.

## Guardrails

- Treat `config.ini` as secret-bearing and do not expose credentials.
- Prefer `format_instruction` edits for shape changes and `system_prompt` edits for behavior/tone.
- Keep the existing `/promblemserve` route spelling unless the user explicitly wants an API rename.
- Avoid using live LLM output as the first validation step when a local parser test can catch the
  same failure faster.

## References

- Read `references/parser-contract.md` before changing prompt structure.
