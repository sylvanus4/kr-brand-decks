#!/usr/bin/env python3
"""build_all.py -- build every company skill end to end.

For each of the 20 companies: write palette.json / brand.json / spec.sample.json
(flagships keep their hand-authored files), generate SKILL.md + brand.md + plugin.json,
render the 6-slide sample deck to PPTX + PDF + PNG previews, and validate it. Finally,
assemble .claude-plugin/marketplace.json from every plugin.json.

Usage: python3 tools/build_all.py [--no-pdf]
Run with any Python 3.10+ that has python-pptx, Pillow, matplotlib installed.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from brands_data import BRANDS, DEFAULT_PAL  # noqa: E402
from brands_rich import RICH  # noqa: E402

PY = sys.executable
ENGINE = os.path.join(REPO, "_engine")
SKILLS = os.path.join(REPO, "skills")
FLAGSHIPS = {"samsung-semi", "sk-hynix"}
PAL_KEYS = ("accent", "divider_bg", "divider_ink", "accent_ink", "on_accent",
            "ink", "sub", "muted", "surface", "border", "bg", "font")


def w(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def make_palette(slug, b):
    pal = dict(DEFAULT_PAL)
    pal["name"] = slug
    pal["label"] = b["label"]
    for k in PAL_KEYS:
        if k in b:
            pal[k] = b[k]
    pal["_source"] = (b["src"] +
                      " | Unofficial brand-inspired theme; trademarks belong to " + b["owner"])
    return pal


def make_brand(slug, b):
    return {
        "slug": slug, "label": b["label"], "label_ko": b["label_ko"],
        "tagline": b["tagline"],
        "triggers_ko": [f'{b["label_ko"]} 발표자료', f'{b["label"]} 덱',
                        f'{b["label_ko"]} 회사소개', f'{b["label"]} brand deck'],
        "art_direction": b["art"], "accent_source": b["src"],
        "font_note": b["font_note"], "trademark_owner": b["owner"],
    }


def make_spec(slug, b, r=None):
    """11-slide rich spec (icons + textfigure + comparison table + numbered + gantt)
    when rich content exists; otherwise a 6-slide basic spec."""
    ey = b["label"]
    closing = {"layout": "closing", "title": b["closing_title"], "subtitle": b["closing_sub"],
               "contact": f'brand-inspired sample deck · 상표는 {b["owner"]}의 자산입니다'}
    if not r:
        return {"meta": {"company": b["label_ko"], "eyebrow": ey}, "slides": [
            {"layout": "cover", "eyebrow": ey, "title": b["cover_title"], "subtitle": b["cover_sub"]},
            {"layout": "toc", "title": "Contents", "items": [["01", "회사 개요", "03"],
                ["02", "핵심 사업 영역", "04"], ["03", "성장 지표", "05"], ["04", "미래 비전", "06"]]},
            {"layout": "divider", "num": "01", "title": b["div_title"], "subtitle": b["div_sub"]},
            {"layout": "icongrid", "eyebrow": "Business Portfolio", "title": "핵심 사업 영역",
             "subtitle": b["div_sub"], "cols": 2, "cells": b["cells"]},
            {"layout": "kpi", "eyebrow": "Growth", "title": "성장 지표", "subtitle": b["tagline"],
             "metrics": b["kpi"], "note": "※ 수치는 브랜드 테마 디자인 예시입니다 (illustrative placeholder values)"},
            closing]}
    icons = r["icons"]
    cells = [[icons[i] if i < len(icons) else None, b["cells"][i][0], b["cells"][i][1]]
             for i in range(len(b["cells"]))]
    kw = [k.strip() for k in b["cover_sub"].replace("·", "|").split("|") if k.strip()][:4]
    return {"meta": {"company": b["label_ko"], "eyebrow": ey}, "slides": [
        {"layout": "cover", "eyebrow": ey, "title": b["cover_title"], "subtitle": b["cover_sub"]},
        {"layout": "toc", "eyebrow": ey, "title": "Contents", "items": [
            ["01", "사업 개요", "03"], ["02", "핵심 사업 영역", "05"], ["03", "성장 전략", "07"],
            ["04", "성장 로드맵", "09"], ["05", "미래 비전", "11"]]},
        {"layout": "divider", "num": "01", "title": "사업 개요", "subtitle": b["div_sub"]},
        {"layout": "textfigure", "eyebrow": "01 · 사업 개요", "title": f"{b['label_ko']}가 그리는 미래",
         "subtitle": b["tagline"],
         "items": [["Why · 시장의 변화", r["why"]], ["What · 사업 영역", b["tagline"]],
                   ["How · 실행 전략", r["how"]]],
         "panel_title": "핵심 지향", "panel_lede": b["tagline"], "panel_points": kw},
        {"layout": "divider", "num": "02", "title": "핵심 사업 영역", "subtitle": b["div_sub"]},
        {"layout": "icongrid", "eyebrow": "02 · 핵심 사업 영역", "title": "핵심 사업 영역",
         "subtitle": b["div_sub"], "cols": 2, "cells": cells},
        {"layout": "table", "eyebrow": "03 · 성장 전략", "title": "현재에서 확대 방향으로",
         "subtitle": "각 사업 영역의 현재와 확대 방향 (표기는 예시)",
         "headers": ["사업 영역", "현재", "확대 방향"], "rows": r["table"]},
        {"layout": "numbered", "eyebrow": "03 · 성장 전략", "title": "성장 전략 4대 축",
         "subtitle": b["tagline"], "lede": b["tagline"], "items": r["numbered"]},
        {"layout": "roadmap", "eyebrow": "04 · 성장 로드맵", "title": "성장 로드맵",
         "subtitle": "단계적 성장 전개 (일정은 브랜드 테마 예시)", "phases": r["roadmap"]},
        {"layout": "kpi", "eyebrow": "04 · 성장 로드맵", "title": "성장 지표", "subtitle": b["tagline"],
         "metrics": b["kpi"], "note": "※ 수치는 브랜드 테마 디자인 예시입니다 (illustrative placeholder values)"},
        closing]}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def main():
    make_pdf = "--no-pdf" not in sys.argv
    order = ["samsung-semi", "sk-hynix"] + [s for s in BRANDS if s not in FLAGSHIPS]
    rows = []
    for slug in order:
        d = os.path.join(SKILLS, f"deck-{slug}")
        os.makedirs(os.path.join(d, "examples"), exist_ok=True)
        if slug in BRANDS and slug not in FLAGSHIPS:
            b = BRANDS[slug]
            w(os.path.join(d, "palette.json"), make_palette(slug, b))
            w(os.path.join(d, "brand.json"), make_brand(slug, b))
            w(os.path.join(d, "spec.sample.json"), make_spec(slug, b, RICH.get(slug)))
        nslides = len(json.load(open(os.path.join(d, "spec.sample.json"), encoding="utf-8"))["slides"])
        # generate SKILL.md / brand.md / plugin.json
        subprocess.run([PY, os.path.join(HERE, "gen_skill.py"), d], check=True,
                       stdout=subprocess.DEVNULL)
        if slug in FLAGSHIPS:
            # flagships are maintained with hero images; do not clobber their examples
            rows.append((slug, "PASS", "flagship (kept, hero images)"))
            print(f"[PASS] deck-{slug} (kept)")
            continue
        # render
        out = os.path.join(d, "examples", f"{slug}-6p.pptx")
        cmd = [PY, os.path.join(ENGINE, "render_deck.py"),
               "--palette", os.path.join(d, "palette.json"),
               "--spec", os.path.join(d, "spec.sample.json"), "--out", out]
        if make_pdf:
            cmd.append("--pdf")
        rc, log = run(cmd)
        # validate
        vrc, vlog = run([PY, os.path.join(ENGINE, "validate.py"), out,
                         "--palette", os.path.join(d, "palette.json"),
                         "--expect-slides", str(nslides)])
        status = "PASS" if (rc == 0 and vrc == 0) else "FAIL"
        rows.append((slug, status, vlog.splitlines()[-1] if vlog else log[:60]))
        print(f"[{status}] deck-{slug}")
        if status == "FAIL":
            print("   ", log[-300:], "|", vlog[-200:])

    # marketplace.json
    plugins = []
    for slug in order:
        pj = os.path.join(SKILLS, f"deck-{slug}", ".claude-plugin", "plugin.json")
        with open(pj, encoding="utf-8") as f:
            p = json.load(f)
        plugins.append({"name": p["name"], "source": f"deck-{slug}",
                        "description": p["description"], "version": p["version"],
                        "author": p["author"]})
    market = {
        "name": "kr-brand-decks",
        "owner": {"name": "sylvanus4"},
        "metadata": {
            "description": "한국 주요 20개 기업 브랜드 테마 PPTX 데크 스킬 모음 (비공식). "
                           "Unofficial Korean-enterprise brand-themed PPTX deck skills.",
            "pluginRoot": "./skills",
        },
        "plugins": plugins,
    }
    os.makedirs(os.path.join(REPO, ".claude-plugin"), exist_ok=True)
    w(os.path.join(REPO, ".claude-plugin", "marketplace.json"), market)

    npass = sum(1 for _, s, _ in rows if s == "PASS")
    print(f"\n=== {npass}/{len(rows)} PASS · marketplace.json: {len(plugins)} plugins ===")
    for slug, s, note in rows:
        print(f"  {s:4}  deck-{slug:16}  {note}")
    sys.exit(0 if npass == len(rows) else 1)


if __name__ == "__main__":
    main()
