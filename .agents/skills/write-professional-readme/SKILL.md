---
name: write-professional-readme
description: Use when creating, rewriting, auditing, or localizing a professional README.md or project landing document for a repository, library, API, CLI, web app, data project, or generated problem corpus. Trigger for requests about README generation, README polish, installation/usage docs, quick starts, badges, feature summaries, project structure, contribution sections, or making documentation clearer and more credible.
---

# Write Professional README

Create README files that are accurate to the codebase, useful to first-time users, and polished
enough for public release. Prefer evidence from repository files over generic filler.

## Workflow

1. Inspect the repository before drafting: read existing `README.md`, package/build files, entry
   points, tests, examples, docs, and public API surfaces.
2. Identify the audience and purpose: user-facing product, developer library, CLI tool, API service,
   research/demo project, internal tool, or problem corpus.
3. Draft around real capabilities only. If a feature is inferred, mark it as inferred in your
   reasoning and verify through code or tests before presenting it as fact.
4. Prefer a concise, scannable README structure. Put the most useful setup and usage path near the
   top.
5. Preserve repository-specific names, commands, endpoint spellings, environment variables, and file
   layout. Do not invent branding, badges, screenshots, licenses, or deployment targets.
6. Validate commands when feasible with local, non-destructive checks. If commands require secrets,
   network, live services, or destructive state changes, document them without running them.
7. When editing an existing README, keep valuable existing content and remove stale, duplicate, or
   marketing-heavy text.
8. Read `references/readme-quality-checklist.md` before finalizing a new README or a substantial
   rewrite.

## Recommended Structure

Choose only the sections that fit the project:

- Project title and one-sentence value proposition
- What it does, with concrete capabilities
- Requirements or prerequisites
- Installation or setup
- Quick start
- Configuration, including `.env` or config file notes without exposing secrets
- Common commands
- API, CLI, or UI usage examples
- Project structure
- Testing and validation
- Generated output shape or important artifacts
- Development notes, contribution workflow, and troubleshooting
- License, only when a license file or explicit project metadata exists

## Writing Standards

- Lead with utility, not hype.
- Use exact commands in fenced code blocks.
- Keep headings predictable and skimmable.
- Explain configuration boundaries clearly, especially secret-bearing files.
- Include examples that match the repository's actual interface.
- State limitations honestly when setup requires external services, credentials, or unfinished work.
- Match the user's requested language. If no language is specified, follow the repository's existing
  README language; otherwise use clear English for international developer projects.
- Avoid boilerplate sections that cannot be supported by repository evidence.

## Repository-Specific Guardrails

For this ACMFlow repository:

- Treat `config.ini` as secret-bearing. Mention how to configure it, but do not print credentials.
- Preserve the `/promblemserve` endpoint spelling unless the user explicitly asks to rename it.
- Describe generated problem bundles using the real output shape under `problem/normal/<title>/`.
- Prefer local validation commands such as `python tests/parser_smoke.py`,
  `python tests/test_pairwise.py`, and the repository-local skill scripts when relevant.
- Keep root-level entrypoint guidance centered on `python main.py`.

## Output Modes

When the user asks to create or update a README, edit the file directly unless they only requested a
draft. When the user asks for a review, provide findings first with file/line references and suggest
specific README changes.

## References

- Read `references/readme-quality-checklist.md` before publishing a new README or major rewrite.
