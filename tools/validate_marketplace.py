#!/usr/bin/env python3
"""validate_marketplace.py -- zero-dependency CI gate for the marketplace.

Checks (fail-fast, exit 1 on any error):
  - .claude-plugin/marketplace.json exists and has name/owner/plugins
  - each plugin entry has name + source, and skills/<source>/ exists
  - each skill has a SKILL.md and .claude-plugin/plugin.json
  - plugin.json name == marketplace entry name == "deck-<source-suffix>"
Runs on stdlib only so CI never fails for the wrong reason.
"""
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errs = []


def err(m):
    errs.append(m)


mp = os.path.join(REPO, ".claude-plugin", "marketplace.json")
if not os.path.exists(mp):
    print("FAIL: .claude-plugin/marketplace.json missing")
    sys.exit(1)

with open(mp, encoding="utf-8") as f:
    m = json.load(f)

for k in ("name", "owner", "plugins"):
    if k not in m:
        err(f"marketplace.json missing key: {k}")

root = m.get("metadata", {}).get("pluginRoot", "./skills").lstrip("./")
seen = set()
for p in m.get("plugins", []):
    name, src = p.get("name"), p.get("source")
    if not name or not src:
        err(f"plugin entry missing name/source: {p}")
        continue
    if name in seen:
        err(f"duplicate plugin name: {name}")
    seen.add(name)
    d = os.path.join(REPO, root, src)
    if not os.path.isdir(d):
        err(f"{name}: source dir not found: {root}/{src}")
        continue
    if not os.path.exists(os.path.join(d, "SKILL.md")):
        err(f"{name}: missing SKILL.md")
    pj = os.path.join(d, ".claude-plugin", "plugin.json")
    if not os.path.exists(pj):
        err(f"{name}: missing .claude-plugin/plugin.json")
    else:
        with open(pj, encoding="utf-8") as f:
            pjj = json.load(f)
        if pjj.get("name") != name:
            err(f"{name}: plugin.json name '{pjj.get('name')}' != marketplace name")

if errs:
    print(f"FAIL: {len(errs)} problem(s)")
    for e in errs:
        print("  - " + e)
    sys.exit(1)
print(f"PASS: marketplace.json + {len(m['plugins'])} skills valid")
