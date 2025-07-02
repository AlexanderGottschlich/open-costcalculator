# Issue: Einführung von Ruff als einheitlichem Linter für Produktiv- und Testcode

## Ziel  
Ruff soll als zentraler Linter für das gesamte Repository eingeführt werden. Damit werden die bisherigen Tools (Flake8, isort, pycodestyle) abgelöst und einheitliche Code- und Teststil-Checks (inkl. pytest-spezifischer Regeln) sichergestellt. Ziel ist die Steigerung der Codequalität, Lesbarkeit und Wartbarkeit durch schnelle, einheitliche und skalierbare Linting-Checks.

## Anforderungen
- Ruff wird als einziger Linter für `src/` und `tests/` genutzt.
- Aktivierung von Ruff-Plugins für pytest (PT-Regeln), sodass Testcode konsistent und fehlerarm gestaltet wird.
- Entfernen von Flake8, isort und ggf. anderen überflüssigen Linting-Tools aus Requirements, CI und Pre-commit.
- Einbindung von Ruff als Pre-commit-Hook für lokalen Workflow.
- CI-Workflow ersetzt alle bisherigen Linting-Schritte durch Ruff.
- Konfiguration über `pyproject.toml`:
  - Linienlänge, Importsortierung, pytest-Regeln (PT)
  - Ausschluss von virtuellen Umgebungen und Build-Verzeichnissen

## Umsetzungshinweise
- Vorhandene Fehler/Meldungen in bestehendem Code beheben oder gezielt Regeln anpassen.
- Dokumentation/README um Ruff-Setup und Standard-Workflow ergänzen.
- Pre-commit-Hook-Konfiguration dokumentieren.

## Beispiel-Konfiguration

```toml
[tool.ruff]
line-length = 100
extend-select = ["PT"]  # pytest rules
exclude = ["venv", "build", "dist"]

[tool.ruff.lint.pytest]
enabled = true
```

## Test & Acceptance Criteria
- Ruff läuft fehlerfrei im Pre-commit und in der CI für alle relevanten Verzeichnisse.
- Tests und Produktivcode sind nach Ruff-Regeln vereinheitlicht.
- Bisherige Linter sind entfernt, die CI bleibt stabil und schnell.
- Entwickler können Ruff lokal und in der Pipeline gleichermaßen nutzen.

## Offene Fragen
- [ ] Sollen bestimmte Ruff-Regeln für Testcode deaktiviert oder angepasst werden?
- [ ] Gibt es individuelle Wünsche für Linelength, Namenskonventionen oder Importe?
- [ ] Ist ein auto-fix-Modus (z. B. vor jedem Commit) gewünscht?