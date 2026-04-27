# Parser Contract

## Flow

1. `main.py` reads `system_prompt` and `format_instruction` from `config.ini`.
2. `/promblemserve` concatenates those prompt fragments with the user request.
3. `CheatAdapter.py` sends the composed prompt to Spark.
4. `ProblemHelper.py` parses the returned markdown and writes the problem bundle.

## What Must Stay Stable

- A recognizable top-level title for the problem.
- A problem statement section that can be turned into `problem.md`.
- Input and output sections that become the saved statement fields.
- Example or testcase material that can be converted into numbered `.in` and `.out` files.
- Solution analysis text plus fenced code blocks whose language labels map to output files.

## Saved Bundle Shape

The parser writes:

- `problem.md`
- `solution.md`
- `metadata.json`
- `code/solution.<ext>` and `solution_<n>.<ext>` for duplicate languages
- `testcases/<n>.in` and `testcases/<n>.out`

`metadata.json` is generated locally. It is not expected from the model output.

## High-Risk Prompt Changes

- Renaming or removing the major headings the regex parser searches for
- Replacing fenced code blocks with inline snippets or prose
- Changing testcase formatting away from numbered pairs or parseable tables
- Changing language labels on code fences to nonstandard names
- Moving solution code into a section the parser does not search

## Lower-Risk Prompt Changes

- Tightening wording inside an existing section
- Adding clearer constraints while preserving section boundaries
- Expanding hints or examples without changing how code fences or testcase pairs are emitted

## Practical Rule

If a prompt edit changes structure, make the parser edit in the same patch and validate the bundle
shape immediately afterward.
