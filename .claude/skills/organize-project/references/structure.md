# Standard Project Structure Reference

## Root files

| File | Purpose | Committed? |
|------|---------|------------|
| `CLAUDE.md` | Loaded at session start. Project overview, goals, architecture, commands, coding conventions. Can be overridden by CLAUDE.local.md. | Yes |
| `CLAUDE.local.md` | Personal notes, local paths, machine-specific preferences. | No (gitignored) |
| `.mcp.json` | MCP integration config. Connects tools (n8n, Notion, Slack, Google, etc.). Shared with the team through version control. | Yes, no secrets inside (use env var references) |
| `README.md` | Human-facing intro and quick start. | Yes |
| `.gitignore` | Keeps secrets, local files, and generated output out of git. | Yes |
| `requirements.txt` / `pyproject.toml` / `package.json` | Dependencies. Stay at root. | Yes |
| `Dockerfile`, `docker-compose.yml` | Containerization for reproducibility (optional). Stay at root. | Yes |

## Folders

### `config/`
Application settings and environment variables: model parameters, tool configuration, logging and
monitoring setup. `settings.json` (or `agent_config.yaml`, `model_config.yaml`, `logging_config.yaml`)
plus `.env.example`. The real `.env` is never committed.

### `src/`
Core source code, kept modular and reusable.
- `agents/` Agent implementations: `base_agent`, `planner_agent`, `tool_agent`, `supervisor_agent`, custom agents.
- `workflows/` Orchestration, task routing, planning logic, multi-agent coordination (`agent_graph`, `orchestrator`, `task_router`).
- `tools/` Web search, code execution, API access, database access, custom tools.
- `memory/` Short-term (conversation) memory, long-term memory (vector DB, DB), memory store logic.
- `utils/` Shared helpers.
- `types/` Shared types, schemas, data models.
- `app/` Main application code (FastAPI, etc.), API endpoints, optional UI. Wires agents, tools, and workflows together.

### `prompts/`
Prompt templates and system prompts, versioned like code.
- `system/` System prompts for agents.
- `templates/` Reusable templates for consistent results; chain definitions.

### `data/`
- `input/` (or `raw/`) Source data.
- `processed/` Cleaned data (optional).
- `vector_db/` Local vector store files such as FAISS or Qdrant (optional, usually gitignored).
- `output/` Generated results (usually gitignored).
- `examples/` Sample inputs and outputs, test data for development.

### `scripts/`
Helper scripts for setup, running, and deployment: `setup.sh`, `run.sh`, `deploy.sh`,
`build_index.py`, `evaluate.py`.

### `docs/`
`architecture.md` (diagrams and explanations), `usage.md` (setup guide, usage examples,
troubleshooting).

### `tests/`
Test cases for agents and workflows, evaluation datasets, metrics (task success, faithfulness),
benchmarks. Validates outputs and edge cases.

## How an agent project flows

User query -> agent (`src/agents`) -> tools (`src/tools`) -> memory (`src/memory`) ->
planning and workflow (`src/workflows`) -> LLM -> response (`src/app`).

## Where loose files usually go

| Loose file looks like | Move to |
|-----------------------|---------|
| `*agent*.py/ts` | `src/agents/` |
| `*workflow*`, `*orchestrat*`, `*router*`, `*graph*` | `src/workflows/` |
| `*tool*`, `*search*`, `*scrape*`, `*client*` | `src/tools/` |
| `*memory*`, `*store*` | `src/memory/` |
| `*util*`, `*helper*` | `src/utils/` |
| `*types*`, `*schema*`, `*model*` (data models) | `src/types/` |
| `main.*`, `app.*`, `api.*`, `server.*` | `src/app/` |
| `*prompt*.md/.txt` | `prompts/system/` or `prompts/templates/` |
| `*.json`, `*.csv`, `*.jsonl`, `*.xlsx` (data) | `data/input/` or `data/examples/` |
| `*.sh`, `setup.*`, `deploy.*` | `scripts/` |
| `*.md` other than README/CLAUDE/LICENSE/CHANGELOG | `docs/` |
| `test_*`, `*_test.*`, `*.test.*`, `*eval*` | `tests/` |
| `*.yaml`, `*.yml`, `*.toml`, `settings.*`, `.env.example` (not CI, not package manifests) | `config/` |
