# Group costs by Terraform tags

## Ziel
Analysiere und gruppiere AWS-Kosten nach Terraform-Tags (z.B. `project`, `team`, `environment`) für bessere Kostenübersicht.

## Features
- Gruppiere Ressourcen nach Tags
- Aggregiere Kosten pro Tag
- Unterstützte Tags: `project`, `team`, `environment`, `cost_center`, custom tags

## Konfiguration
Output format grouping:
```yaml
group_by: project  # oder team, environment, cost_center
```

## Output
- Gruppierte Tabelle nach Tag
- Separate Kosten pro Gruppe

## Implementation
- Extrahiere Tags aus Terraform-Plan
- Gruppiere Kosten in Dictionary
-輸出 gruppiert nach Tag