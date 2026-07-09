---
name: deck-kakao
description: >-
  Generate a Kakao (카카오) brand-themed PPTX deck from a content spec, using the verified Kakao color palette (accent #FEE500) and reference-grade native layouts (cover, TOC, section divider, icon grid, KPI chart, closing). The model writes content; code owns all format. Use when "카카오 발표자료", "Kakao 덱", "카카오 회사소개", "Kakao brand deck", "make a Kakao deck", "Kakao 브랜드 발표자료". Do NOT use for a different company (use that company's deck-* skill) or a generic template deck (use branded-deck / anthropic-pptx). Unofficial brand-inspired theme; trademarks belong to 카카오 (Kakao Corp.).
---

# deck-kakao — Kakao (카카오) 브랜드 데크

관계를 잇는 플랫폼으로 만드는 일상의 혁신를 담은 **Kakao 브랜드 테마 PPTX** 생성기. 검증된 브랜드 컬러와
네이티브 레퍼런스 레이아웃으로 제출급 데크를 만든다. 콘텐츠는 사용자가, 포맷(색·폰트·
레이아웃)은 코드가 소유한다.

## 팔레트 (검증)

| role | hex | role | hex |
|---|---|---|---|
| accent | `#FEE500` | bg | `#FFFFFF` |
| ink | `#1A1A1A` | surface | `#F5F6F8` |
| sub | `#4A4A4A` | border | `#E1E3E8` |
| divider_bg | `#191919` | divider_ink | `#FFFFFF` |

출처·타이포·아트디렉션·상표 고지는 [`brand.md`](brand.md) 참조.

## 사용법

```bash
# 1) 내용만 편집 (포맷은 건드리지 않는다)
$EDITOR spec.sample.json

# 2) 렌더 (PPTX + PDF)
python3 ../../_engine/render_deck.py \
  --palette palette.json --spec spec.sample.json \
  --out examples/kakao-6p.pptx --pdf

# 3) 검증 게이트 (PASS라야 배포)
python3 ../../_engine/validate.py examples/kakao-6p.pptx \
  --palette palette.json --expect-slides 6
```

레이아웃: `cover · toc · divider · icongrid · kpi · bullets · roadmap · closing`.
스펙 스키마와 공용 엔진은 리포 루트 `_engine/render_deck.py` docstring 참조.

> ⚠️ **비공식 브랜드 영감 테마입니다.** 본 스킬은 Kakao과 제휴·보증 관계가 없으며,
> 상표·로고는 카카오 (Kakao Corp.)의 자산입니다. 팔레트는 공개된 브랜드 컬러를
> 참고한 것이며 로고 파일은 포함하지 않습니다.
