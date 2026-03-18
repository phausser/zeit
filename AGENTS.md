# Repository Guidelines

## Project Structure & Module Organization
Application code lives under `src/zeit/`. Keep CLI wiring in `src/zeit/cli.py`, database setup in `src/zeit/db.py` and `src/zeit/schema.py`, and feature logic split by domain in `projects.py`, `time_entries.py`, and `reports.py`. The root `zeit` script is only a thin launcher. Tests live in `tests/` and are organized by feature, with shared helpers in `tests/helpers.py`. Reference docs are in `README.md` and `SPEC.md`.

## Build, Test, and Development Commands
Run the CLI locally with `./zeit --help` or `PYTHONPATH=src python3 -m zeit --help`. Execute the full test suite from the repository root with `python3 -m unittest discover -s tests -v`. Run a single test module while iterating, for example: `python3 -m unittest tests.test_reports -v`. CI runs the same test command on Python 3.11, 3.12, and 3.13.

## Coding Style & Naming Conventions
Target Python 3.11+ and the standard library only. Follow PEP 8 with 4-space indentation, readable line lengths, and grouped imports. Use type hints throughout, matching the existing codebase. Prefer small, direct functions over extra abstraction. Modules use `snake_case`; test files follow `tests/test_<feature>.py`; CLI handlers use `_handle_<area>_<action>` naming.

## Testing Guidelines
Use `unittest`, not third-party frameworks. Add or update tests for every behavior change, including validation and CLI output when relevant. Base new tests on `TempDatabaseTestCase` so they use an isolated temporary SQLite database instead of `~/.zeit/zeit.db`. Keep acceptance-style coverage in `tests/test_acceptance.py` for end-to-end CLI flows.

## Commit & Pull Request Guidelines
Recent history uses short conventional prefixes such as `test:`, `docs:`, `refactor:`, and `ci:`. Continue that style with concise, imperative subjects, for example `fix: validate archived project before insert`. Pull requests should describe the behavior change, mention test coverage, and link any related issue. Include sample CLI output when a change affects user-facing messages or tables.

## Security & Configuration Tips
Do not point tests at the real home-directory database. Preserve the default local database location `~/.zeit/zeit.db` for normal runtime behavior unless the task explicitly changes configuration handling.
