#!/bin/sh
export SHIP_HOME="$XDG_DATA_HOME"
exec /app/lib/soh/soh.elf "$@"
