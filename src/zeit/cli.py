from __future__ import annotations

import argparse
import sqlite3

from . import projects, reports, time_entries
from .db import get_connection
from .utils import NotFoundError, ValidationError, print_table


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="zeit", description="Local CLI time tracking.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    _build_project_parser(subparsers)
    _build_time_parser(subparsers)
    _build_report_parser(subparsers)
    return parser


def run(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    connection = None

    try:
        connection = get_connection()
        return args.handler(connection, args)
    except (ValidationError, NotFoundError) as exc:
        print(f"Error: {exc}")
        return 1
    except sqlite3.Error as exc:
        print(f"Database error: {exc}")
        return 1
    finally:
        if connection is not None:
            connection.close()


def _build_project_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    project_parser = subparsers.add_parser("project", help="Manage projects.")
    project_subparsers = project_parser.add_subparsers(dest="project_command", required=True)

    add_parser = project_subparsers.add_parser("add", help="Add a project.")
    add_parser.add_argument("name")
    add_parser.add_argument("--description")
    add_parser.set_defaults(handler=_handle_project_add)

    edit_parser = project_subparsers.add_parser("edit", help="Edit a project.")
    edit_parser.add_argument("id", type=int)
    edit_parser.add_argument("--name")
    edit_parser.add_argument("--description")
    edit_parser.set_defaults(handler=_handle_project_edit)

    list_parser = project_subparsers.add_parser("list", help="List projects.")
    list_parser.add_argument("--all", action="store_true", dest="include_archived")
    list_parser.set_defaults(handler=_handle_project_list)

    archive_parser = project_subparsers.add_parser("archive", help="Archive a project.")
    archive_parser.add_argument("id", type=int)
    archive_parser.set_defaults(handler=_handle_project_archive)

    activate_parser = project_subparsers.add_parser("activate", help="Activate a project.")
    activate_parser.add_argument("id", type=int)
    activate_parser.set_defaults(handler=_handle_project_activate)


def _build_time_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    time_parser = subparsers.add_parser("time", help="Manage time entries.")
    time_subparsers = time_parser.add_subparsers(dest="time_command", required=True)

    add_parser = time_subparsers.add_parser("add", help="Add a time entry.")
    add_parser.add_argument("--project", required=True, type=int, dest="project_id")
    add_parser.add_argument("--date", required=True, dest="entry_date")
    add_parser.add_argument("--hours", required=True, type=float)
    add_parser.add_argument("--note")
    add_parser.set_defaults(handler=_handle_time_add)

    list_parser = time_subparsers.add_parser("list", help="List time entries.")
    list_parser.add_argument("--project", type=int, dest="project_id")
    list_parser.add_argument("--from", dest="from_date")
    list_parser.add_argument("--to", dest="to_date")
    list_parser.set_defaults(handler=_handle_time_list)


def _build_report_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    report_parser = subparsers.add_parser("report", help="Create reports.")
    report_subparsers = report_parser.add_subparsers(dest="report_command", required=True)

    by_project_parser = report_subparsers.add_parser(
        "by-project",
        help="Report total hours by project.",
    )
    by_project_parser.add_argument("--from", dest="from_date")
    by_project_parser.add_argument("--to", dest="to_date")
    by_project_parser.set_defaults(handler=_handle_report_by_project)

    project_parser = report_subparsers.add_parser(
        "project",
        help="Report for a single project.",
    )
    project_parser.add_argument("id", type=int)
    project_parser.add_argument("--from", dest="from_date")
    project_parser.add_argument("--to", dest="to_date")
    project_parser.set_defaults(handler=_handle_report_project)


def _handle_project_add(connection: sqlite3.Connection, args: argparse.Namespace) -> int:
    project_id = projects.add_project(connection, args.name, args.description)
    print(f"Project created with id {project_id}.")
    return 0


def _handle_project_edit(connection: sqlite3.Connection, args: argparse.Namespace) -> int:
    projects.edit_project(connection, args.id, name=args.name, description=args.description)
    print(f"Project {args.id} updated.")
    return 0


def _handle_project_list(connection: sqlite3.Connection, args: argparse.Namespace) -> int:
    rows = projects.list_projects(connection, include_archived=args.include_archived)
    table_rows = [
        (
            row["id"],
            row["name"],
            row["description"],
            "active" if row["is_active"] else "archived",
            row["updated_at"],
        )
        for row in rows
    ]
    print_table(["ID", "Name", "Description", "Status", "Updated"], table_rows)
    return 0


def _handle_project_archive(connection: sqlite3.Connection, args: argparse.Namespace) -> int:
    projects.archive_project(connection, args.id)
    print(f"Project {args.id} archived.")
    return 0


def _handle_project_activate(connection: sqlite3.Connection, args: argparse.Namespace) -> int:
    projects.activate_project(connection, args.id)
    print(f"Project {args.id} activated.")
    return 0


def _handle_time_add(connection: sqlite3.Connection, args: argparse.Namespace) -> int:
    entry_id = time_entries.add_time_entry(
        connection,
        project_id=args.project_id,
        entry_date=args.entry_date,
        hours=args.hours,
        note=args.note,
    )
    print(f"Time entry created with id {entry_id}.")
    return 0


def _handle_time_list(connection: sqlite3.Connection, args: argparse.Namespace) -> int:
    rows = time_entries.list_time_entries(
        connection,
        project_id=args.project_id,
        from_date=args.from_date,
        to_date=args.to_date,
    )
    table_rows = [
        (
            row["id"],
            row["project_id"],
            row["project_name"],
            row["entry_date"],
            f"{float(row['hours']):.2f}",
            row["note"],
        )
        for row in rows
    ]
    print_table(["ID", "Project ID", "Project", "Date", "Hours", "Note"], table_rows)
    return 0


def _handle_report_by_project(connection: sqlite3.Connection, args: argparse.Namespace) -> int:
    rows = reports.report_by_project(connection, from_date=args.from_date, to_date=args.to_date)
    table_rows = [
        (
            row["id"],
            row["name"],
            "active" if row["is_active"] else "archived",
            f"{float(row['total_hours']):.2f}",
        )
        for row in rows
    ]
    print_table(["ID", "Project", "Status", "Total Hours"], table_rows)
    return 0


def _handle_report_project(connection: sqlite3.Connection, args: argparse.Namespace) -> int:
    project, rows, total_hours = reports.report_for_project(
        connection,
        project_id=args.id,
        from_date=args.from_date,
        to_date=args.to_date,
    )
    print(f"Project {project['id']}: {project['name']}")
    print(f"Status: {'active' if project['is_active'] else 'archived'}")
    print(f"Total Hours: {total_hours:.2f}")
    print()
    table_rows = [
        (row["id"], row["entry_date"], f"{float(row['hours']):.2f}", row["note"])
        for row in rows
    ]
    print_table(["ID", "Date", "Hours", "Note"], table_rows)
    return 0
