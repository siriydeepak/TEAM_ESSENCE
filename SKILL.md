# Pantry Intel Skill

## Schema

This skill provides core intelligence for the AetherShelf autonomous agent, exposing three primary tools:

### 1. update_inventory
- **Description**: Ingests OCR/email parsed data and safely updates the `pantry_ledger.yaml`.
- **Inputs**: `item_name` (string), `quantity` (integer), `expiry_date` (string, optional).
- **Outputs**: Success status and any collision warnings.

### 2. predict_depletion
- **Description**: The core Autonomous Flux logic. Triggered automatically by the `file_watcher` when the ledger changes. Analyzes current stock and consumption flux to find "Utility Gaps."
- **Inputs**: `ledger_path` (string, optional).
- **Outputs**: Proactive `notify_user` alerts if items deplete in < 3 days.

### 3. generate_shopping_list
- **Description**: Compiles a comprehensive list of depleted or soon-to-be depleted items.
- **Inputs**: None.
- **Outputs**: Formatted shopping list array.
