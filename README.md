# Text-to-Speech Software

A lightweight command-line Text-to-Speech (TTS) tool built with Python and native OS speech engines.

## Features

- Speak text directly through system audio output.
- Convert text to an audio file (`.wav` recommended).
- Read text from command line input or a UTF-8 file.
- Configure voice, speaking rate, and volume.
- List available voices from your backend.

## Backend support

- **Linux**: `espeak` (install with your package manager)
- **macOS**: built-in `say`
- **Windows**: PowerShell + `System.Speech`

## Quick start (source mode)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python tts.py --text "Hello from TTS"
```

## Ready-to-copy production deployment pack

This repository now includes production deployment assets:

- **Python package metadata**: `pyproject.toml`
- **Build/test automation**: `Makefile`
- **Install scripts**:
  - `scripts/install_linux.sh`
  - `scripts/install_macos.sh`
  - `scripts/install_windows.ps1`
- **CI release workflow**: `.github/workflows/release.yml`

### Deployment option A: install from source as a CLI

```bash
python -m venv .venv
source .venv/bin/activate
pip install .
tts --list-voices
```

### Deployment option B: build distributable artifacts

```bash
python -m pip install --upgrade pip build
python -m build
```

Build output:

- `dist/*.whl` (wheel)
- `dist/*.tar.gz` (source distribution)

You can publish these to an internal package index or PyPI.

### Deployment option C: one-command installers

#### Linux

```bash
./scripts/install_linux.sh
```

#### macOS

```bash
./scripts/install_macos.sh
```

#### Windows (PowerShell)

```powershell
./scripts/install_windows.ps1
```

## Usage

### Speak text out loud

```bash
tts --text "Hello! This is your text to speech software."
```

### Speak from a text file

```bash
tts --input-file message.txt
```

### Save speech to a file

```bash
tts --text "Saving to file" --output speech.wav
```

### List available voices

```bash
tts --list-voices
```

### Control rate, volume, and voice

```bash
tts --text "Custom settings" --rate 180 --volume 0.8 --voice en
```

## Makefile shortcuts

```bash
make test
make build
```

## Run tests

```bash
python -m unittest discover -s tests
```
