#!/usr/bin/env bash
set -euo pipefail

: "${PARAVIEW_PATH:?PARAVIEW_PATH is not set}"

PYTHONPATH="$PARAVIEW_PATH/lib/python3.12/site-packages" \
"$PARAVIEW_PATH/bin/pvpython" \
  create_scene.py \
  --input VisualizationOutput/Output.vtpc.series \
  --freq 50 \
  --size 1600x1200 \
  --glyph-scale 2e-8
