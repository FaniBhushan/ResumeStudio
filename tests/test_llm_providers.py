from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

from src.cv_builder import processes


class ProviderRunnerTests(unittest.TestCase):
    schema = {"type": "object", "properties": {"answer": {"type": "string"}}}

    def test_codex_uses_read_only_exec_and_structured_output(self) -> None:
        def fake_run(args: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
            output_path = Path(args[args.index("--output-last-message") + 1])
            output_path.write_text('{"answer":"ok"}', encoding="utf-8")
            return subprocess.CompletedProcess(args, 0, "", "")

        with patch.object(processes.shutil, "which", return_value="/fake/codex"), patch.object(
            processes.subprocess, "run", side_effect=fake_run
        ) as run:
            response = processes.run_llm_prompt("hello", provider="Codex CLI", schema=self.schema)

        self.assertEqual(response, '{"answer":"ok"}')
        args = run.call_args.args[0]
        self.assertIn("--sandbox", args)
        self.assertIn("read-only", args)
        self.assertIn("--output-schema", args)

    def test_gemini_unwraps_headless_json_response(self) -> None:
        completed = subprocess.CompletedProcess(
            ["gemini"], 0, json.dumps({"response": '{"answer":"ok"}', "stats": {}}), ""
        )
        with patch.object(processes.shutil, "which", return_value="/fake/gemini"), patch.object(
            processes.subprocess, "run", return_value=completed
        ) as run:
            response = processes.run_llm_prompt("hello", provider="Gemini CLI", schema=self.schema)

        self.assertEqual(response, '{"answer":"ok"}')
        self.assertIn("plan", run.call_args.args[0])
        self.assertIn("json", run.call_args.args[0])

    def test_claude_unwraps_structured_output_and_disables_tools(self) -> None:
        completed = subprocess.CompletedProcess(
            ["claude"], 0, json.dumps({"structured_output": {"answer": "ok"}}), ""
        )
        with patch.object(processes.shutil, "which", return_value="/fake/claude"), patch.object(
            processes.subprocess, "run", return_value=completed
        ) as run:
            response = processes.run_llm_prompt("hello", provider="Claude Code", schema=self.schema)

        self.assertEqual(json.loads(response), {"answer": "ok"})
        args = run.call_args.args[0]
        self.assertIn("--bare", args)
        self.assertIn("--tools", args)
        self.assertIn("", args)
        self.assertIn("--json-schema", args)

    def test_missing_cli_names_provider(self) -> None:
        with patch.object(processes.shutil, "which", return_value=None):
            with self.assertRaisesRegex(RuntimeError, "Gemini CLI was not found"):
                processes.run_llm_prompt("hello", provider="Gemini CLI")


if __name__ == "__main__":
    unittest.main()
