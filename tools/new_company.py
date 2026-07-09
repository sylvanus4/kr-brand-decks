#!/usr/bin/env python3
"""new_company.py -- scaffold a NEW company deck skill in one command.

Give it a slug, names, and the verified brand accent color; it writes palette.json,
brand.json, and an editable spec.sample.json, then generates SKILL.md/brand.md/
plugin.json, renders the 6-slide sample, and validates it. Then you edit the spec
content and re-render.

Example:
  python3 tools/new_company.py \
    --slug hyundai-mobis --label "Hyundai Mobis" --label-ko "현대모비스" \
    --accent 002C5F --homepage https://www.mobis.co.kr \
    --tagline "미래 모빌리티 부품·전동화 솔루션" \
    --owner "현대모비스 (Hyundai Mobis Co., Ltd.)"

Bright accent (yellow/green/orange)? Also pass --accent-ink <dark hex> so text on a
white background stays readable, and --divider-bg <dark hex> so cover text is readable.
The script warns you if it detects a low-contrast accent.
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from brands_data import DEFAULT_PAL  # noqa: E402


def luminance(hexstr):
    h = hexstr.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--label-ko", required=True)
    ap.add_argument("--accent", required=True, help="brand accent hex, e.g. EA002C")
    ap.add_argument("--divider-bg", help="cover/section bg hex (default: accent)")
    ap.add_argument("--divider-ink", default="FFFFFF")
    ap.add_argument("--accent-ink", help="dark variant for accent-colored TEXT on white")
    ap.add_argument("--on-accent", help="text color ON an accent fill (default divider_ink)")
    ap.add_argument("--secondary")
    ap.add_argument("--tagline", default="핵심 사업을 아우르는 종합 역량")
    ap.add_argument("--owner", default="해당 기업")
    ap.add_argument("--homepage", default="")
    ap.add_argument("--source", default="brand color provided by user (verify against official CI)")
    ap.add_argument("--interp", default=sys.executable, help="python to render with")
    args = ap.parse_args()

    slug = args.slug
    acc = args.accent.lstrip("#").upper()
    div = (args.divider_bg or acc).lstrip("#").upper()
    d = os.path.join(REPO, "skills", f"deck-{slug}")
    os.makedirs(os.path.join(d, "examples"), exist_ok=True)

    # contrast warnings
    if contrast(acc, "FFFFFF") < 3.0 and not args.accent_ink:
        print(f"⚠ accent #{acc} has low contrast on white ({contrast(acc,'FFFFFF'):.1f}:1). "
              f"Pass --accent-ink <dark hex> for readable eyebrow/number text.")
    if contrast(div, args.divider_ink) < 3.0:
        print(f"⚠ divider_bg #{div} vs divider_ink #{args.divider_ink} contrast is "
              f"{contrast(div, args.divider_ink):.1f}:1 (<3). Pick a darker --divider-bg.")

    pal = dict(DEFAULT_PAL)
    pal.update({"name": slug, "label": args.label, "accent": acc,
                "divider_bg": div, "divider_ink": args.divider_ink.lstrip("#").upper()})
    if args.accent_ink:
        pal["accent_ink"] = args.accent_ink.lstrip("#").upper()
    if args.on_accent:
        pal["on_accent"] = args.on_accent.lstrip("#").upper()
    if args.secondary:
        pal["secondary"] = args.secondary.lstrip("#").upper()
    pal["_source"] = args.source + f" | Unofficial brand-inspired theme; trademarks belong to {args.owner}"

    brand = {
        "slug": slug, "label": args.label, "label_ko": args.label_ko,
        "tagline": args.tagline,
        "triggers_ko": [f"{args.label_ko} 발표자료", f"{args.label} 덱",
                        f"{args.label_ko} 회사소개", f"{args.label} brand deck"],
        "art_direction": "clean minimal brand-colored illustration, no logos, no wordmarks",
        "accent_source": args.source + (f" · homepage: {args.homepage}" if args.homepage else ""),
        "font_note": "Pretendard 무료 폴백, 대안 Noto Sans KR",
        "trademark_owner": args.owner,
    }
    spec = {
        "meta": {"company": args.label_ko, "eyebrow": args.label},
        "slides": [
            {"layout": "cover", "eyebrow": args.label, "title": f"{args.label_ko}\n{args.tagline}",
             "subtitle": "편집하세요 — 부제"},
            {"layout": "toc", "title": "Contents",
             "items": [["01", "회사 개요", "03"], ["02", "핵심 사업 영역", "04"],
                       ["03", "성장 지표", "05"], ["04", "미래 비전", "06"]]},
            {"layout": "divider", "num": "01", "title": "핵심 사업 영역", "subtitle": args.tagline},
            {"layout": "icongrid", "eyebrow": "Business Portfolio", "title": "핵심 사업 영역",
             "subtitle": args.tagline, "cols": 2,
             "cells": [["사업 영역 1", "설명을 입력하세요."], ["사업 영역 2", "설명을 입력하세요."],
                       ["사업 영역 3", "설명을 입력하세요."], ["사업 영역 4", "설명을 입력하세요."]]},
            {"layout": "kpi", "eyebrow": "Growth", "title": "성장 지표", "subtitle": args.tagline,
             "metrics": [["지표 1", "기준", "+30%", 100, 130], ["지표 2", "기준", "2.0x", 100, 200],
                         ["지표 3", "기준", "+40%", 100, 140]],
             "note": "※ 수치는 브랜드 테마 디자인 예시입니다 (illustrative placeholder values)"},
            {"layout": "closing", "title": f"{args.label_ko}와 함께\n미래를 그립니다",
             "subtitle": args.label, "contact": f"brand-inspired sample deck · 상표는 {args.owner}의 자산입니다"},
        ],
    }

    def w(p, o):
        with open(p, "w", encoding="utf-8") as f:
            json.dump(o, f, ensure_ascii=False, indent=2)

    w(os.path.join(d, "palette.json"), pal)
    w(os.path.join(d, "brand.json"), brand)
    w(os.path.join(d, "spec.sample.json"), spec)
    subprocess.run([args.interp, os.path.join(HERE, "gen_skill.py"), d], check=True)
    out = os.path.join(d, "examples", f"{slug}-6p.pptx")
    subprocess.run([args.interp, os.path.join(REPO, "_engine", "render_deck.py"),
                    "--palette", os.path.join(d, "palette.json"),
                    "--spec", os.path.join(d, "spec.sample.json"), "--out", out, "--pdf"])
    subprocess.run([args.interp, os.path.join(REPO, "_engine", "validate.py"), out,
                    "--palette", os.path.join(d, "palette.json"), "--expect-slides", "6"])
    print(f"\n✅ deck-{slug} scaffolded. Next:")
    print(f"   1) edit skills/deck-{slug}/spec.sample.json  (cells/kpi/titles = your real content)")
    print(f"   2) re-render: python3 _engine/render_deck.py --palette skills/deck-{slug}/palette.json "
          f"--spec skills/deck-{slug}/spec.sample.json --out {out} --pdf")
    print(f"   3) (optional) add it to tools/brands_data.py and run tools/build_all.py to include in marketplace")


if __name__ == "__main__":
    main()
