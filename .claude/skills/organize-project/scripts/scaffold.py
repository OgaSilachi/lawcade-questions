#!/usr/bin/env python3
"""Create any missing pieces of the standard layout. Never overwrites or moves existing files.

Usage: python3 scaffold.py <project-root> [--profile minimal|standard|agent] [--dry-run]
"""
import argparse
import os
import stat
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from layout import GITIGNORE_LINES, PROFILES, required  # noqa: E402

TEMPLATES = os.path.join(os.path.dirname(HERE), "templates")

# Map a layout file to its template file in ../templates
TEMPLATE_FOR = {
    "CLAUDE.md": "CLAUDE.md",
    "CLAUDE.local.md": "CLAUDE.local.md",
    "README.md": "README.md",
    ".mcp.json": "mcp.json",
    "config/settings.json": "settings.json",
    "config/.env.example": "env.example",
    "docs/architecture.md": "architecture.md",
    "docs/usage.md": "usage.md",
    "scripts/setup.sh": "setup.sh",
    "scripts/run.sh": "run.sh",
    "scripts/deploy.sh": "deploy.sh",
}


def render(template_name, project_name):
    path = os.path.join(TEMPLATES, template_name)
    with open(path, encoding="utf-8") as fh:
        return fh.read().replace("{{PROJECT_NAME}}", project_name)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--profile", choices=PROFILES, default="standard")
    ap.add_argument("--dry-run", action="store_true", help="show what would be created")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        sys.exit(f"Not a directory: {root}")
    name = os.path.basename(root)
    created, skipped = [], []

    def note(msg):
        created.append(msg)

    entries = required(args.profile)
    dirs = [p for p, k in entries if k == "dir"]
    files = [p for p, k in entries if k == "file"]

    for d in dirs:
        full = os.path.join(root, d)
        if os.path.isdir(full):
            continue
        note(d + "/")
        if not args.dry_run:
            os.makedirs(full, exist_ok=True)

    for f in files:
        full = os.path.join(root, f)
        if f == ".gitignore":
            continue  # merged below
        if os.path.exists(full):
            skipped.append(f)
            continue
        note(f)
        if args.dry_run:
            continue
        os.makedirs(os.path.dirname(full) or root, exist_ok=True)
        tmpl = TEMPLATE_FOR.get(f)
        content = render(tmpl, name) if tmpl else ""
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(content)
        if f.endswith(".sh"):
            os.chmod(full, os.stat(full).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    # Merge .gitignore: append only lines that are not already there.
    gi = os.path.join(root, ".gitignore")
    existing = open(gi, encoding="utf-8").read().splitlines() if os.path.isfile(gi) else []
    have = {line.strip() for line in existing}
    to_add = [line for line in GITIGNORE_LINES if line and line not in have]
    if to_add:
        note(".gitignore (+%d lines)" % len(to_add))
        if not args.dry_run:
            with open(gi, "a", encoding="utf-8") as fh:
                if existing and existing[-1].strip():
                    fh.write("\n")
                fh.write("# Added by organize-project\n")
                fh.write("\n".join(to_add) + "\n")

    # .gitkeep in any empty required folder so git tracks it.
    for d in dirs:
        full = os.path.join(root, d)
        if args.dry_run or not os.path.isdir(full):
            continue
        if not os.listdir(full):
            open(os.path.join(full, ".gitkeep"), "w").close()

    label = "Would create" if args.dry_run else "Created"
    print(f"{label} ({len(created)}):")
    for c in created:
        print(f"  + {c}")
    if skipped:
        print(f"\nAlready present, left untouched ({len(skipped)}):")
        for s in skipped:
            print(f"  = {s}")
    if not created:
        print("  nothing, the project already matches this profile.")


if __name__ == "__main__":
    main()
