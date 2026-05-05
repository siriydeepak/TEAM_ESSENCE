#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EMAIL_PARSER_SKILL="$ROOT_DIR/EmailParser.skill"
FLUX_SKILL="$ROOT_DIR/FluxAlgorithm.skill"
GAP_SKILL="$ROOT_DIR/UtilityGapFinder.skill"

echo "Registering EmailParser skill..."
openclaw skills register "$EMAIL_PARSER_SKILL" --trigger webhook

echo "Registering FluxAlgorithm skill..."
openclaw skills register "$FLUX_SKILL" --trigger heartbeat --schedule daily

echo "Writing gateway_config.yaml..."
cat > "$ROOT_DIR/gateway_config.yaml" <<'EOF'
project_root: .
openclaw_runtime: local
skills:
  - name: EmailParser
    path: ./skills/pantry_manager/EmailParser.skill
    trigger: webhook
  - name: FluxAlgorithm
    path: ./skills/pantry_manager/FluxAlgorithm.skill
    trigger: heartbeat
    schedule: daily
EOF

echo "Registration complete. gateway_config.yaml created at $ROOT_DIR/gateway_config.yaml."
