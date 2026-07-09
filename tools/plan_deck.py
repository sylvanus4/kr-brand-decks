#!/usr/bin/env python3
"""plan_deck.py -- the PLANNING step: turn a content brief into a full deck spec.

Given a brief (topic, purpose, sections with a `kind`), this:
  1. picks a visual THEME by matching `purpose` against each theme's `best_for`
     (formal purposes are restricted to formal themes),
  2. maps each section's `kind` to the best LAYOUT,
  3. composes the slide sequence (cover -> toc -> [divider + content]* -> closing),
     auto-numbering the TOC/dividers/pages and avoiding back-to-back layout repeats,
  4. writes a spec.json ready for _engine/render_deck.py --palette <brand> --theme <t>.

So the model only supplies CONTENT + intent; the composition (theme + structure +
layout choice) is decided here. Deterministic (format owned by code).

Brief schema (JSON):
{
  "topic": "삼성전자 2026 2분기 실적", "eyebrow": "SAMSUNG", "company": "삼성전자",
  "purpose": "재무",            # matches themes.json best_for; drives theme + formality
  "subtitle": "...", "theme": "auto",   # or an explicit theme name
  "sections": [
    {"title":"실적 요약","kind":"metrics","cards":[["171조","매출","+129%"], ...]},
    {"title":"사업 부문","kind":"breakdown","labels":[...],"values":[...],"unit":"조원"},
    {"title":"핵심 사업","kind":"features","cells":[["memory-stick","DRAM","..."], ...]},
    {"title":"추세","kind":"trend","labels":[...],"revenue":[...],"op":[...]},
    {"title":"비교","kind":"compare","headers":[...],"rows":[[...], ...]},
    {"title":"전략","kind":"steps","items":[["축","설명"], ...]},
    {"title":"로드맵","kind":"timeline","phases":[["label",2026.0,2027.4], ...]},
    {"title":"개요","kind":"story","items":[["Why · ...","..."], ...]}
  ]
}
Usage: python3 tools/plan_deck.py brief.json --out spec.json [--theme NAME] [--no-dividers]
"""
import argparse
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
THEMES = os.path.join(REPO, "_engine", "themes.json")

# section kind -> content layout
KIND_LAYOUT = {
    "metrics": "bignum", "kpi": "kpi", "breakdown": "segment", "features": "icongrid",
    "trend": "trend", "compare": "table", "steps": "numbered", "timeline": "roadmap",
    "story": "textfigure", "list": "bullets",
}
# purposes that must use a formal (emoji-off) theme
FORMAL_PURPOSES = {"재무", "IR", "정부", "데이터리포트", "실적발표", "학술", "이사회",
                   "리서치", "정책보고", "M&A", "감사", "컨설팅"}


def pick_theme(purpose, want_formal):
    themes = json.load(open(THEMES, encoding="utf-8"))["themes"]
    best, best_score = "corporate-clean", -1
    for name, t in themes.items():
        if want_formal and not t.get("formal"):
            continue
        score = sum(1 for tag in t.get("best_for", []) if purpose and (purpose in tag or tag in purpose))
        if score > best_score:
            best, best_score = name, score
    return best


def content_slide(sec, eyebrow):
    """Map one section to a content-slide dict (layout + fields)."""
    kind = sec.get("kind", "list")
    layout = KIND_LAYOUT.get(kind, "bullets")
    base = {"layout": layout, "eyebrow": eyebrow, "title": sec["title"],
            "subtitle": sec.get("subtitle", "")}
    if layout == "bignum":
        base["cards"] = sec["cards"]
    elif layout == "kpi":
        base["metrics"] = sec["metrics"]; base["note"] = sec.get("note", "")
    elif layout == "segment":
        base.update(labels=sec["labels"], values=sec["values"], unit=sec.get("unit", ""))
    elif layout == "icongrid":
        base.update(cells=sec["cells"], cols=sec.get("cols", 2))
    elif layout == "trend":
        base.update(labels=sec["labels"], revenue=sec["revenue"], op=sec["op"],
                    unit=sec.get("unit", "조원"))
    elif layout == "table":
        base.update(headers=sec["headers"], rows=sec["rows"])
    elif layout == "numbered":
        base.update(items=sec["items"], lede=sec.get("lede", ""))
    elif layout == "roadmap":
        base["phases"] = sec["phases"]
    elif layout == "textfigure":
        base.update(items=sec["items"], panel_title=sec.get("panel_title", "핵심 지향"),
                    panel_lede=sec.get("panel_lede", sec.get("subtitle", "")),
                    panel_points=sec.get("panel_points", []))
    else:  # bullets
        base["items"] = sec.get("items", [])
    return base, layout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("brief")
    ap.add_argument("--out", required=True)
    ap.add_argument("--theme", help="override theme (default: auto by purpose)")
    ap.add_argument("--no-dividers", action="store_true", help="skip per-section dividers")
    args = ap.parse_args()

    b = json.load(open(args.brief, encoding="utf-8"))
    purpose = b.get("purpose", "일반")
    want_formal = purpose in FORMAL_PURPOSES
    theme = args.theme or (b.get("theme") if b.get("theme", "auto") != "auto" else None) \
        or pick_theme(purpose, want_formal)
    ey = b.get("eyebrow", b.get("company", ""))

    slides = [{"layout": "cover", "eyebrow": b.get("company", ey),
               "title": b["topic"], "subtitle": b.get("subtitle", "")}]

    secs = b["sections"]
    # page numbers: cover=1, toc=2, then each section = divider(optional)+content
    toc_items, page = [], 3
    for i, sec in enumerate(secs, 1):
        toc_items.append([f"{i:02d}", sec["title"], f"{page:02d}"])
        page += 1 if args.no_dividers else 2
    slides.append({"layout": "toc", "eyebrow": ey, "title": "Contents", "items": toc_items})

    prev_layout = None
    for i, sec in enumerate(secs, 1):
        if not args.no_dividers:
            slides.append({"layout": "divider", "num": f"{i:02d}", "title": sec["title"],
                           "subtitle": sec.get("subtitle", "")})
        cs, layout = content_slide(sec, f"{i:02d} · {sec['title']}")
        # avoid a content layout identical to the previous section's (rotate story<->numbered)
        if layout == prev_layout == "textfigure" and sec.get("items"):
            cs = {"layout": "numbered", "eyebrow": cs["eyebrow"], "title": cs["title"],
                  "subtitle": cs.get("subtitle", ""), "items": sec["items"]}
            layout = "numbered"
        slides.append(cs)
        prev_layout = layout

    slides.append({"layout": "closing", "title": b.get("closing_title", b["topic"]),
                   "subtitle": b.get("company", ey), "contact": b.get("contact", "")})

    spec = {"meta": {"company": b.get("company", ""), "eyebrow": ey, "theme": theme}, "slides": slides}
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    json.dump(spec, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"[plan] theme={theme} · {len(slides)} slides · purpose={purpose} -> {args.out}")


if __name__ == "__main__":
    main()
