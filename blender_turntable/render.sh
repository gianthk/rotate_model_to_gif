#!/bin/bash
# Example: render one model as a 360-degree turntable, then make the GIF and MP4.
# usage: bash render.sh path/to/model.obj out/model [light]
#
# BLENDER: path to the Blender executable, e.g.
#   macOS:  /Applications/Blender.app/Contents/MacOS/Blender
#   Linux:  ./blender-4.2.3-linux-x64/blender
set -e
BLENDER=${BLENDER:-blender}
OBJ=$1
OUT=$2
LIGHT=${3:-1.0}

# --tilt 90 0 0 stands the Kiri models upright; --elev 8 = camera 8 degrees above the model
"$BLENDER" -b -P turntable.py -- --obj "$OBJ" --out "$OUT" --tilt 90 0 0 --elev 8 \
    --frames 240 --size 800 --samples 64 --light "$LIGHT"

python make_gif.py "$OUT" --fps 24 --step 2 --gif-size 600
