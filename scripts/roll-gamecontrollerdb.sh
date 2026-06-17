#!/bin/sh
# Stamp the sha256 of mdqinc/SDL_GameControllerDB master HEAD into a manifest's
# gamecontrollerdb.txt placeholder. Run before flatpak-builder so the nightly
# matches the rolling-master fetch in SoH CMake.
# Usage: scripts/roll-gamecontrollerdb.sh <manifest.yml>
set -eu

manifest=$1
hash=$(curl -sL https://raw.githubusercontent.com/mdqinc/SDL_GameControllerDB/master/gamecontrollerdb.txt | sha256sum | awk '{print $1}')
sed -i "s|sha256: PLACEHOLDER_GCDB_SHA256|sha256: $hash|" "$manifest"
echo "stamped gamecontrollerdb.txt sha256: $hash"
