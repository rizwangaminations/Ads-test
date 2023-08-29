#!/bin/sh
SCRIPT_DIR="$( dirname "$0" )"

python "$SCRIPT_DIR/../sync_from_parse.py" --json="$SCRIPT_DIR/sync_parse_config.json" --syncBonusGames=false
echo "Local data is synced with Parse"
