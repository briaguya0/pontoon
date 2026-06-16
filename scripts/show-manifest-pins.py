#!/usr/bin/env python3
"""
Print _fetchcontent/* pins from a Pontoon flatpak manifest. Output format
matches show-upstream-pins.py so the two can be compared via `diff(1)`.

Usage:
    scripts/show-manifest-pins.py soh/org.harbourmasters.soh.yml
"""

import sys
import yaml

manifest = sys.argv[1] if len(sys.argv) > 1 else sys.exit(f"usage: {sys.argv[0]} <manifest.yml>")

pins = []
for module in yaml.safe_load(open(manifest)).get("modules", []):
    if not isinstance(module, dict):
        continue
    for src in module.get("sources", []):
        dest = src.get("dest", "")
        if not dest.startswith("_fetchcontent"):
            continue
        url = src.get("url", "")
        if src.get("type") == "git":
            name = dest.split("/", 1)[1] if "/" in dest else dest
            ref = src.get("tag") or src.get("commit", "")
            pins.append((name.lower(), str(ref), url))
        elif src.get("type") == "file":
            pins.append((url.rsplit("/", 1)[-1].lower(), "<file>", url))

for name, ref, url in sorted(pins):
    print(f"{name:16} {ref:48} {url}")
