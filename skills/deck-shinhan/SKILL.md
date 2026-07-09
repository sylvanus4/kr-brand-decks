---
name: deck-shinhan
description: >-
  Generate a Shinhan Financial Group (신한금융그룹) brand-themed PPTX deck from a content spec, using the verified Shinhan Financial Group color palette (accent #0046FF) and reference-grade native layouts (cover, TOC, section divider, Lucide icon grid, text+figure, comparison table, gantt roadmap, KPI/impact charts, closing). The model writes content; code owns all format. Use when "신한금융그룹 발표자료", "Shinhan Financial Group 덱", "신한금융그룹 회사소개", "Shinhan Financial Group brand deck", "make a Shinhan Financial Group deck", "Shinhan Financial Group 브랜드 발표자료". Do NOT use for a different company (use that company's deck-* skill) or a generic template deck (use branded-deck / anthropic-pptx). Unofficial brand-inspired theme; trademarks belong to 신한금융그룹 (Shinhan Financial Group).
---

# deck-shinhan — Shinhan Financial Group (신한금융그룹) 브랜드 데크

은행·카드·증권을 잇는 리딩 금융 그룹를 담은 **Shinhan Financial Group 브랜드 테마 PPTX** 생성기. 검증된 브랜드 컬러와
네이티브 레퍼런스 레이아웃으로 제출급 데크를 만든다. 콘텐츠는 사용자가, 포맷(색·폰트·
레이아웃)은 코드가 소유한다.

## 팔레트 (검증)

| role | hex | role | hex |
|---|---|---|---|
| accent | `#0046FF` | bg | `#FFFFFF` |
| ink | `#1A1A1A` | surface | `#F5F6F8` |
| sub | `#4A4A4A` | border | `#E1E3E8` |
| divider_bg | `#0046FF` | divider_ink | `#FFFFFF` |

출처·타이포·아트디렉션·상표 고지는 [`brand.md`](brand.md) 참조.

## 사용법

```bash
# 1) 내용만 편집 (포맷은 건드리지 않는다)
$EDITOR spec.sample.json

# 2) 렌더 (PPTX + PDF)
python3 ../../_engine/render_deck.py \
  --palette palette.json --spec spec.sample.json \
  --out examples/shinhan-6p.pptx --pdf

# 3) 검증 게이트 (PASS라야 배포)
python3 ../../_engine/validate.py examples/shinhan-6p.pptx \
  --palette palette.json --expect-slides 11
```

레이아웃: `cover · toc · divider · icongrid · textfigure · table · numbered · roadmap · kpi · closing`
(아이콘 = Lucide 라인 아이콘, 표·간트·임팩트 = 온브랜드 차트).
스펙 스키마와 공용 엔진은 리포 루트 `_engine/render_deck.py` docstring 참조.

> ⚠️ **비공식 브랜드 영감 테마입니다.** 본 스킬은 Shinhan Financial Group과 제휴·보증 관계가 없으며,
> 상표·로고는 신한금융그룹 (Shinhan Financial Group)의 자산입니다. 팔레트는 공개된 브랜드 컬러를
> 참고한 것이며 로고 파일은 포함하지 않습니다.
