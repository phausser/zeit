Erstelle ein vollständiges Python-Projekt für eine kleine lokale CLI-Zeiterfassung.

Wichtige Vorgaben:
- Nur Python-Standardbibliothek
- Keine externen Dependencies
- SQLite nur über `sqlite3`
- CLI nur über `argparse`
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
- `main.py`
- `cli.py`
- `db.py`
- `schema.py`
- `projects.py`
- `time_entries.py`
- `reports.py`
- `utils.py`

Implementiere:
- saubere Validierung
- klare Fehlermeldungen
- tabellarische Konsolenausgabe
- type hints
- einfache, gut lesbare Struktur
- kein Overengineering

Zusätzlich:
- Erzeuge eine kurze `README.md`
- Zeige dort Installations-/Startbeispiele
- Zeige Beispielbefehle

Liefere den vollständigen Code aller Dateien.