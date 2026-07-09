#!/usr/bin/env python3
"""render_html.py -- export the SAME spec+palette (+theme) as a self-contained HTML deck.

Gives the third format (HTML) alongside PPTX+PDF: a single .html file you can open in any
browser, edit in place (it's plain HTML/text), and print to PDF (Ctrl-P). No Node, no
build step, no external requests -- CSS is inlined, chart images are base64-embedded.
Agent-agnostic: only needs Python (+ matplotlib for chart slides, degrades to a table).

Usage: python3 render_html.py --palette PALETTE.json --spec SPEC.json --out deck.html [--theme NAME]

Covers: cover, toc, divider, icongrid, textfigure, table, numbered, bullets, kpi, bignum,
trend, segment, roadmap, closing. Chart layouts (kpi/trend/segment/roadmap) reuse charts.py.
"""
import argparse
import base64
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def esc(x):
    return html.escape(str(x)).replace("\n", "<br>")


def chart_uri(kind, **kw):
    import tempfile
    import charts
    p = os.path.join(tempfile.gettempdir(), f"_html_{kind}.png")
    fn = {"kpi": "kpi_bars", "trend": "trend_dual", "segment": "hbars",
          "roadmap": "roadmap"}[kind]
    getattr(charts, fn)(out=p, **kw)
    with open(p, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def css(pal, t):
    def c(k, d=None):
        return "#" + pal.get(k, d or "000000").lstrip("#")
    return f"""
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#3a3a3a;font-family:'Pretendard','Noto Sans KR',-apple-system,sans-serif}}
.slide{{position:relative;width:1280px;height:720px;margin:24px auto;background:{c('bg','FFFFFF')};
  overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.35)}}
.slide.dark{{background:{c('divider_bg')};color:{c('divider_ink','FFFFFF')}}}
.pad{{position:absolute;left:60px;right:60px;top:44px}}
.eyebrow{{font-size:15px;font-weight:700;letter-spacing:.12em;color:{c('accent')}}}
.dark .eyebrow{{color:{c('divider_ink','FFFFFF')}}}
.title{{font-size:34px;font-weight:800;color:{c('ink')};margin-top:14px}}
.dark .title{{color:{c('divider_ink','FFFFFF')}}}
.sub{{font-size:18px;color:{c('sub')};margin-top:10px}}
.dark .sub{{color:{c('divider_ink','FFFFFF')};opacity:.85}}
.tick{{width:74px;height:6px;background:{c('accent')};margin-top:22px}}
.rule{{height:1px;background:{c('border')};margin-top:14px}}
.cover-t{{position:absolute;left:60px;bottom:120px;right:60px;font-size:66px;font-weight:800;line-height:1.05;color:{c('divider_ink','FFFFFF')}}}
.cover-s{{position:absolute;left:60px;bottom:70px;font-size:20px;color:{c('divider_ink','FFFFFF')};opacity:.85}}
.grid{{position:absolute;left:60px;right:60px;top:250px;display:grid;grid-template-columns:1fr 1fr;gap:26px 60px}}
.cell h4{{font-size:20px;color:{c('ink')};font-weight:700;margin-bottom:8px}}
.cell p{{font-size:15px;color:{c('sub')};line-height:1.5}}
.chip{{display:inline-block;width:40px;height:40px;background:{c('accent')};color:{c('on_accent','FFFFFF')};
  border-radius:6px;text-align:center;line-height:40px;font-weight:800;margin-bottom:10px}}
table{{position:absolute;left:60px;right:60px;top:250px;border-collapse:collapse;width:calc(100% - 120px)}}
th{{text-align:left;font-size:18px;color:{c('ink')};padding:12px 8px;border-bottom:3px solid {c('accent')}}}
td{{font-size:16px;color:{c('ink')};padding:12px 8px;border-bottom:1px solid {c('border')}}}
td.sub{{color:{c('sub')}}}
.cards{{position:absolute;left:60px;right:60px;top:255px;display:flex;gap:22px}}
.card{{flex:1;background:{c('surface')};border-top:5px solid {c('accent')};padding:26px 22px}}
.card .lab{{font-size:15px;color:{c('sub')}}}
.card .val{{font-size:40px;font-weight:800;color:{c('ink')};margin-top:10px}}
.card .dl{{font-size:15px;font-weight:700;color:{c('accent')};margin-top:14px}}
.num{{position:absolute;left:60px;right:60px;top:255px}}
.num .row{{display:flex;gap:20px;margin-bottom:20px}}
.num .n{{font-size:28px;font-weight:800;color:{c('accent')};min-width:56px}}
.num h4{{font-size:19px;color:{c('ink')};font-weight:700}}
.num p{{font-size:15px;color:{c('sub')};margin-top:4px}}
.chart{{position:absolute;left:60px;right:60px;top:250px;width:calc(100% - 120px)}}
.chart img{{width:100%}}
.note{{position:absolute;left:60px;bottom:36px;font-size:13px;color:{c('muted')}}}
@media print{{body{{background:#fff}}.slide{{margin:0;box-shadow:none;page-break-after:always}}}}
"""


def head(sp, pal):
    ey = esc(sp.get("eyebrow", "")).upper()
    parts = ['<div class="pad">']
    if ey:
        parts.append(f'<div class="eyebrow">{ey}</div>')
    parts.append(f'<div class="title">{esc(sp["title"])}</div>')
    if sp.get("subtitle"):
        parts.append(f'<div class="sub">{esc(sp["subtitle"])}</div>')
    parts.append('<div class="tick"></div><div class="rule"></div></div>')
    return "".join(parts)


def slide_html(sp, pal, t):
    L = sp["layout"]
    if L == "cover":
        return (f'<section class="slide dark"><div class="pad"><div class="tick"></div>'
                f'<div class="eyebrow" style="margin-top:14px">{esc(sp.get("eyebrow","")).upper()}</div></div>'
                f'<div class="cover-t">{esc(sp["title"])}</div>'
                f'<div class="cover-s">{esc(sp.get("subtitle",""))}</div></section>')
    if L == "divider":
        return (f'<section class="slide dark"><div class="pad" style="top:300px">'
                f'<div class="eyebrow" style="font-size:44px">{esc(sp.get("num",""))}</div>'
                f'<div class="title" style="font-size:40px;margin-top:6px">{esc(sp["title"])}</div>'
                f'<div class="sub">{esc(sp.get("subtitle",""))}</div></div></section>')
    if L == "closing":
        return (f'<section class="slide dark"><div class="cover-t" style="bottom:200px">{esc(sp.get("title","Thank you"))}</div>'
                f'<div class="cover-s" style="bottom:150px">{esc(sp.get("subtitle",""))}</div>'
                f'<div class="note">{esc(sp.get("contact",""))}</div></section>')
    body = ""
    if L == "toc":
        rows = "".join(f'<tr><td style="width:70px;color:{"#"+pal["accent"]};font-weight:800">{esc(r[0])}</td>'
                       f'<td>{esc(r[1])}</td><td class="sub" style="text-align:right;width:60px">{esc(r[2] if len(r)>2 else "")}</td></tr>'
                       for r in sp["items"])
        body = f'<table>{rows}</table>'
    elif L == "icongrid":
        cells = "".join(f'<div class="cell"><div class="chip">{i+1}</div>'
                        f'<h4>{esc(c[-2])}</h4><p>{esc(c[-1])}</p></div>'
                        for i, c in enumerate(sp["cells"]))
        body = f'<div class="grid">{cells}</div>'
    elif L in ("numbered", "bullets"):
        rows = "".join(f'<div class="row"><div class="n">{i+1:02d}</div><div><h4>{esc(it[0])}</h4>'
                       f'<p>{esc(it[1])}</p></div></div>' for i, it in enumerate(sp["items"]))
        body = f'<div class="num">{rows}</div>'
    elif L == "textfigure":
        rows = "".join(f'<div style="margin-bottom:20px"><h4 style="font-size:19px;color:#{pal["ink"]};font-weight:700">{esc(it[0])}</h4>'
                       f'<p style="font-size:15px;color:#{pal["sub"]};margin-top:4px">{esc(it[1])}</p></div>' for it in sp["items"])
        body = f'<div style="position:absolute;left:60px;top:255px;width:560px">{rows}</div>'
    elif L == "table":
        th = "".join(f"<th>{esc(h)}</th>" for h in sp["headers"])
        trs = "".join("<tr>" + "".join(f'<td class="{"sub" if j==1 else ""}">{esc(cell)}</td>'
                      for j, cell in enumerate(r)) + "</tr>" for r in sp["rows"])
        body = f'<table><tr>{th}</tr>{trs}</table>'
    elif L == "bignum":
        cards = "".join(f'<div class="card"><div class="lab">{esc(c[1])}</div>'
                        f'<div class="val">{esc(c[0])}</div>'
                        + (f'<div class="dl">{esc(c[2])}</div>' if len(c) > 2 else "") + '</div>'
                        for c in sp["cards"])
        body = f'<div class="cards">{cards}</div>'
    elif L in ("kpi", "trend", "segment", "roadmap"):
        col = dict(ink="#" + pal["ink"], sub="#" + pal["sub"], muted="#" + pal["muted"],
                   accent="#" + pal["accent"], line="#" + pal["border"])
        try:
            if L == "kpi":
                uri = chart_uri("kpi", metrics=sp["metrics"], **col)
            elif L == "trend":
                uri = chart_uri("trend", labels=sp["labels"], revenue=sp["revenue"], op=sp["op"],
                                unit=sp.get("unit", "조원"), **col)
            elif L == "segment":
                uri = chart_uri("segment", labels=sp["labels"], values=sp["values"],
                                unit=sp.get("unit", "조원"), **col)
            else:
                uri = chart_uri("roadmap", phases=[tuple(p) for p in sp["phases"]], panel="#" + pal["surface"], **col)
            body = f'<div class="chart"><img src="{uri}"></div>'
        except Exception as e:
            body = f'<div class="chart"><p style="color:#{pal["sub"]}">[chart: {esc(e)}]</p></div>'
    note = f'<div class="note">{esc(sp["note"])}</div>' if sp.get("note") else ""
    return f'<section class="slide">{head(sp, pal)}{body}{note}</section>'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--palette", required=True)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--theme")
    args = ap.parse_args()
    pal = json.load(open(args.palette, encoding="utf-8"))
    spec = json.load(open(args.spec, encoding="utf-8"))
    t = {}
    ref = args.theme or spec.get("meta", {}).get("theme")
    if isinstance(ref, str):
        tf = os.path.join(HERE, "themes.json")
        if os.path.isfile(tf):
            t = json.load(open(tf, encoding="utf-8")).get("themes", {}).get(ref, {})
    elif isinstance(ref, dict):
        t = ref
    slides = "\n".join(slide_html(sl, pal, t) for sl in spec["slides"])
    title = esc(spec.get("meta", {}).get("company", "Deck"))
    out = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8">'
           f'<title>{title}</title><style>{css(pal, t)}</style></head>'
           f'<body>{slides}</body></html>')
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"[ok] {args.out}  ({len(spec['slides'])} slides, HTML)")


if __name__ == "__main__":
    main()
