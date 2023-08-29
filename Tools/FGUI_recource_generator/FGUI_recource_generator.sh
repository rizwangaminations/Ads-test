#!/bin/sh
SCRIPT_DIR="$( pwd )"

# Resource_Copy:
python "$SCRIPT_DIR/image_generator.py"

# Resource_Compression:
python "$SCRIPT_DIR/../image_compressor.py" -i="$SCRIPT_DIR"
echo Common Resource Compressed


