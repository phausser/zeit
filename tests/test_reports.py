from __future__ import annotations

import projects
import reports
import time_entries
from tests.helpers import TempDatabaseTestCase
from utils import ValidationError


class ReportTests(TempDatabaseTestCase):
    def test_report_by_project_returns_totals(self) -> None:
        with self.make_connection() as connection:
            alpha_id = projects.add_project(connection, "Alpha", None)
            beta_id = projects.add_project(connection, "Beta", None)
            time_entries.add_time_entry(
                connection,
                project_id=alpha_id,
                entry_date="2026-03-17",
                hours=2.5,
                note=None,
            )
            time_entries.add_time_entry(
                connection,
                project_id=beta_id,
                entry_date="2026-03-17",
                hours=1.0,
                note=None,
            )
            rows = reports.report_by_project(connection, from_date=None, to_date=None)

        totals = {row["id"]: float(row["total_hours"]) for row in rows}
        self.assertEqual(totals[alpha_id], 2.5)
        self.assertEqual(totals[beta_id], 1.0)

    def test_report_for_project_returns_entries_and_sum(self) -> None:
        with self.make_connection() as connection:
            project_id = projects.add_project(connection, "Alpha", None)
            time_entries.add_time_entry(
                connection,
                project_id=project_id,
                entry_date="2026-03-15",
                hours=1.5,
                note="Analysis",
            )
            time_entries.add_time_entry(
                connection,
                project_id=project_id,
                entry_date="2026-03-17",
                hours=2.0,
                note="Coding",
            )

            project, rows, total_hours = reports.report_for_project(
                connection,
                project_id=project_id,
                from_date=None,
                to_date=None,
            )

        self.assertEqual(project["name"], "Alpha")
        self.assertEqual(total_hours, 3.5)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["entry_date"], "2026-03-17")

    def test_reports_support_date_filters(self) -> None:
        with self.make_connection() as connection:
            project_id = projects.add_project(connection, "Alpha", None)
            time_entries.add_time_entry(
                connection,
                project_id=project_id,
                entry_date="2026-03-10",
                hours=1.0,
                note=None,
            )
            time_entries.add_time_entry(
                connection,
                project_id=project_id,
                entry_date="2026-03-20",
                hours=3.0,
                note=None,
            )

            grouped_rows = reports.report_by_project(
                connection,
                from_date="2026-03-15",
                to_date="2026-03-31",
            )
            _, detail_rows, total_hours = reports.report_for_project(
                connection,
                project_id=project_id,
                from_date="2026-03-15",
                to_date="2026-03-31",
            )

        self.assertEqual(float(grouped_rows[0]["total_hours"]), 3.0)
        self.assertEqual(total_hours, 3.0)
        self.assertEqual(len(detail_rows), 1)
        self.assertEqual(detail_rows[0]["entry_date"], "2026-03-20")

    def test_report_date_filter_validation(self) -> None:
        with self.make_connection() as connection:
            projects.add_project(connection, "Alpha", None)

            with self.assertRaises(ValidationError):
                reports.report_by_project(
                    connection,
                    from_date="2026-03-20",
                    to_date="2026-03-10",
                )
