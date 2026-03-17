from __future__ import annotations

import projects
from tests.helpers import TempDatabaseTestCase
from utils import ValidationError


class ProjectTests(TempDatabaseTestCase):
    def test_add_project(self) -> None:
        with self.make_connection() as connection:
            project_id = projects.add_project(connection, "Alpha", None)
            project = projects.get_project(connection, project_id)

        self.assertEqual(project_id, 1)
        self.assertEqual(project["name"], "Alpha")
        self.assertEqual(project["description"], "")
        self.assertTrue(project["is_active"])

    def test_add_project_with_description(self) -> None:
        with self.make_connection() as connection:
            project_id = projects.add_project(connection, "Alpha", "Customer work")
            project = projects.get_project(connection, project_id)

        self.assertEqual(project["description"], "Customer work")

    def test_edit_project(self) -> None:
        with self.make_connection() as connection:
            project_id = projects.add_project(connection, "Alpha", "Old")
            projects.edit_project(
                connection,
                project_id,
                name="Beta",
                description="Updated description",
            )
            project = projects.get_project(connection, project_id)

        self.assertEqual(project["name"], "Beta")
        self.assertEqual(project["description"], "Updated description")

    def test_list_projects_only_returns_active_by_default(self) -> None:
        with self.make_connection() as connection:
            active_id = projects.add_project(connection, "Active", None)
            archived_id = projects.add_project(connection, "Archived", None)
            projects.archive_project(connection, archived_id)

            listed = projects.list_projects(connection, include_archived=False)

        self.assertEqual([row["id"] for row in listed], [active_id])

    def test_list_projects_with_all_includes_archived(self) -> None:
        with self.make_connection() as connection:
            active_id = projects.add_project(connection, "Active", None)
            archived_id = projects.add_project(connection, "Archived", None)
            projects.archive_project(connection, archived_id)

            listed = projects.list_projects(connection, include_archived=True)

        listed_ids = {row["id"] for row in listed}
        self.assertEqual(listed_ids, {active_id, archived_id})
        archived_row = next(row for row in listed if row["id"] == archived_id)
        self.assertFalse(archived_row["is_active"])

    def test_archive_and_activate_project(self) -> None:
        with self.make_connection() as connection:
            project_id = projects.add_project(connection, "Alpha", None)
            projects.archive_project(connection, project_id)
            self.assertFalse(projects.get_project(connection, project_id)["is_active"])

            projects.activate_project(connection, project_id)
            project = projects.get_project(connection, project_id)

        self.assertTrue(project["is_active"])

    def test_empty_project_name_is_rejected(self) -> None:
        with self.make_connection() as connection:
            with self.assertRaises(ValidationError):
                projects.add_project(connection, "   ", None)

    def test_duplicate_project_name_is_rejected(self) -> None:
        with self.make_connection() as connection:
            projects.add_project(connection, "Alpha", None)

            with self.assertRaises(ValidationError):
                projects.add_project(connection, "Alpha", None)
