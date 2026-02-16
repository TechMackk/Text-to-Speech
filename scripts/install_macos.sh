#!/usr/bin/env bash
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required (install with Homebrew: brew install python)" >&2
  exit 1
fi

if ! command -v say >/dev/null 2>&1; then
  echo "The 'say' command is required and should be available on macOS." >&2
  exit 1
fi

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .

echo "Installed successfully. Run: . .venv/bin/activate && tts --list-voices"
