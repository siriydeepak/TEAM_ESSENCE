# Utility Gap Finder Skill

I analyze expiring pantry items and suggest a low-cost, high-value ingredient to maximize usage.

## Capabilities
- **Expiry Detection**: Scan pantry inventory for items expiring in less than 48 hours.
- **Meal Suggestion**: Ask Gemini to propose one ingredient under $2 for a high-value meal.
- **Proactive Alerts**: Generate push-style suggestions for urgent food rescue.

## Execution
This skill calls `gap_finder.py` to inspect `pantry_ledger.yaml` and produce a proactive suggestion.

## Priority
Urgent

## Response_Template
`Proactive Suggestion: {{suggestion}}`
