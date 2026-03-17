from __future__ import annotations

from tests.helpers import TempDatabaseTestCase
from zeit import projects, time_entries
from zeit.utils import NotFoundError, ValidationError


class TimeEntryTests(TempDatabaseTestCase):
    def test_database_is_initialized_and_foreign_keys_are_enabled(self) -> None:
        with self.make_connection() as connection:
            tables = {
                row["name"]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                ).fetchall()
            }
            foreign_keys_enabled = connection.execute("PRAGMA foreign_keys;").fetchone()[0]

            with self.assertRaises(Exception) as context:
                connection.execute(
                    """
                    INSERT INTO time_entries (project_id, entry_date, hours, note, created_at)
                    VALUES (999, '2026-03-17', 1.0, '', '2026-03-17T00:00:00+00:00')
                    """
                )

        self.assertIn("projects", tables)
        self.assertIn("time_entries", tables)
        self.assertEqual(foreign_keys_enabled, 1)
        self.assertEqual(context.exception.__class__.__name__, "IntegrityError")

    def test_add_time_entry(self) -> None:
        with self.make_connection() as connection:
            project_id = projects.add_project(connection, "Alpha", None)
            entry_id = time_entries.add_time_entry(
                connection,
                project_id=project_id,
                entry_date="2026-03-17",
                hours=2.5,
                note="Implementation",
            )
            rows = time_entries.list_time_entries(
                connection,
                project_id=None,
                from_date=None,
                to_date=None,
            )

        self.assertEqual(entry_id, 1)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["project_id"], project_id)
        self.assertEqual(rows[0]["hours"], 2.5)

    def test_list_time_entries_with_project_filter(self) -> None:
        with self.make_connection() as connection:
            alpha_id = projects.add_project(connection, "Alpha", None)
            beta_id = projects.add_project(connection, "Beta", None)
            time_entries.add_time_entry(
                connection,
                project_id=alpha_id,
                entry_date="2026-03-17",
                hours=1.0,
                note=None,
            )
            time_entries.add_time_entry(
                connection,
                project_id=beta_id,
                entry_date="2026-03-17",
                hours=2.0,
                note=None,
            )

            rows = time_entries.list_time_entries(
                connection,
                project_id=beta_id,
                from_date=None,
                to_date=None,
            )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["project_id"], beta_id)

    def test_list_time_entries_with_date_range_filter(self) -> None:
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
                entry_date="2026-03-17",
                hours=2.0,
                note=None,
            )

            rows = time_entries.list_time_entries(
                connection,
                project_id=None,
                from_date="2026-03-15",
                to_date="2026-03-20",
            )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["entry_date"], "2026-03-17")

    def test_invalid_date_is_rejected(self) -> None:
        with self.make_connection() as connection:
            project_id = projects.add_project(connection, "Alpha", None)
            with self.assertRaises(ValidationError):
                time_entries.add_time_entry(
                    connection,
                    project_id=project_id,
                    entry_date="2026-02-30",
                    hours=1.0,
                    note=None,
                )

    def test_wrong_date_format_is_rejected(self) -> None:
        with self.make_connection() as connection:
            project_id = projects.add_project(connection, "Alpha", None)
            with self.assertRaises(ValidationError):
                time_entries.add_time_entry(
                    connection,
                    project_id=project_id,
                    entry_date="17-03-2026",
                    hours=1.0,
                    note=None,
                )

    def test_hours_less_than_or_equal_to_zero_are_rejected(self) -> None:
        with self.make_connection() as connection:
            project_id = projects.add_project(connection, "Alpha", None)
            for invalid_hours in (0, -1):
                with self.assertRaises(ValidationError):
                    time_entries.add_time_entry(
                        connection,
                        project_id=project_id,
                        entry_date="2026-03-17",
                        hours=invalid_hours,
                        note=None,
                    )

    def test_hours_greater_than_24_are_rejected(self) -> None:
        with self.make_connection() as connection:
            project_id = projects.add_project(connection, "Alpha", None)
            with self.assertRaises(ValidationError):
                time_entries.add_time_entry(
                    connection,
                    project_id=project_id,
                    entry_date="2026-03-17",
                    hours=24.1,
                    note=None,
                )

    def test_missing_project_is_rejected(self) -> None:
        with self.make_connection() as connection:
            with self.assertRaises(NotFoundError):
                time_entries.add_time_entry(
                    connection,
                    project_id=999,
                    entry_date="2026-03-17",
                    hours=1.0,
                    note=None,
                )

    def test_archived_project_cannot_receive_new_time_entries(self) -> None:
        with self.make_connection() as connection:
            project_id = projects.add_project(connection, "Alpha", None)
            projects.archive_project(connection, project_id)

            with self.assertRaises(ValidationError):
                time_entries.add_time_entry(
                    connection,
                    project_id=project_id,
                    entry_date="2026-03-17",
                    hours=1.0,
                    note=None,
                )

    def test_invalid_date_range_is_rejected(self) -> None:
        with self.make_connection() as connection:
            projects.add_project(connection, "Alpha", None)

            with self.assertRaises(ValidationError):
                time_entries.list_time_entries(
                    connection,
                    project_id=None,
                    from_date="2026-03-20",
                    to_date="2026-03-10",
                )
