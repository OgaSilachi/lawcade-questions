#!/usr/bin/env python3
"""Audit a project against the standard layout. Read-only: changes nothing.

Usage: python3 audit.py <project-root> [--profile minimal|standard|agent] [--json]
"""
import argparse
import fnmatch
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout import PROFILES, ROOT_KEEP, required  # noqa: E402

# (glob patterns, destination). First match wins, so order matters.
MOVE_RULES = [
    (["test_*", "*_test.*", "*.test.*", "*.spec.*", "*eval*"], "tests/"),
    (["*agent*.py", "*agent*.ts", "*agent*.js"], "src/agents/"),
    (["*workflow*", "*orchestrat*", "*router*", "*graph*.py"], "src/workflows/"),
    (["*memory*", "*_store.*"], "src/memory/"),
    (["*tool*.py", "*tool*.ts", "*tool*.js", "*search*.py", "*scrape*", "*client*.py"], "src/tools/"),
    (["*util*", "*helper*"], "src/utils/"),
    (["*types*", "*schema*"], "src/types/"),
    (["main.*", "app.*", "api.*", "server.*", "index.*", "ui.*"], "src/app/"),
    (["*prompt*.md", "*prompt*.txt", "*prompt*.yaml"], "prompts/templates/"),
    (["*.sh", "*.ps1", "*.bat", "setup.*", "deploy.*", "run.*"], "scripts/"),
    (["*.yaml", "*.yml", "*.toml", "*.ini", "settings.*", "config.*"], "config/"),
    (["*.json", "*.jsonl", "*.csv", "*.tsv", "*.xlsx", "*.xls", "*.parquet", "*.txt"], "data/input/"),
    (["*.md", "*.pdf", "*.docx"], "docs/"),
    (["*.py", "*.ts", "*.js", "*.tsx", "*.jsx", "*.go", "*.rs", "*.rb"], "src/"),
]


def suggest(name):
    low = name.lower()
    for patterns, dest in MOVE_RULES:
        if any(fnmatch.fnmatch(low, p) for p in patterns):
            return dest
    return None


def audit(root, profile):
    req = required(profile)
    present, missing = [], []
    for path, kind in req:
        full = os.path.join(root, path)
        ok = os.path.isdir(full) if kind == "dir" else os.path.isfile(full)
        (present if ok else missing).append(path + ("/" if kind == "dir" else ""))

    moves = []
    for name in sorted(os.listdir(root)):
        full = os.path.join(root, name)
        if not os.path.isfile(full) or name in ROOT_KEEP:
            continue
        dest = suggest(name)
        if dest:
            moves.append({"from": name, "to": dest + name})
        else:
            moves.append({"from": name, "to": None})

    warnings = []
    gi = os.path.join(root, ".gitignore")
    gi_text = open(gi, encoding="utf-8", errors="ignore").read() if os.path.isfile(gi) else ""
    if os.path.isfile(os.path.join(root, ".env")) and ".env" not in gi_text:
        warnings.append(".env exists but is not gitignored. Secrets may be committed.")
    if os.path.isfile(os.path.join(root, "CLAUDE.local.md")) and "CLAUDE.local.md" not in gi_text:
        warnings.append("CLAUDE.local.md is not gitignored.")
    mcp = os.path.join(root, ".mcp.json")
    if os.path.isfile(mcp):
        try:
            servers = json.load(open(mcp, encoding="utf-8")).get("mcpServers", {})
            if len(servers) > 8:
                warnings.append(
                    f".mcp.json lists {len(servers)} servers. Consider trimming or using one "
                    "endpoint with tool search so tool definitions do not flood context."
                )
        except (ValueError, AttributeError):
            warnings.append(".mcp.json is not valid JSON.")
    claude_md = os.path.join(root, "CLAUDE.md")
    if os.path.isfile(claude_md) and "TODO(organize-project)" in open(claude_md, encoding="utf-8").read():
        warnings.append("CLAUDE.md still has template placeholders. Fill them in.")

    score = round(100 * len(present) / len(req)) if req else 100
    return {
        "root": os.path.abspath(root),
        "profile": profile,
        "score": score,
        "present": present,
        "missing": missing,
        "suggested_moves": [m for m in moves if m["to"]],
        "unclassified_root_files": [m["from"] for m in moves if not m["to"]],
        "warnings": warnings,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--profile", choices=PROFILES, default="standard")
    ap.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = ap.parse_args()

    if not os.path.isdir(args.root):
        sys.exit(f"Not a directory: {args.root}")
    r = audit(args.root, args.profile)

    if args.json:
        print(json.dumps(r, indent=2))
        return

    print(f"Project: {r['root']}")
    print(f"Profile: {r['profile']}    Structure score: {r['score']}/100\n")
    print("Missing:" if r["missing"] else "Missing: nothing")
    for m in r["missing"]:
        print(f"  - {m}")
    if r["suggested_moves"]:
        print("\nSuggested moves (review before applying; paths may be referenced elsewhere):")
        for m in r["suggested_moves"]:
            print(f"  {m['from']}  ->  {m['to']}")
    if r["unclassified_root_files"]:
        print("\nLoose root files with no rule (decide manually):")
        for f in r["unclassified_root_files"]:
            print(f"  ? {f}")
    if r["warnings"]:
        print("\nWarnings:")
        for w in r["warnings"]:
            print(f"  ! {w}")


if __name__ == "__main__":
    main()
