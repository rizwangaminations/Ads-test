#!/bin/sh
SCRIPT_DIR="$( dirname "$0" )"

python "$SCRIPT_DIR/copy_parse_tables.py" --json="$SCRIPT_DIR/copy_config.json"
echo "Local data is synced with Parse"
