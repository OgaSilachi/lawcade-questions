"""Shared definition of the standard project layout, used by audit.py and scaffold.py."""

PROFILES = ("minimal", "standard", "agent")

# Each entry: (path, kind, lowest profile that requires it)
# kind is "dir" or "file". Profiles are cumulative: agent > standard > minimal.
LAYOUT = [
    ("CLAUDE.md", "file", "minimal"),
    ("CLAUDE.local.md", "file", "minimal"),
    ("README.md", "file", "minimal"),
    (".gitignore", "file", "minimal"),
    ("data", "dir", "minimal"),
    ("data/input", "dir", "minimal"),
    ("data/output", "dir", "minimal"),
    ("data/examples", "dir", "minimal"),
    ("docs", "dir", "minimal"),
    ("docs/architecture.md", "file", "minimal"),
    ("docs/usage.md", "file", "minimal"),
    ("scripts", "dir", "minimal"),
    (".mcp.json", "file", "standard"),
    ("config", "dir", "standard"),
    ("config/settings.json", "file", "standard"),
    ("config/.env.example", "file", "standard"),
    ("src", "dir", "standard"),
    ("src/utils", "dir", "standard"),
    ("src/types", "dir", "standard"),
    ("tests", "dir", "standard"),
    ("scripts/setup.sh", "file", "standard"),
    ("scripts/run.sh", "file", "standard"),
    ("src/agents", "dir", "agent"),
    ("src/workflows", "dir", "agent"),
    ("src/tools", "dir", "agent"),
    ("src/memory", "dir", "agent"),
    ("src/app", "dir", "agent"),
    ("prompts", "dir", "agent"),
    ("prompts/system", "dir", "agent"),
    ("prompts/templates", "dir", "agent"),
    ("scripts/deploy.sh", "file", "agent"),
]

GITIGNORE_LINES = [
    "# Secrets and local config",
    ".env",
    ".env.*",
    "!.env.example",
    "!config/.env.example",
    "CLAUDE.local.md",
    ".claude/settings.local.json",
    "",
    "# Generated output",
    "data/output/*",
    "!data/output/.gitkeep",
    "data/vector_db/",
    "",
    "# Tooling",
    "__pycache__/",
    "*.pyc",
    ".venv/",
    "node_modules/",
    ".DS_Store",
]

# Root files that should stay at the root and never be suggested for a move.
ROOT_KEEP = {
    "README.md", "LICENSE", "LICENSE.md", "LICENSE.txt", "CHANGELOG.md", "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md", "SECURITY.md", "CLAUDE.md", "CLAUDE.local.md", "AGENTS.md",
    ".gitignore", ".gitattributes", ".mcp.json", ".editorconfig", ".dockerignore",
    ".env", ".env.example", ".nvmrc", ".python-version", ".tool-versions",
    "Dockerfile", "docker-compose.yml", "docker-compose.yaml", "Makefile", "Procfile",
    "requirements.txt", "requirements-dev.txt", "pyproject.toml", "setup.cfg", "setup.py",
    "poetry.lock", "uv.lock", "Pipfile", "Pipfile.lock",
    "package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb",
    "tsconfig.json", "jsconfig.json", "go.mod", "go.sum", "Cargo.toml", "Cargo.lock",
    "Gemfile", "Gemfile.lock", "composer.json", "composer.lock", "vercel.json", "netlify.toml",
}


def rank(profile):
    return PROFILES.index(profile)


def required(profile):
    """Layout entries required by the given profile."""
    return [(p, k) for p, k, lvl in LAYOUT if rank(lvl) <= rank(profile)]
