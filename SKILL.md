# Collision Detection Skill

## Function
Acts as the "Anti-Waste" Guard. Triggered when a new email is parsed.

## Logic
Before you buy, the agent checks `pantry_ledger.yaml`. If you buy Milk but already have 1.5L, it sends a Telegram/WhatsApp alert using the OpenClaw `notify_user` protocol.

## Output
"Collision detected! You already have {item} that expires in {time}. Do you really need to buy more?"
