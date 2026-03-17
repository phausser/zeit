from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Iterable, Sequence


class ValidationError(ValueError):
    """Raised when user input fails validation."""


class NotFoundError(ValueError):
    """Raised when a requested record does not exist."""


def now_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_date(value: str, *, field_name: str = "date") -> str:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValidationError(
            f"{field_name} must be a valid date in YYYY-MM-DD format."
        ) from exc
    return parsed.isoformat()


def parse_optional_date(value: str | None, *, field_name: str) -> str | None:
    if value is None:
        return None
    return parse_date(value, field_name=field_name)


def validate_project_name(name: str) -> str:
    cleaned = name.strip()
    if not cleaned:
        raise ValidationError("Project name must not be empty.")
    return cleaned


def validate_hours(hours: float) -> float:
    if hours <= 0 or hours > 24:
        raise ValidationError("Hours must be greater than 0 and less than or equal to 24.")
    return hours


def validate_date_range(from_date: str | None, to_date: str | None) -> tuple[str | None, str | None]:
    parsed_from = parse_optional_date(from_date, field_name="from") if from_date else None
    parsed_to = parse_optional_date(to_date, field_name="to") if to_date else None

    if parsed_from and parsed_to and parsed_from > parsed_to:
        raise ValidationError("'from' date must be earlier than or equal to 'to' date.")

    return parsed_from, parsed_to


def format_table(headers: Sequence[str], rows: Iterable[Sequence[object]]) -> str:
    materialized_rows = [[str(cell) for cell in row] for row in rows]
    widths = [len(header) for header in headers]

    for row in materialized_rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))

    def format_row(row: Sequence[str]) -> str:
        return "  ".join(value.ljust(widths[index]) for index, value in enumerate(row))

    lines = [
        format_row(headers),
        "  ".join("-" * width for width in widths),
    ]
    lines.extend(format_row(row) for row in materialized_rows)
    return "\n".join(lines)


def print_table(headers: Sequence[str], rows: Iterable[Sequence[object]]) -> None:
    materialized_rows = list(rows)
    if not materialized_rows:
        print("No results.")
        return
    print(format_table(headers, materialized_rows))
