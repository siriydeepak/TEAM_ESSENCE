#!/bin/bash

echo "=================================================="
echo "[AetherShelf Demo Mode] Initializing..."
echo "=================================================="

# 1. Force the OpenClaw Gateway to reload skills
echo -e "\n>>> [OpenClaw Gateway] Reloading skills (pantry_intel.skill)..."
# In a real environment, this invokes the gateway reload
# openclaw-cli gateway reload --skills pantry_intel.skill
sleep 1
echo "✅ Skills reloaded successfully."

# 2. Inject mock invoice into the parser
echo -e "\n>>> [AetherShelf] Injecting mock invoice: '1L Milk, 500g Spinach'"
# openclaw-cli trigger invoke EmailParser.skill --mock-payload '{"receipt": "1L Milk, 500g Spinach", "source": "demo_invoice"}'
sleep 1
echo "✅ Mock invoice processed. File Watcher triggered."

# 3. Stream Reasoning Logs
echo -e "\n>>> [OpenClaw Gateway] Streaming internal reasoning logs to terminal..."
echo "--- Chain of Thought (openclaw_session.log) ---"
# Create mock log entry to demonstrate the flow
echo "[CoT] Detected change in pantry_ledger.yaml via file_watcher" >> openclaw_session.log
echo "[CoT] Executing pantry_intel.skill.predict_depletion()" >> openclaw_session.log
echo "[CoT] Analyzing consumption flux... Milk expires in 2 days" >> openclaw_session.log
echo "[CoT] Triggering notify_user protocol: Sending alert via linked provider." >> openclaw_session.log

tail -f openclaw_session.log
