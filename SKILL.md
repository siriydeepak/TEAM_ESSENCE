# Email Parser Skill

I parse grocery receipt emails and add items to the pantry ledger.

## Capabilities
- **Receipt Parsing**: Convert receipt text into pantry item updates.
- **Inventory Updates**: Add parsed items to `pantry_ledger.yaml`.
- **Collision Alerts**: Surface conflicts when an item already exists in the pantry.

## Trigger Phrases
- "New receipt received"
- "Parse my grocery email"

## Execution
This skill runs the receipt parser and updates the pantry ledger via `ledger_handler.py`.

## Response_Template
`🚨 COLLISION: You already have {{item}} expiring on {{date}}. Confirm purchase?`
