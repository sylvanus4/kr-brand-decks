#!/usr/bin/env python3
"""validate.py -- deterministic quality gate for a rendered deck.

Exit 0 = PASS, non-zero = FAIL. Checks: file opens, expected slide count,
the brand accent color actually appears in the deck XML, and no leftover
placeholder/lorem text. Run before publishing any example deck.

Usage:
  python3 validate.py deck.pptx --palette palette.json --expect-slides 6
"""
import argparse
import json
import sys
import re
from pptx import Presentation

LOREM = re.compile(r"lorem ipsum|\{\{.*?\}\}|\bTODO\b|xxxx", re.IGNORECASE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("--palette")
    ap.add_argument("--expect-slides", type=int)
    args = ap.parse_args()

    fails = []
    try:
        prs = Presentation(args.deck)
    except Exception as e:
        print(f"FAIL: cannot open deck: {e}")
        sys.exit(1)

    n = len(prs.slides._sldIdLst)
    if args.expect_slides and n != args.expect_slides:
        fails.append(f"slide count {n} != expected {args.expect_slides}")

    # gather all text
    texts = []
    for s in prs.slides:
        for sh in s.shapes:
            if sh.has_text_frame:
                texts.append(sh.text_frame.text)
    blob = "\n".join(texts)
    if LOREM.search(blob):
        fails.append("placeholder/lorem text found")
    if not blob.strip():
        fails.append("deck has no text")

    # accent color present in XML?
    if args.palette:
        with open(args.palette, encoding="utf-8") as f:
            pal = json.load(f)
        accent = pal.get("accent", "").lstrip("#").upper()
        import zipfile
        xml = ""
        with zipfile.ZipFile(args.deck) as z:
            for nm in z.namelist():
                if nm.startswith("ppt/slides/slide") and nm.endswith(".xml"):
                    xml += z.read(nm).decode("utf-8", "ignore").upper()
        if accent and accent not in xml:
            fails.append(f"accent {accent} not found in slide XML")

    if fails:
        print("VERDICT: FAIL")
        for f in fails:
            print("  - " + f)
        sys.exit(1)
    print(f"VERDICT: PASS ({n} slides, accent applied, no lorem)")


if __name__ == "__main__":
    main()
