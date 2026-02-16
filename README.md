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

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Speak text out loud

```bash
python tts.py --text "Hello! This is your text to speech software."
```

### Speak from a text file

```bash
python tts.py --input-file message.txt
```

### Save speech to a file

```bash
python tts.py --text "Saving to file" --output speech.wav
```

### List available voices

```bash
python tts.py --list-voices
```

### Control rate, volume, and voice

```bash
python tts.py --text "Custom settings" --rate 180 --volume 0.8 --voice en
```

## Run tests

```bash
python -m unittest discover -s tests
```
