#!/usr/bin/env python3
"""Cross-platform command-line text-to-speech application using system tools."""

from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
from pathlib import Path


class TextToSpeechApp:
    """Text-to-speech wrapper that delegates to native OS capabilities."""

    def __init__(self, rate: int | None = None, volume: float | None = None, voice: str | None = None) -> None:
        self.rate = rate
        self.volume = volume
        self.voice = voice
        self.system = platform.system().lower()

    def speak(self, text: str) -> None:
        command = self._build_command(text=text, output_path=None)
        subprocess.run(command, check=True)

    def save_to_file(self, text: str, output_path: Path) -> None:
        command = self._build_command(text=text, output_path=output_path)
        subprocess.run(command, check=True)

    def list_voices(self) -> list[str]:
        if self.system == "darwin" and shutil.which("say"):
            result = subprocess.run(["say", "-v", "?"], check=True, capture_output=True, text=True)
            return [line for line in result.stdout.splitlines() if line.strip()]
        if self.system == "linux" and shutil.which("espeak"):
            result = subprocess.run(["espeak", "--voices"], check=True, capture_output=True, text=True)
            return [line for line in result.stdout.splitlines() if line.strip()]
        return ["Voice listing is unavailable for this OS/backend."]

    def _build_command(self, text: str, output_path: Path | None) -> list[str]:
        if self.system == "darwin" and shutil.which("say"):
            command = ["say"]
            if self.voice:
                command.extend(["-v", self.voice])
            if self.rate is not None:
                command.extend(["-r", str(self.rate)])
            if output_path is not None:
                command.extend(["-o", str(output_path)])
            command.append(text)
            return command

        if self.system == "linux" and shutil.which("espeak"):
            command = ["espeak"]
            if self.voice:
                command.extend(["-v", self.voice])
            if self.rate is not None:
                command.extend(["-s", str(self.rate)])
            if self.volume is not None:
                command.extend(["-a", str(int(self.volume * 200))])
            if output_path is not None:
                command.extend(["-w", str(output_path)])
            command.append(text)
            return command

        if self.system == "windows":
            escaped_text = text.replace("'", "''")
            if output_path is not None:
                script = (
                    "Add-Type -AssemblyName System.Speech;"
                    "$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer;"
                    f"$speak.Rate = {self.rate if self.rate is not None else 0};"
                    f"$speak.Volume = {int(self.volume * 100) if self.volume is not None else 100};"
                    f"$speak.SetOutputToWaveFile('{output_path}');"
                    f"$speak.Speak('{escaped_text}');"
                    "$speak.Dispose();"
                )
            else:
                script = (
                    "Add-Type -AssemblyName System.Speech;"
                    "$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer;"
                    f"$speak.Rate = {self.rate if self.rate is not None else 0};"
                    f"$speak.Volume = {int(self.volume * 100) if self.volume is not None else 100};"
                    f"$speak.Speak('{escaped_text}');"
                    "$speak.Dispose();"
                )
            if self.voice:
                script = script.replace("$speak.Rate", f"$speak.SelectVoice('{self.voice}');$speak.Rate")
            return ["powershell", "-Command", script]

        raise RuntimeError(
            "No supported TTS backend found. Install 'espeak' on Linux or use macOS 'say'."
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert text to spoken audio.")
    text_group = parser.add_mutually_exclusive_group(required=False)
    text_group.add_argument("-t", "--text", help="Text to read aloud or export.")
    text_group.add_argument("-i", "--input-file", type=Path, help="Path to a UTF-8 text file.")

    parser.add_argument("-o", "--output", type=Path, help="Optional output audio filename (e.g. speech.wav).")
    parser.add_argument("--rate", type=int, default=None, help="Speech rate.")
    parser.add_argument("--volume", type=float, default=None, help="Volume from 0.0 to 1.0.")
    parser.add_argument("--voice", type=str, default=None, help="Voice ID/name.")
    parser.add_argument("--list-voices", action="store_true", help="List available system voices and exit.")
    args = parser.parse_args()

    if not args.list_voices and not args.text and not args.input_file:
        parser.error("Provide --text or --input-file (or use --list-voices).")

    if args.volume is not None and not 0.0 <= args.volume <= 1.0:
        parser.error("--volume must be between 0.0 and 1.0.")

    return args


def load_text(text: str | None, input_file: Path | None) -> str:
    if text is not None:
        return text.strip()
    if input_file is None:
        return ""
    return input_file.read_text(encoding="utf-8").strip()


def main() -> None:
    args = parse_args()
    app = TextToSpeechApp(rate=args.rate, volume=args.volume, voice=args.voice)

    if args.list_voices:
        for voice_line in app.list_voices():
            print(voice_line)
        return

    text = load_text(args.text, args.input_file)
    if not text:
        raise SystemExit("No text content was provided.")

    if args.output:
        app.save_to_file(text, args.output)
        print(f"Saved speech to {args.output}")
    else:
        app.speak(text)


if __name__ == "__main__":
    main()
