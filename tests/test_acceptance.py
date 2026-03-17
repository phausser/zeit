from __future__ import annotations

from tests.helpers import TempDatabaseTestCase


class AcceptanceTests(TempDatabaseTestCase):
    def test_complete_time_tracking_workflow(self) -> None:
        create_exit_code, create_output = self.run_cli(
            ["project", "add", "Website Relaunch"]
        )
        self.assertEqual(create_exit_code, 0)
        self.assertIn("Project created with id 1.", create_output)

        first_entry_exit_code, _ = self.run_cli(
            [
                "time",
                "add",
                "--project",
                "1",
                "--date",
                "2026-03-15",
                "--hours",
                "2.5",
                "--note",
                "Planung",
            ]
        )
        second_entry_exit_code, _ = self.run_cli(
            [
                "time",
                "add",
                "--project",
                "1",
                "--date",
                "2026-03-16",
                "--hours",
                "3",
                "--note",
                "Umsetzung",
            ]
        )
        self.assertEqual(first_entry_exit_code, 0)
        self.assertEqual(second_entry_exit_code, 0)

        list_exit_code, list_output = self.run_cli(["time", "list", "--project", "1"])
        self.assertEqual(list_exit_code, 0)
        self.assertIn("Website Relaunch", list_output)
        self.assertIn("2026-03-15", list_output)
        self.assertIn("2026-03-16", list_output)
        self.assertIn("Planung", list_output)
        self.assertIn("Umsetzung", list_output)

        report_exit_code, report_output = self.run_cli(["report", "project", "1"])
        self.assertEqual(report_exit_code, 0)
        self.assertIn("Project 1: Website Relaunch", report_output)
        self.assertIn("Total Hours: 5.50", report_output)

        archive_exit_code, archive_output = self.run_cli(["project", "archive", "1"])
        self.assertEqual(archive_exit_code, 0)
        self.assertIn("Project 1 archived.", archive_output)

        rejected_exit_code, rejected_output = self.run_cli(
            [
                "time",
                "add",
                "--project",
                "1",
                "--date",
                "2026-03-17",
                "--hours",
                "1",
                "--note",
                "Nachtrag",
            ]
        )
        self.assertEqual(rejected_exit_code, 1)
        self.assertIn("archived", rejected_output)
