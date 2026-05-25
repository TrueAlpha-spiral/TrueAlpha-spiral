import os
import re
import subprocess
import sys
import unittest


class TestTasCliHelp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cli_path = os.path.abspath("tas_cli.py")

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, self.cli_path, *args],
            check=True,
            capture_output=True,
            text=True,
        )

    def test_top_level_help_includes_examples(self):
        result = self.run_cli("--help")

        self.assertIn("Examples:", result.stdout)
        self.assertIn("python tas_cli.py shadow-scan .", result.stdout)
        self.assertIn("Create TAS metadata for an artifact", result.stdout)

    def test_sequence_help_includes_defaults(self):
        result = self.run_cli("sequence", "--help")

        normalized_stdout = re.sub(r'\s+', ' ', result.stdout)

        self.assertIn("emit the matching .tasmeta.json sidecar", normalized_stdout)
        self.assertIn("Human Seed ID used in the metadata", normalized_stdout)
        self.assertIn("(default: Russell Nordland)", normalized_stdout)
        self.assertIn("(default: TAS_GENOME_V1)", normalized_stdout)
