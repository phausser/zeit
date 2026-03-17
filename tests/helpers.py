from __future__ import annotations

import io
import sys
import tempfile
import unittest
from contextlib import contextmanager
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from zeit import cli, db


class TempDatabaseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._temp_dir.cleanup)
        self.temp_path = Path(self._temp_dir.name)
        self.db_dir = self.temp_path / ".zeit"
        self.db_path = self.db_dir / "zeit.db"

        self._db_dir_patch = patch.object(db, "DB_DIR", self.db_dir)
        self._db_path_patch = patch.object(db, "DB_PATH", self.db_path)
        self._db_dir_patch.start()
        self._db_path_patch.start()
        self.addCleanup(self._db_dir_patch.stop)
        self.addCleanup(self._db_path_patch.stop)

    @contextmanager
    def make_connection(self):
        connection = db.get_connection()
        try:
            yield connection
        finally:
            connection.close()

    def run_cli(self, argv: list[str]) -> tuple[int, str]:
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = cli.run(argv)
        return exit_code, output.getvalue()
