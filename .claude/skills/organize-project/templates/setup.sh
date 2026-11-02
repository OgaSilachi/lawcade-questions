#!/usr/bin/env bash
# Install dependencies and prepare local config.
set -euo pipefail
cd "$(dirname "$0")/.."
[ -f .env ] || { [ -f config/.env.example ] && cp config/.env.example .env && echo "Created .env from example"; }
[ -f requirements.txt ] && python3 -m pip install -r requirements.txt
[ -f package.json ] && npm install
echo "Setup complete."
