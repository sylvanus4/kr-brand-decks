#!/usr/bin/env python3
"""creative_template.py -- full pipeline: creative prompt -> gate -> AI template image
-> assemble template -> render slides.

Instead of a solid-color theme, this generates a genuinely CREATIVE background image and
uses it as the deck template (cover + section dividers), keeping content slides clean for
legibility. Flow (each stage gated):

  1. Build an image prompt from your concept + the brand palette (colors, legibility rules).
  2. CREATIVITY GATE (tools/eval_template_prompt.py): only a distinctive prompt proceeds;
     a weak prompt is auto-rewritten once and re-judged, else the run stops with feedback.
  3. GENERATE the cover + divider background images (gpt-image-1, needs OPENAI_API_KEY).
  4. ASSEMBLE a spec where cover/dividers use bg_image; content stays on the brand palette.
  5. RENDER + VALIDATE the deck.

Usage:
  python3 tools/creative_template.py --palette skills/deck-samsung-semi/palette.json \
    --concept "silicon wafers dissolving into a night skyline of data" \
    --company "삼성전자 반도체" --out-dir out/creative/samsung-semi [--force] [--threshold 75]
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, "_engine"))
import eval_template_prompt as evalp  # noqa: E402


def build_prompt(concept, pal, variant=""):
    acc, ink, bg = pal["accent"], pal["ink"], pal["bg"]
    v = f" {variant}" if variant else ""
    return (f"{concept}.{v} A slide-template background: brand palette with accent #{acc}, "
            f"ink #{ink}, base #{bg}; cinematic depth and a distinct visual concept, generous "
            f"negative space with a darker lower third so caption text stays legible; "
            f"editorial art direction; no text, no logo, no watermark.")


def gate(prompt, threshold, model):
    if os.environ.get("OPENAI_API_KEY"):
        try:
            return evalp.llm(prompt, model)
        except Exception as e:
            sys.stderr.write(f"[gate: LLM judge failed ({e}) -> heuristic]\n")
    return evalp.heuristic(prompt)


def gen_image(prompt, out_png, size="1536x1024", model="gpt-image-1"):
    from openai import OpenAI
    import base64
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    r = client.images.generate(model=model, prompt=prompt, size=size, quality="high", n=1)
    with open(out_png, "wb") as f:
        f.write(base64.b64decode(r.data[0].b64_json))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--palette", required=True)
    ap.add_argument("--concept", required=True)
    ap.add_argument("--company", default="")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--threshold", type=int, default=75)
    ap.add_argument("--eval-model", default=os.environ.get("EVAL_MODEL", "gpt-4o-mini"))
    ap.add_argument("--image-model", default=os.environ.get("IMAGE_MODEL", "gpt-image-1"))
    ap.add_argument("--force", action="store_true", help="skip the creativity gate")
    ap.add_argument("--placeholder", action="store_true", help="skip generation (use placeholder)")
    args = ap.parse_args()

    pal = json.load(open(args.palette, encoding="utf-8"))
    os.makedirs(args.out_dir, exist_ok=True)
    prompt = build_prompt(args.concept, pal)

    # 2. creativity gate (auto-revise once)
    if not args.force:
        res = gate(prompt, args.threshold, args.eval_model)
        print(f"[gate] score {res['score']} · {res['verdict']} (judge={res['judge']})")
        print(f"       {res.get('feedback','')}")
        if res["score"] < args.threshold:
            imp = res.get("improved_prompt") or prompt
            print("[gate] revising with the stronger prompt and re-judging ...")
            res2 = gate(imp, args.threshold, args.eval_model)
            print(f"[gate] retry score {res2['score']} · {res2['verdict']}")
            if res2["score"] < args.threshold:
                print(f"[gate] BLOCKED — prompt not creative enough (score {res2['score']} "
                      f"< {args.threshold}). Improve the concept and retry, or use --force.")
                print(f"       개선안: {imp}")
                sys.exit(3)
            prompt = imp
        print(f"[gate] PASS. prompt:\n  {prompt}\n")

    # 3. generate cover + divider background images
    cover_png = os.path.join(args.out_dir, "cover-bg.png")
    div_png = os.path.join(args.out_dir, "divider-bg.png")
    if args.placeholder or not os.environ.get("OPENAI_API_KEY"):
        print("[gen] no key / --placeholder -> spec will use placeholder panels")
        cover_png = div_png = None
    else:
        print("[gen] generating cover background ...")
        gen_image(prompt, cover_png, model=args.image_model)
        print("[gen] generating divider background ...")
        gen_image(build_prompt(args.concept, pal, "a calmer, more minimal variant for section dividers"),
                  div_png, model=args.image_model)
        print(f"[gen] images -> {cover_png}, {div_png}")

    # 4. assemble a spec (reuse the brand's sample content if present)
    brand_dir = os.path.dirname(os.path.abspath(args.palette))
    sample = os.path.join(brand_dir, "spec.sample.json")
    if os.path.exists(sample):
        spec = json.load(open(sample, encoding="utf-8"))
        for sl in spec["slides"]:
            if sl["layout"] == "cover" and cover_png:
                sl["bg_image"] = cover_png
            elif sl["layout"] == "divider" and div_png:
                sl["bg_image"] = div_png
    else:
        co = args.company or "Company"
        spec = {"meta": {"company": co, "eyebrow": co}, "slides": [
            {"layout": "cover", "eyebrow": co, "title": args.concept[:40], "subtitle": co,
             **({"bg_image": cover_png} if cover_png else {})},
            {"layout": "toc", "title": "Contents", "items": [["01", "개요", "02"], ["02", "핵심", "03"]]},
            {"layout": "divider", "num": "01", "title": "개요", **({"bg_image": div_png} if div_png else {})},
            {"layout": "closing", "title": "Thank you", "subtitle": co}]}
    spec.setdefault("meta", {})["theme"] = spec.get("meta", {}).get("theme", "minimal-white")
    spec_out = os.path.join(args.out_dir, "spec.json")
    json.dump(spec, open(spec_out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # 5. render + validate
    out_pptx = os.path.join(args.out_dir, "deck.pptx")
    subprocess.run([sys.executable, os.path.join(REPO, "_engine", "render_deck.py"),
                    "--palette", args.palette, "--spec", spec_out, "--out", out_pptx, "--pdf"],
                   check=True)
    subprocess.run([sys.executable, os.path.join(REPO, "_engine", "validate.py"), out_pptx,
                    "--palette", args.palette])
    print(f"[ok] creative template deck -> {out_pptx}")


if __name__ == "__main__":
    main()
