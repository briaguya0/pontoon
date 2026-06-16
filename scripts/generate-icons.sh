#!/bin/sh
# Resize a 1024x1024 source PNG into the hicolor sizes used by the manifest.
# Usage: scripts/generate-icons.sh <source.png> <out-dir> <app-id>
set -eu

src=$1
out=$2
id=$3

mkdir -p "$out"
for size in 16 32 64 128 256 512; do
  magick "$src" -resize "${size}x${size}" "$out/$id.${size}x${size}.png"
done
