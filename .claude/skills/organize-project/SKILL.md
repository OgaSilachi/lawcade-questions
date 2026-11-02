---
name: organize-project
description: Audit and organize any project folder into the standard Claude Code / AI agent project structure (CLAUDE.md, CLAUDE.local.md, .mcp.json, config/, src/agents|workflows|tools|memory|utils|types|app, prompts/, data/, scripts/, docs/, tests/). Use when the user says "organize this project", "set up the project structure", "scaffold a new project", "clean up this repo", "audit the folder layout", or "make this match the standard structure", or when starting any new project.
---

# Organize Project

Puts every project into one predictable layout so Claude (and people) always know where things live.
The full layout, with what belongs in each folder, is in `references/structure.md`. Read it before
proposing moves.

## The standard layout

```
<project>/
├── CLAUDE.md            # loaded at session start: overview, goals, architecture, conventions
├── CLAUDE.local.md      # personal / machine-specific notes (gitignored)
├── .mcp.json            # shared MCP server config (n8n, Notion, Slack, Google...)
├── README.md
├── .gitignore
├── config/              # settings.json, .env.example (real .env is gitignored)
├── src/
│   ├── agents/          # agent implementations (planner, tool-using, supervisor)
│   ├── workflows/       # orchestration, routing, multi-agent coordination
│   ├── tools/           # web search, code execution, API and DB access
│   ├── memory/          # short-term and long-term memory
│   ├── utils/           # shared helpers
│   ├── types/           # shared types and schemas
│   └── app/             # entry point, API endpoints, UI (optional)
├── prompts/
│   ├── system/          # system prompts for agents
│   └── templates/       # reusable prompt templates
├── data/
│   ├── input/           # raw inputs
│   ├── output/          # generated results (usually gitignored)
│   └── examples/        # sample inputs and outputs
├── scripts/             # setup.sh, run.sh, deploy.sh
├── docs/                # architecture.md, usage.md
└── tests/               # tests and evaluations for agents and workflows
```

## Profiles

Not every project needs every folder. Pick the smallest profile that fits and say which one you chose.

| Profile   | Use for                                   | Creates                                                                 |
|-----------|-------------------------------------------|-------------------------------------------------------------------------|
| `minimal` | content repos, data banks, docs, one-off scripts | CLAUDE.md, CLAUDE.local.md, .gitignore, README.md, data/, docs/, scripts/ |
| `standard`| ordinary apps and automations             | minimal + .mcp.json, config/, src/ (utils, types), tests/               |
| `agent`   | AI agents and AI automation               | everything in the layout above                                           |

## Workflow

Always follow these steps in order. Never skip step 3.

1. **Audit.** Run the audit script against the project root:
   `python3 <skill-dir>/scripts/audit.py <project-root> --profile <profile>`
   It prints a score, what is missing, and suggested moves for loose files. It changes nothing.
2. **Plan.** Turn the audit into a short plan with three lists: folders/files to create, files to
   move (from -> to), and things to leave alone with the reason.
3. **Confirm.** Show the plan and wait for the user to approve it. Moving files can break imports,
   raw GitHub URLs, CI paths, and apps that load files by path. Call out any of those risks you see.
   If a file is consumed by path from outside the repo (for example raw.githubusercontent.com
   links), recommend leaving it in place.
4. **Scaffold.** Create the missing pieces (never overwrites existing files):
   `python3 <skill-dir>/scripts/scaffold.py <project-root> --profile <profile>`
   Add `--dry-run` first if the user wants to preview.
5. **Move.** Use `git mv` (not plain `mv`) for approved moves so history is kept. Then search the
   repo for the old paths and update every reference.
6. **Fill in CLAUDE.md.** Replace the template placeholders with the real project overview, goals,
   architecture, commands, and conventions, based on what you learned from the code. Keep it short.
7. **Verify.** Re-run the audit and report the before and after scores. Run the project's tests or
   build if it has them.

## Rules

- Never overwrite an existing file. Merge into it instead (for example, append missing lines to
  `.gitignore`).
- Never commit secrets. `.env`, `CLAUDE.local.md`, and `data/output/` go in `.gitignore`.
- Keep `.mcp.json` lean: only servers this project actually uses. Every connected tool costs context
  on every turn; if a project needs many tools, prefer a single MCP endpoint with tool search
  enabled over listing dozens of servers.
- Respect the language's own conventions when they conflict (for example, a Python package may keep
  `pyproject.toml` at the root and code in `src/<package_name>/`; a Next.js app keeps `app/` and
  `public/` at the root). Note the exception in CLAUDE.md instead of fighting the framework.
- Empty folders get a `.gitkeep` so git tracks them.
