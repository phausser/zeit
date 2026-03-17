from __future__ import annotations

import sqlite3

from .projects import ensure_active_project
from .utils import now_timestamp, parse_date, validate_date_range, validate_hours


def add_time_entry(
    connection: sqlite3.Connection,
    *,
    project_id: int,
    entry_date: str,
    hours: float,
    note: str | None,
) -> int:
    ensure_active_project(connection, project_id)
    parsed_date = parse_date(entry_date, field_name="date")
    validated_hours = validate_hours(hours)
    cleaned_note = (note or "").strip()

    cursor = connection.execute(
        """
        INSERT INTO time_entries (project_id, entry_date, hours, note, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (project_id, parsed_date, validated_hours, cleaned_note, now_timestamp()),
    )
    connection.commit()
    return int(cursor.lastrowid)


def list_time_entries(
    connection: sqlite3.Connection,
    *,
    project_id: int | None,
    from_date: str | None,
    to_date: str | None,
) -> list[sqlite3.Row]:
    parsed_from, parsed_to = validate_date_range(from_date, to_date)
    query = """
        SELECT
            te.id,
            te.project_id,
            p.name AS project_name,
            te.entry_date,
            te.hours,
            te.note,
            te.created_at
        FROM time_entries te
        JOIN projects p ON p.id = te.project_id
        WHERE 1 = 1
    """
    params: list[object] = []

    if project_id is not None:
        query += " AND te.project_id = ?"
        params.append(project_id)

    if parsed_from is not None:
        query += " AND te.entry_date >= ?"
        params.append(parsed_from)

    if parsed_to is not None:
        query += " AND te.entry_date <= ?"
        params.append(parsed_to)

    query += " ORDER BY te.entry_date DESC, te.id DESC"

    cursor = connection.execute(query, params)
    return list(cursor.fetchall())
