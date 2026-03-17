from __future__ import annotations

import sqlite3

from .projects import get_project
from .utils import validate_date_range


def report_by_project(
    connection: sqlite3.Connection,
    *,
    from_date: str | None,
    to_date: str | None,
) -> list[sqlite3.Row]:
    parsed_from, parsed_to = validate_date_range(from_date, to_date)
    params: list[object] = []
    filters: list[str] = []

    if parsed_from is not None:
        filters.append("te.entry_date >= ?")
        params.append(parsed_from)

    if parsed_to is not None:
        filters.append("te.entry_date <= ?")
        params.append(parsed_to)

    if filters:
        query = """
            SELECT
                p.id,
                p.name,
                p.is_active,
                COALESCE(SUM(CASE
                    WHEN {conditions} THEN te.hours
                    ELSE 0
                END), 0) AS total_hours
            FROM projects p
            LEFT JOIN time_entries te ON te.project_id = p.id
            GROUP BY p.id, p.name, p.is_active
            ORDER BY total_hours DESC, p.name COLLATE NOCASE ASC
        """.format(conditions=" AND ".join(filters))
    else:
        query = """
            SELECT
                p.id,
                p.name,
                p.is_active,
                COALESCE(SUM(te.hours), 0) AS total_hours
            FROM projects p
            LEFT JOIN time_entries te ON te.project_id = p.id
            GROUP BY p.id, p.name, p.is_active
            ORDER BY total_hours DESC, p.name COLLATE NOCASE ASC
        """

    cursor = connection.execute(query, params)
    return list(cursor.fetchall())


def report_for_project(
    connection: sqlite3.Connection,
    *,
    project_id: int,
    from_date: str | None,
    to_date: str | None,
) -> tuple[sqlite3.Row, list[sqlite3.Row], float]:
    project = get_project(connection, project_id)
    parsed_from, parsed_to = validate_date_range(from_date, to_date)

    query = """
        SELECT id, entry_date, hours, note, created_at
        FROM time_entries
        WHERE project_id = ?
    """
    params: list[object] = [project_id]

    if parsed_from is not None:
        query += " AND entry_date >= ?"
        params.append(parsed_from)

    if parsed_to is not None:
        query += " AND entry_date <= ?"
        params.append(parsed_to)

    query += " ORDER BY entry_date DESC, id DESC"

    rows = list(connection.execute(query, params).fetchall())
    total_hours = sum(float(row["hours"]) for row in rows)
    return project, rows, total_hours
