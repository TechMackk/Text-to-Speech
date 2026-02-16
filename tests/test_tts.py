from __future__ import annotations

import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import tts


class ParseArgsTests(unittest.TestCase):
    def test_requires_text_or_input_or_list(self) -> None:
        with patch.object(sys, "argv", ["tts.py"]):
            with self.assertRaises(SystemExit):
                tts.parse_args()

    def test_accepts_text(self) -> None:
        with patch.object(sys, "argv", ["tts.py", "--text", "hello"]):
            args = tts.parse_args()
        self.assertEqual(args.text, "hello")


class LoadTextTests(unittest.TestCase):
    def test_loads_from_text_argument(self) -> None:
        self.assertEqual(tts.load_text("  hello  ", None), "hello")

    def test_loads_from_file(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "sample.txt"
            file_path.write_text(" hello file ", encoding="utf-8")
            self.assertEqual(tts.load_text(None, file_path), "hello file")


class CommandBuildTests(unittest.TestCase):
    @patch("tts.platform.system", return_value="Linux")
    @patch("tts.shutil.which", return_value="/usr/bin/espeak")
    def test_linux_speak_command(self, _mock_which, _mock_system) -> None:
        app = tts.TextToSpeechApp(rate=180, volume=0.5, voice="en")
        command = app._build_command("hello", None)
        self.assertEqual(command[:7], ["espeak", "-v", "en", "-s", "180", "-a", "100"])


if __name__ == "__main__":
    unittest.main()
