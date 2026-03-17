from __future__ import annotations

import sqlite3

from utils import NotFoundError, ValidationError, now_timestamp, validate_project_name


def add_project(connection: sqlite3.Connection, name: str, description: str | None) -> int:
    cleaned_name = validate_project_name(name)
    cleaned_description = (description or "").strip()
    timestamp = now_timestamp()

    try:
        cursor = connection.execute(
            """
            INSERT INTO projects (name, description, is_active, created_at, updated_at)
            VALUES (?, ?, 1, ?, ?)
            """,
            (cleaned_name, cleaned_description, timestamp, timestamp),
        )
    except sqlite3.IntegrityError as exc:
        raise ValidationError(f"Project name '{cleaned_name}' already exists.") from exc

    connection.commit()
    return int(cursor.lastrowid)


def edit_project(
    connection: sqlite3.Connection,
    project_id: int,
    *,
    name: str | None,
    description: str | None,
) -> None:
    project = get_project(connection, project_id)
    updates: list[str] = []
    values: list[object] = []

    if name is not None:
        updates.append("name = ?")
        values.append(validate_project_name(name))

    if description is not None:
        updates.append("description = ?")
        values.append(description.strip())

    if not updates:
        raise ValidationError("Provide at least one field to update.")

    updates.append("updated_at = ?")
    values.append(now_timestamp())
    values.append(project["id"])

    try:
        connection.execute(
            f"UPDATE projects SET {', '.join(updates)} WHERE id = ?",
            values,
        )
    except sqlite3.IntegrityError as exc:
        raise ValidationError("Project name already exists.") from exc

    connection.commit()


def list_projects(connection: sqlite3.Connection, *, include_archived: bool) -> list[sqlite3.Row]:
    if include_archived:
        cursor = connection.execute(
            """
            SELECT id, name, description, is_active, created_at, updated_at
            FROM projects
            ORDER BY is_active DESC, name COLLATE NOCASE ASC
            """
        )
    else:
        cursor = connection.execute(
            """
            SELECT id, name, description, is_active, created_at, updated_at
            FROM projects
            WHERE is_active = 1
            ORDER BY name COLLATE NOCASE ASC
            """
        )
    return list(cursor.fetchall())


def archive_project(connection: sqlite3.Connection, project_id: int) -> None:
    _set_project_active_state(connection, project_id, is_active=False)


def activate_project(connection: sqlite3.Connection, project_id: int) -> None:
    _set_project_active_state(connection, project_id, is_active=True)


def get_project(connection: sqlite3.Connection, project_id: int) -> sqlite3.Row:
    cursor = connection.execute(
        """
        SELECT id, name, description, is_active, created_at, updated_at
        FROM projects
        WHERE id = ?
        """,
        (project_id,),
    )
    project = cursor.fetchone()
    if project is None:
        raise NotFoundError(f"Project with id {project_id} does not exist.")
    return project


def ensure_active_project(connection: sqlite3.Connection, project_id: int) -> sqlite3.Row:
    project = get_project(connection, project_id)
    if not bool(project["is_active"]):
        raise ValidationError(f"Project {project_id} is archived and cannot receive new time entries.")
    return project


def _set_project_active_state(connection: sqlite3.Connection, project_id: int, *, is_active: bool) -> None:
    get_project(connection, project_id)
    connection.execute(
        """
        UPDATE projects
        SET is_active = ?, updated_at = ?
        WHERE id = ?
        """,
        (1 if is_active else 0, now_timestamp(), project_id),
    )
    connection.commit()
