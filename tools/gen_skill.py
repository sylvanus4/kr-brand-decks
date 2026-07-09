#!/usr/bin/env python3
"""gen_skill.py -- generate SKILL.md, brand.md, plugin.json for one company skill
from its palette.json + brand.json. Deterministic: format owned by code, so all
company skills stay consistent. Run per skill dir, or via tools/build_all.py.

Usage: python3 tools/gen_skill.py skills/deck-samsung-semi
"""
import json
import os
import sys

VERSION = "0.1.0"


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def skill_md(pal, br, nslides=6):
    slug = br["slug"]
    label = br["label"]
    ko = br["label_ko"]
    trig = br.get("triggers_ko", [])
    trig_str = ", ".join(f'"{t}"' for t in trig[:4])
    desc = (
        f"Generate a {label} ({ko}) brand-themed PPTX deck from a content spec, using "
        f"the verified {label} color palette (accent #{pal['accent']}) and reference-grade "
        f"native layouts (cover, TOC, section divider, Lucide icon grid, text+figure, "
        f"comparison table, gantt roadmap, KPI/impact charts, closing). "
        f"The model writes content; code owns all format. "
        f'Use when {trig_str}, "make a {label} deck", "{label} 브랜드 발표자료". '
        f"Do NOT use for a different company (use that company's deck-* skill) or a generic "
        f"template deck (use branded-deck / anthropic-pptx). Unofficial brand-inspired theme; "
        f"trademarks belong to {br['trademark_owner']}."
    )
    return f"""---
name: deck-{slug}
description: >-
  {desc}
---

# deck-{slug} — {label} ({ko}) 브랜드 데크

{br['tagline']}를 담은 **{label} 브랜드 테마 PPTX** 생성기. 검증된 브랜드 컬러와
네이티브 레퍼런스 레이아웃으로 제출급 데크를 만든다. 콘텐츠는 사용자가, 포맷(색·폰트·
레이아웃)은 코드가 소유한다.

## 팔레트 (검증)

| role | hex | role | hex |
|---|---|---|---|
| accent | `#{pal['accent']}` | bg | `#{pal['bg']}` |
| ink | `#{pal['ink']}` | surface | `#{pal['surface']}` |
| sub | `#{pal['sub']}` | border | `#{pal['border']}` |
| divider_bg | `#{pal['divider_bg']}` | divider_ink | `#{pal['divider_ink']}` |

출처·타이포·아트디렉션·상표 고지는 [`brand.md`](brand.md) 참조.

## 사용법

```bash
# 1) 내용만 편집 (포맷은 건드리지 않는다)
$EDITOR spec.sample.json

# 2) 렌더 (PPTX + PDF)
python3 ../../_engine/render_deck.py \\
  --palette palette.json --spec spec.sample.json \\
  --out examples/{slug}-6p.pptx --pdf

# 3) 검증 게이트 (PASS라야 배포)
python3 ../../_engine/validate.py examples/{slug}-6p.pptx \\
  --palette palette.json --expect-slides {nslides}
```

레이아웃: `cover · toc · divider · icongrid · textfigure · table · numbered · roadmap · kpi · closing`
(아이콘 = Lucide 라인 아이콘, 표·간트·임팩트 = 온브랜드 차트).
스펙 스키마와 공용 엔진은 리포 루트 `_engine/render_deck.py` docstring 참조.

> ⚠️ **비공식 브랜드 영감 테마입니다.** 본 스킬은 {label}과 제휴·보증 관계가 없으며,
> 상표·로고는 {br['trademark_owner']}의 자산입니다. 팔레트는 공개된 브랜드 컬러를
> 참고한 것이며 로고 파일은 포함하지 않습니다.
"""


def brand_md(pal, br):
    label = br["label"]
    return f"""# {label} — 브랜드 가이드 (비공식)

> 본 문서는 공개된 브랜드 자료를 참고한 **비공식 브랜드 테마** 정의입니다. 상표·로고는
> {br['trademark_owner']}의 자산이며, 본 리포는 로고 파일을 포함하지 않습니다.

## 컬러

| 역할 | HEX | 설명 |
|---|---|---|
| accent | `#{pal['accent']}` | 시그니처 브랜드 컬러 |
| divider_bg | `#{pal['divider_bg']}` | 커버·섹션 배경 (흰 텍스트 대비 확보) |
| ink | `#{pal['ink']}` | 제목 |
| sub | `#{pal['sub']}` | 본문 |
| muted | `#{pal['muted']}` | 캡션·페이지 번호 |
| surface | `#{pal['surface']}` | 패널 배경 |
| border | `#{pal['border']}` | 헤어라인 |
| bg | `#{pal['bg']}` | 슬라이드 배경 |

**출처**: {br['accent_source']}

## 타이포그래피

{br.get('font_note', 'Pretendard (무료) 권장, 대안 Noto Sans KR')}

## 히어로 이미지 아트디렉션 (선택)

`{br.get('art_direction', 'clean minimal tech illustration, no logos, no wordmarks')}`

AI 이미지는 옵션입니다. `OPENAI_API_KEY`가 설정된 경우에만 동작하며, 로고·워드마크는
생성하지 않습니다(브랜드 상표 보호).

## 상표 고지

{label}, 관련 로고 및 명칭은 {br['trademark_owner']}의 등록상표입니다. 본 테마는 팬메이드/
교육용 참고 자료로, 어떠한 공식 제휴·보증도 나타내지 않습니다.
"""


def plugin_json(pal, br):
    return {
        "name": f"deck-{br['slug']}",
        "description": f"{br['label']} ({br['label_ko']}) brand-themed PPTX deck generator (unofficial).",
        "version": VERSION,
        "author": {"name": "sylvanus4"},
        "homepage": "https://github.com/sylvanus4/kr-brand-decks",
        "repository": "https://github.com/sylvanus4/kr-brand-decks",
        "license": "MIT",
    }


def main():
    d = sys.argv[1].rstrip("/")
    pal = load(os.path.join(d, "palette.json"))
    br = load(os.path.join(d, "brand.json"))
    nslides = 6
    sp = os.path.join(d, "spec.sample.json")
    if os.path.exists(sp):
        nslides = len(load(sp).get("slides", [])) or 6
    with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(skill_md(pal, br, nslides))
    with open(os.path.join(d, "brand.md"), "w", encoding="utf-8") as f:
        f.write(brand_md(pal, br))
    os.makedirs(os.path.join(d, ".claude-plugin"), exist_ok=True)
    with open(os.path.join(d, ".claude-plugin", "plugin.json"), "w", encoding="utf-8") as f:
        json.dump(plugin_json(pal, br), f, ensure_ascii=False, indent=2)
    print(f"[gen] {d}: SKILL.md, brand.md, .claude-plugin/plugin.json")


if __name__ == "__main__":
    main()
