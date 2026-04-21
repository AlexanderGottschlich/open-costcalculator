# Compare Plans

## Ziel
Vergleiche zwei Terraform-Pläne und zeige die Kostendifferenz (delta cost analysis).

## Features
- Lade zwei Terraform-Pläne (before/after)
- Analysiere beide Pläne
- Berechne Differenz: Kosten(nach) - Kosten(vor)
- Zeige hinzugefügte, entfernte und geänderte Ressourcen

## CLI
```bash
python src/main.py --plan plan/after.tfplan.json --compare plan/before.tfplan.json
```

## Implementation
- Extrahiere Ressourcen aus beiden Plänen
- Vergleiche Ressourcen-Typen und Anzahl
- Berechne Kosten-Differenz
- Output: Tabelle mit Delta


## Konzept (vereinfacht)

```python
before_costs = analyze(plan1)
after_costs = analyze(plan2)
delta = after_costs - before_costs
```

## Kosten-Differenz Berechnung

1. **Neue Ressourcen**: nur in after → Kosten hinzugefügt
2. **Entfernte Ressourcen**: nur in before → Kosten entfernt
3. **Geänderte Ressourcen**: Typ/Größe geändert → Kostendifferenz