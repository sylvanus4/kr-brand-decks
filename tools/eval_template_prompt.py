#!/usr/bin/env python3
"""eval_template_prompt.py -- the CREATIVITY GATE for AI template-image prompts.

Before spending an image-generation call, judge whether the prompt describes a genuinely
CREATIVE, distinctive slide-template background -- not a generic "professional abstract
gradient". Only prompts that pass the gate proceed to generation (used by
tools/creative_template.py). Returns JSON: {score, verdict, dims, feedback, improved_prompt}.

Two judges:
  - LLM judge (if OPENAI_API_KEY): scores on a rubric and rewrites a stronger prompt.
  - Heuristic fallback (no key / failure): rewards a concrete concept/metaphor, specific
    art-direction (medium, light, composition), brand-color reference, and legibility
    guidance; penalizes clichés ("professional background", "abstract", "corporate").

Usage:
  python3 tools/eval_template_prompt.py "a prompt ..." [--threshold 75] [--model gpt-4o-mini] [--json]
Exit 0 = PASS (score >= threshold), 3 = REVISE (below threshold), 1 = error.
"""
import argparse
import json
import os
import re
import sys

CLICHE = ["professional background", "abstract gradient", "corporate", "modern background",
          "clean minimalist background", "business background", "high quality", "4k", "8k",
          "beautiful", "nice", "simple background"]
STYLE_VOCAB = ["isometric", "cinematic", "watercolor", "blueprint", "neon", "duotone",
               "risograph", "collage", "papercut", "3d render", "line art", "low poly",
               "photographic", "long exposure", "bokeh", "double exposure", "gradient mesh",
               "editorial", "brutalist", "art deco", "bauhaus", "vaporwave", "glassmorphism",
               "topographic", "circuit", "wireframe", "aurora", "liquid metal", "origami"]
CONCEPT_CUES = ["like", "as if", "inspired by", "metaphor", "represent", "symboliz",
                "evokes", "shaped like", "made of", "transforming into", "network of",
                "flow of", "constellation", "landscape of"]
LEGIBILITY = ["lower third", "dark", "space for text", "negative space", "left side clear",
              "no text", "no logo", "no watermark"]


def heuristic(prompt):
    p = prompt.lower()
    dims = {}
    dims["specificity"] = min(25, len(re.findall(r"[a-z]+", p)) // 3 * 5)  # detail via length
    dims["concept"] = 25 if any(c in p for c in CONCEPT_CUES) else 8
    dims["style"] = min(20, 7 * sum(1 for s in STYLE_VOCAB if s in p))
    dims["brand"] = 15 if re.search(r"#([0-9a-f]{6})|palette|brand color|accent color", p) else 5
    dims["legibility"] = 15 if any(l in p for l in LEGIBILITY) else 4
    penalty = 8 * sum(1 for c in CLICHE if c in p)
    score = max(0, min(100, sum(dims.values()) - penalty))
    fb = []
    if dims["concept"] < 20:
        fb.append("구체적 컨셉/은유가 약함 — '무엇을 표현하는 배경인가'를 한 문장으로.")
    if dims["style"] < 14:
        fb.append("아트디렉션(매체·조명·구도) 형용사를 추가 (예: isometric, cinematic, papercut).")
    if dims["brand"] < 15:
        fb.append("브랜드 컬러(hex)를 명시해 팔레트와 조화시킬 것.")
    if dims["legibility"] < 15:
        fb.append("텍스트 가독성 — 'lower third darker', 'no text/logo'를 넣을 것.")
    if penalty:
        fb.append("클리셰 표현(professional/abstract/corporate) 제거.")
    return {"score": score, "verdict": "pass" if score >= 75 else "revise",
            "dims": dims, "feedback": " ".join(fb) or "충분히 구체적/창의적.",
            "improved_prompt": prompt, "judge": "heuristic"}


def llm(prompt, model):
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    rubric = (
        "You are a creative director judging a PROMPT for a slide-template BACKGROUND image. "
        "Score 0-100 on: concept originality (distinct visual idea/metaphor, not generic), "
        "art-direction specificity (medium, light, composition), brand fit (uses given colors), "
        "and legibility guidance (space/scrim for text, no text/logo). Reward bold, unusual, "
        "memorable concepts; penalize clichés (professional/abstract/corporate/gradient). "
        "Return ONLY JSON: {\"score\":int,\"verdict\":\"pass|revise\",\"dims\":{...},"
        "\"feedback\":\"<korean, 1-2 sentences>\",\"improved_prompt\":\"<a stronger, more creative rewrite>\"}."
    )
    r = client.chat.completions.create(
        model=model, temperature=0.4,
        messages=[{"role": "system", "content": rubric},
                  {"role": "user", "content": prompt}],
        response_format={"type": "json_object"})
    out = json.loads(r.choices[0].message.content)
    out["judge"] = model
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("--threshold", type=int, default=75)
    ap.add_argument("--model", default=os.environ.get("EVAL_MODEL", "gpt-4o-mini"))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    res = None
    if os.environ.get("OPENAI_API_KEY"):
        try:
            res = llm(args.prompt, args.model)
        except Exception as e:
            sys.stderr.write(f"[eval: LLM judge failed ({e}) -> heuristic]\n")
    if res is None:
        res = heuristic(args.prompt)
    res["pass"] = res.get("score", 0) >= args.threshold

    if args.json:
        print(json.dumps(res, ensure_ascii=False))
    else:
        print(f"score {res['score']} · {'PASS' if res['pass'] else 'REVISE'} "
              f"(judge={res['judge']})\n  {res.get('feedback','')}")
        if not res["pass"]:
            print(f"  개선안: {res.get('improved_prompt','')[:300]}")
    sys.exit(0 if res["pass"] else 3)


if __name__ == "__main__":
    main()
