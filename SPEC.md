Erstelle ein vollständiges Python-Projekt für eine kleine lokale CLI-Zeiterfassung.

Wichtige Vorgaben:
- Nur Python-Standardbibliothek
- Keine externen Dependencies
- SQLite nur über `sqlite3`
- CLI nur über `argparse`
- Tests nur mit Python-Standardbibliothek, z. B. `unittest`
- Python 3.11+
- Mehrere Dateien
- Sofort lauffähig

Features:
- Projekte anlegen, bearbeiten, archivieren, aktivieren, auflisten
- Zeiteinträge hinzufügen und auflisten
- Reports pro Projekt mit Summen
- Zeitraumfilter für Listen und Reports

CLI:
- `zeit project add <name> [--description TEXT]`
- `zeit project edit <id> [--name TEXT] [--description TEXT]`
- `zeit project list [--all]`
- `zeit project archive <id>`
- `zeit project activate <id>`
- `zeit time add --project <id> --date YYYY-MM-DD --hours FLOAT [--note TEXT]`
- `zeit time list [--project ID] [--from YYYY-MM-DD] [--to YYYY-MM-DD]`
- `zeit report by-project [--from YYYY-MM-DD] [--to YYYY-MM-DD]`
- `zeit report project <id> [--from YYYY-MM-DD] [--to YYYY-MM-DD]`

Datenbank:
- SQLite-Datei in `~/.zeit/zeit.db`
- Automatische Initialisierung beim ersten Start
- Foreign Keys aktivieren

Schema:
- `projects(id, name UNIQUE, description, is_active, created_at, updated_at)`
- `time_entries(id, project_id, entry_date, hours, note, created_at)`

Regeln:
- Projektname nicht leer und eindeutig
- Stunden > 0 und <= 24
- Datum muss gültig sein und Format `YYYY-MM-DD` haben
- Projekt muss existieren
- Archivierte Projekte dürfen keine neuen Zeiteinträge bekommen

Code-Struktur:
- `codex-zeit/`
- `.github/workflows/tests.yml`
- `src/zeit/__init__.py`
- `src/zeit/__main__.py`
- `src/zeit/cli.py`
- `src/zeit/db.py`
- `src/zeit/schema.py`
- `src/zeit/projects.py`
- `src/zeit/time_entries.py`
- `src/zeit/reports.py`
- `src/zeit/utils.py`
- `tests/__init__.py`
- `tests/helpers.py`
- `tests/test_projects.py`
- `tests/test_time_entries.py`
- `tests/test_reports.py`
- `tests/test_cli.py`
- `README.md`
- `SPEC.md`
- `zeit`

Verzeichnisstruktur:
- Der Python-Code für die Anwendung soll nicht im Projekt-Root liegen
- Lege den Anwendungscode unter `src/zeit/` ab
- Verwende package-relative Imports innerhalb von `src/zeit/`
- Das Root-Skript `zeit` dient nur als kleiner Einstiegspunkt und startet die CLI aus dem Paket

Tests:
- Erzeuge automatische Tests für jedes Feature
- Nutze nur Python-Standardbibliothek, z. B. `unittest`, `tempfile`, `subprocess`
- Lege die Tests in mehreren Dateien unter `tests/` ab
- Die Tests müssen ohne manuelle Vorbereitung ausführbar sein
- Die Tests dürfen nicht die echte Datei `~/.zeit/zeit.db` verändern
- Verwende für Tests eine temporäre SQLite-Datei oder ein isoliertes Test-Verzeichnis
- Teste sowohl Fachlogik als auch CLI-Verhalten

Mindestens abzudeckende Testfälle:
- Projekt anlegen
- Projekt mit Beschreibung anlegen
- Projekt bearbeiten
- Projekt auflisten
- Archivierte Projekte mit `--all` sehen
- Projekt archivieren
- Projekt wieder aktivieren
- Zeiteintrag hinzufügen
- Zeiteinträge mit Projektfilter auflisten
- Zeiteinträge mit Zeitraumfilter auflisten
- Report `by-project`
- Report für einzelnes Projekt
- Reports mit Zeitraumfilter
- Automatische Datenbank-Initialisierung beim ersten Start
- Foreign Keys sind aktiv

Validierungs- und Fehlerfälle, die automatisch getestet werden müssen:
- Leerer Projektname wird abgelehnt
- Doppelter Projektname wird abgelehnt
- Ungültiges Datum wird abgelehnt
- Falsches Datumsformat wird abgelehnt
- Stunden <= 0 werden abgelehnt
- Stunden > 24 werden abgelehnt
- Nicht existierendes Projekt wird abgelehnt
- Archiviertes Projekt darf keinen neuen Zeiteintrag erhalten
- Ungültiger Zeitraumfilter (`from` nach `to`) wird abgelehnt

Zusätzliche Dateien:
- `tests/test_projects.py`
- `tests/test_time_entries.py`
- `tests/test_reports.py`
- `tests/test_cli.py`
- Optional gemeinsame Hilfen in `tests/helpers.py`

Implementiere:
- saubere Validierung
- klare Fehlermeldungen
- tabellarische Konsolenausgabe
- type hints
- orientiere dich am Style Guide aus PEP 8 (`https://peps.python.org/pep-0008/`)
- achte insbesondere auf lesbare Benennung, konsistente Einrückung mit 4 Spaces, sinnvolle Leerzeilen, saubere Import-Gruppierung und gut umbrechbare Zeilen
- der Code soll maximal verständlich sein
- priorisiere Klarheit und Nachvollziehbarkeit vor Kürze, Abstraktion oder cleveren Patterns
- Funktionen und Module sollen klein, direkt und leicht lesbar bleiben
- verwende nur so viel Abstraktion wie für diese kleine Anwendung wirklich nötig ist
- schreibe Code so, dass auch Python-Einsteiger die Struktur schnell verstehen können
- bevorzuge gut lesbaren, konsistenten Code statt cleverer, unnötig komplexer Konstruktionen
- einfache, gut lesbare Struktur
- kein Overengineering

Zusätzlich:
- Erzeuge eine kurze `README.md`
- Zeige dort Installations-/Startbeispiele
- Zeige Beispielbefehle
- Ergänze im `README.md`, wie die Tests ausgeführt werden, z. B. `python -m unittest`

Liefere den vollständigen Code aller Dateien.
