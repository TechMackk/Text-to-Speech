#!/usr/bin/env bash
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required" >&2
  exit 1
fi

if ! command -v espeak >/dev/null 2>&1; then
  if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y espeak
  elif command -v dnf >/dev/null 2>&1; then
    sudo dnf install -y espeak
  elif command -v yum >/dev/null 2>&1; then
    sudo yum install -y espeak
  elif command -v pacman >/dev/null 2>&1; then
    sudo pacman -Sy --noconfirm espeak
  else
    echo "Please install espeak manually with your package manager." >&2
    exit 1
  fi
fi

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .

echo "Installed successfully. Run: . .venv/bin/activate && tts --list-voices"
