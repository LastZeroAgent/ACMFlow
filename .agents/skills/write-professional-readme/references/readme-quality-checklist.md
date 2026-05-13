# README Quality Checklist

Use this checklist as a final pass for new README files and substantial rewrites.

## Accuracy

- The project name matches repository metadata and entry points.
- The description reflects code that actually exists.
- Commands are copied from package files, scripts, tests, docs, or verified local execution.
- Required runtime versions, services, and credentials are mentioned only when supported by files.
- Endpoints, flags, config keys, output paths, and filenames use exact spelling.
- Secret-bearing values are never printed or embedded.

## Reader Journey

- A first-time user can understand the purpose in the first screen.
- Setup steps are ordered from prerequisites to install to run.
- The shortest useful success path is visible before deeper reference material.
- Examples use realistic input and show expected output shape when helpful.
- Troubleshooting covers the most likely local failures without turning into a full FAQ.

## Structure

- Headings are predictable and not overly clever.
- Optional sections are omitted when there is no evidence for them.
- Long command lists are grouped by workflow.
- Project structure listings include only files or directories that matter to users.
- Generated artifacts are documented with paths and a short purpose.

## Tone

- The README is confident but not inflated.
- It avoids generic claims such as "powerful", "seamless", or "production-ready" unless proven.
- It uses the user's requested language, or follows the existing repository language.
- It keeps marketing copy short and developer instructions concrete.

## Maintenance

- Installation and test commands are easy to update later.
- Configuration notes explain where values live without exposing private values.
- Known limitations are explicit when external services, credentials, or platform assumptions exist.
- Links point to files that exist in the repository or stable external documentation.
