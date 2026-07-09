#!/usr/bin/env python3
"""validate_marketplace.py -- zero-dependency CI gate for the marketplace.

Checks (fail-fast, exit 1 on any error):
  - .claude-plugin/marketplace.json exists and has name/owner/plugins
  - each plugin entry has name + source; the source dir exists
  - the source dir has a .claude-plugin/plugin.json whose name matches the entry
  - the source dir contains at least one SKILL.md (directly or under skills/*/)
  - the shared engine (_engine/render_deck.py) is present inside the bundle source
Runs on stdlib only so CI never fails for the wrong reason.
"""
import glob
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

root = (m.get("metadata", {}).get("pluginRoot", ".") or ".").lstrip("./") or "."
seen = set()
total_skills = 0
for p in m.get("plugins", []):
    name, src = p.get("name"), p.get("source")
    if not name or not src:
        err(f"plugin entry missing name/source: {p}")
        continue
    if name in seen:
        err(f"duplicate plugin name: {name}")
    seen.add(name)
    d = REPO if src == "." else os.path.join(REPO, root, src)
    if not os.path.isdir(d):
        err(f"{name}: source dir not found: {src}")
        continue
    pj = os.path.join(d, ".claude-plugin", "plugin.json")
    if not os.path.exists(pj):
        err(f"{name}: missing .claude-plugin/plugin.json")
    else:
        with open(pj, encoding="utf-8") as f:
            if json.load(f).get("name") != name:
                err(f"{name}: plugin.json name != marketplace name")
    skills = glob.glob(os.path.join(d, "SKILL.md")) + \
        glob.glob(os.path.join(d, "skills", "*", "SKILL.md"))
    if not skills:
        err(f"{name}: no SKILL.md found under source")
    total_skills += len(skills)
    # bundle must carry the shared engine
    if not os.path.exists(os.path.join(d, "_engine", "render_deck.py")):
        err(f"{name}: shared engine _engine/render_deck.py not inside source "
            f"(skills would lose ../../_engine)")

if errs:
    print(f"FAIL: {len(errs)} problem(s)")
    for e in errs:
        print("  - " + e)
    sys.exit(1)
print(f"PASS: marketplace.json valid · {len(seen)} plugin(s) · {total_skills} skill(s)")
