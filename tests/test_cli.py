from __future__ import annotations

from tests.helpers import TempDatabaseTestCase


class CliTests(TempDatabaseTestCase):
    def test_project_add_command(self) -> None:
        exit_code, output = self.run_cli(["project", "add", "Alpha"])

        self.assertEqual(exit_code, 0)
        self.assertIn("Project created with id 1.", output)

    def test_project_list_command(self) -> None:
        self.run_cli(["project", "add", "Alpha", "--description", "Internal"])

        exit_code, output = self.run_cli(["project", "list"])

        self.assertEqual(exit_code, 0)
        self.assertIn("Alpha", output)
        self.assertIn("Internal", output)
        self.assertIn("active", output)

    def test_time_list_command_with_project_filter(self) -> None:
        self.run_cli(["project", "add", "Alpha"])
        self.run_cli(["project", "add", "Beta"])
        self.run_cli(
            [
                "time",
                "add",
                "--project",
                "1",
                "--date",
                "2026-03-17",
                "--hours",
                "1.5",
            ]
        )
        self.run_cli(
            [
                "time",
                "add",
                "--project",
                "2",
                "--date",
                "2026-03-17",
                "--hours",
                "2.0",
            ]
        )

        exit_code, output = self.run_cli(["time", "list", "--project", "2"])

        self.assertEqual(exit_code, 0)
        self.assertIn("Beta", output)
        self.assertNotIn("Alpha", output)

    def test_report_commands(self) -> None:
        self.run_cli(["project", "add", "Alpha"])
        self.run_cli(
            [
                "time",
                "add",
                "--project",
                "1",
                "--date",
                "2026-03-17",
                "--hours",
                "2.5",
                "--note",
                "Feature work",
            ]
        )

        grouped_exit_code, grouped_output = self.run_cli(["report", "by-project"])
        detail_exit_code, detail_output = self.run_cli(["report", "project", "1"])

        self.assertEqual(grouped_exit_code, 0)
        self.assertEqual(detail_exit_code, 0)
        self.assertIn("2.50", grouped_output)
        self.assertIn("Project 1: Alpha", detail_output)
        self.assertIn("Feature work", detail_output)

    def test_invalid_cli_input_returns_error_code_and_message(self) -> None:
        self.run_cli(["project", "add", "Alpha"])
        self.run_cli(["project", "archive", "1"])

        exit_code, output = self.run_cli(
            [
                "time",
                "add",
                "--project",
                "1",
                "--date",
                "2026-03-18",
                "--hours",
                "1",
            ]
        )

        self.assertEqual(exit_code, 1)
        self.assertIn("archived", output)
