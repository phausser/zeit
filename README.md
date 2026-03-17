# zeit

Kleine lokale CLI-Zeiterfassung in Python mit SQLite und nur Standardbibliothek.

## Voraussetzungen

- Python 3.11 oder neuer

## Start

```bash
chmod +x zeit
./zeit --help
```

Alternativ:

```bash
python3 main.py --help
```

Die Datenbank wird beim ersten Start automatisch unter `~/.zeit/zeit.db` angelegt.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

In GitHub werden die Tests außerdem automatisch per GitHub Actions bei Pushes und Pull Requests ausgeführt.

## Beispiele

```bash
./zeit project add "Kundenportal" --description "Interne Weiterentwicklung"
./zeit project list
./zeit time add --project 1 --date 2026-03-17 --hours 2.5 --note "Bugfixes"
./zeit time list --from 2026-03-01 --to 2026-03-31
./zeit report by-project --from 2026-03-01 --to 2026-03-31
./zeit report project 1
./zeit project archive 1
./zeit project activate 1
```
