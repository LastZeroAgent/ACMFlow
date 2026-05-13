# [ACMFlow](https://github.com/LastZeroAgent/ACMFlow) Agent Guide

## Scope

This repository turns a natural-language algorithm prompt into a saved ACM-style problem bundle.
The only root-level Python entry point is `main.py`; production implementation lives under
`src/create_problem_api/`.

## Core Working Rules

- Treat `config.ini` as secret-bearing. Do not print, rotate, or rewrite API credentials unless the
  user explicitly asks for that work.
- Prefer local parser validation before any live model call. Prompt work should usually be verified
  with `python tests/parser_smoke.py` or a focused `process_problem()` smoke test first.
- Keep the prompt contract and parser contract aligned. Any structural change to
  `[prompt].format_instruction` in `config.ini` should be reviewed against
  `src/create_problem_api/problem_helper.py` in the same change.
- Generated bundles under `problem/normal/` are user data. Make narrow edits there and avoid bulk
  rewrites unless the user explicitly requests a migration or cleanup pass.
- Preserve the public endpoint spelling `/promblemserve` unless the user explicitly asks to rename
  the API surface.
- Keep root-level files thin. New production logic belongs in `src/create_problem_api/`, test code
  in `tests/`, reusable scripts in `scripts/`, and engineering notes in `docs/`.

## Key Files

- `main.py`: root entrypoint for local API startup.
- `src/create_problem_api/api.py`: FastAPI app and request flow.
- `src/create_problem_api/model_adapter.py`: model adapter and Spark client setup.
- `src/create_problem_api/problem_helper.py`: markdown parsing, file generation, metadata, code extraction, testcase output.
- `src/create_problem_api/pairwise.py`: pairwise execution and MCP tool implementation.
- `tests/parser_smoke.py`: parser-oriented local smoke test.
- `tests/test_pairwise.py`: pairwise smoke test.
- `scripts/`: reusable demos and report generation scripts.
- `docs/HARNESS_ENGINEERING.md`: repository layout and harness rules.
- `front/ProblemHelper.html`: standalone frontend page.
- `problem/normal/`: generated problem corpus.

## Output Contract

The normal output shape is:

- `problem/normal/<title>/problem.md`
- `problem/normal/<title>/solution.md`
- `problem/normal/<title>/metadata.json`
- `problem/normal/<title>/code/solution.*`
- `problem/normal/<title>/testcases/<n>.in` and `<n>.out`

If you change how the model emits headings, code fences, or testcase blocks, update the parser and
then validate the saved bundle shape.

## Common Commands

- `python main.py`
- `python tests/parser_smoke.py`
- `python tests/test_pairwise.py`
- `python scripts/pairwise_quick_demo.py`
- `python .agents/skills/validate-problem-bundle/scripts/validate_problem_bundle.py problem/normal`
- `python .agents/skills/audit-problem-corpus/scripts/audit_problem_corpus.py problem/normal`

## Project Skills

Repository-local skills live in `.agents/skills/`:

- `tune-problem-prompt`
- `validate-problem-bundle`
- `audit-problem-corpus`

Use them when the task is about prompt formatting, bundle validation, or corpus cleanup.
