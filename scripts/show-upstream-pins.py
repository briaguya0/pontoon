#!/usr/bin/env python3
"""
Print FetchContent / file(DOWNLOAD) pins that libultraship and SoH would
fetch at the given SoH ref. Output format matches show-manifest-pins.py
so the two can be compared via `diff(1)`.

Usage:
    scripts/show-upstream-pins.py <soh-ref>
    scripts/show-upstream-pins.py 9.2.3
    scripts/show-upstream-pins.py develop
"""

import re
import sys
import urllib.request as u

API = "https://api.github.com"
RAW = "https://raw.githubusercontent.com"

ref = sys.argv[1] if len(sys.argv) > 1 else sys.exit(f"usage: {sys.argv[0]} <soh-ref>")

lus_sha = re.search(
    r'"sha":\s*"([^"]+)"',
    u.urlopen(f"{API}/repos/HarbourMasters/Shipwright/contents/libultraship?ref={ref}").read().decode(),
)[1]

pins = []
for url in (
    f"{RAW}/kenix3/libultraship/{lus_sha}/cmake/dependencies/common.cmake",
    f"{RAW}/HarbourMasters/Shipwright/{ref}/soh/CMakeLists.txt",
):
    cmake = u.urlopen(url).read().decode()
    for m in re.finditer(
        r"FetchContent_Declare\s*\(\s*(\w+).*?GIT_REPOSITORY\s+(\S+).*?GIT_TAG\s+(\S+)",
        cmake, re.DOTALL,
    ):
        pins.append((m[1].lower(), m[3], m[2]))
    for m in re.finditer(r'file\(DOWNLOAD\s+"([^"]+)"', cmake):
        pins.append((m[1].rsplit("/", 1)[-1].lower(), "<file>", m[1]))

for name, ref_, url in sorted(pins):
    print(f"{name:16} {ref_:48} {url}")
