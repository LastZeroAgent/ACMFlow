# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

An AI-powered ACM problem generation service. It accepts a natural language prompt describing an
algorithm problem, sends it to the Xunfei Spark LLM with formatting instructions, parses the
structured markdown response, and saves the problem as a directory of files.

## Commands

```bash
python main.py
python tests/parser_smoke.py
python tests/test_pairwise.py
python scripts/pairwise_quick_demo.py
```

## Architecture

```text
User Prompt (HTTP GET /promblemserve?Prompt=...)
  -> main.py
  -> src/create_problem_api/api.py
  -> src/create_problem_api/model_adapter.py
  -> src/create_problem_api/problem_helper.py
  -> problem/normal/<title>/
```

## Core files

- `main.py` - root entrypoint that forwards to `src/create_problem_api/api.py`
- `src/create_problem_api/api.py` - FastAPI app, CORS, `/oneup`, `/promblemserve`
- `src/create_problem_api/model_adapter.py` - Spark adapter via the OpenAI-compatible client
- `src/create_problem_api/problem_helper.py` - parser and file-writing logic
- `src/create_problem_api/pairwise.py` - pairwise execution helpers and FastMCP registration
- `config.ini` - save-path, Spark, and prompt configuration; contains secrets
- `tests/parser_smoke.py` - parser smoke harness
- `tests/test_pairwise.py` - pairwise smoke harness
- `scripts/` - demos and report-generation scripts
- `docs/HARNESS_ENGINEERING.md` - repository layout and harness rules

## Output directory structure

```text
problem/normal/<title>/
├── problem.md
├── solution.md
├── metadata.json
├── code/
│   └── solution.*
└── testcases/
    ├── 1.in
    ├── 1.out
    └── ...
```
