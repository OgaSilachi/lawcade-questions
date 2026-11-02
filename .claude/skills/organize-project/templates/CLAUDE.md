# {{PROJECT_NAME}}

<!-- TODO(organize-project): replace every placeholder below, then delete this line. -->

## Overview
One or two sentences: what this project is and who it is for.

## Goals
- Goal 1
- Goal 2

## Architecture
- `src/agents/` agent implementations
- `src/workflows/` orchestration and routing
- `src/tools/` integrations and tool wrappers
- `src/memory/` short and long term memory
- `src/app/` entry point, API, UI
- `prompts/` system prompts and templates
- `config/` settings; secrets live in `.env` (see `config/.env.example`)
- `data/` inputs, outputs, examples
- See `docs/architecture.md` for details.

## Commands
- Setup: `./scripts/setup.sh`
- Run: `./scripts/run.sh`
- Test: (add the test command)

## Conventions
- Keep modules small and reusable; shared helpers go in `src/utils/`.
- Prompts are files in `prompts/`, never inline strings scattered through code.
- Never commit secrets. Personal notes go in `CLAUDE.local.md` (gitignored).
