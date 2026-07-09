# 기획 (Planning) — 내용을 주면 덱 구성을 결정한다

`tools/plan_deck.py`는 **내용 + 목적**만 받아서 (1) 목적에 맞는 비주얼 테마를 고르고,
(2) 섹션의 종류(`kind`)를 최적 레이아웃에 매핑하고, (3) 표지→목차→[섹션 디바이더+본문]→
클로징 순서로 슬라이드를 짜서 `spec.json`을 냅니다. 모델은 **내용만**, 구성(테마·구조·레이아웃
선택)은 코드가 결정합니다. 이것이 "기획 능력"입니다.

## 브리프 스키마

```json
{
  "topic": "AI 클라우드 사업 계획", "company": "ThakiCloud", "eyebrow": "THAKICLOUD",
  "purpose": "스타트업피치",           // 테마 자동선택 + 격식 판단에 사용
  "subtitle": "2026 성장 전략", "closing_title": "함께 만드는 AI 인프라", "contact": "...",
  "theme": "auto",                     // 또는 명시 테마명
  "sections": [
    {"title":"사업 개요", "kind":"story",     "items":[["Why · 시장","..."], ...]},
    {"title":"핵심 지표", "kind":"metrics",   "cards":[["3.0x","고객 성장","YoY"], ...]},
    {"title":"성장 로드맵","kind":"timeline",  "phases":[["MVP",2026.0,2026.6], ...]},
    {"title":"경쟁 전략", "kind":"steps",     "items":[["자동화","..."], ...]},
    {"title":"부문 비교", "kind":"compare",   "headers":[...], "rows":[[...], ...]},
    {"title":"사업 영역", "kind":"features",  "cells":[["cpu","제목","설명"], ...]},
    {"title":"실적 추이", "kind":"trend",     "labels":[...],"revenue":[...],"op":[...]},
    {"title":"부문 비중", "kind":"breakdown", "labels":[...],"values":[...],"unit":"조원"}
  ]
}
```

## 섹션 종류(kind) → 레이아웃

| kind | 레이아웃 | 쓰임 |
|---|---|---|
| `metrics` | bignum (KPI 카드) | 핵심 숫자 3~4개 |
| `kpi` | kpi (before/after 막대) | 현재→목표 지표 |
| `breakdown` | segment (가로 막대) | 부문/카테고리 비중 |
| `features` | icongrid (아이콘 2×2) | 사업/기능 나열 |
| `trend` | trend (매출막대+이익선) | 분기/연도 추이 |
| `compare` | table (비교표) | 현재 vs 차세대 등 |
| `steps` | numbered (01..N) | 전략 축·단계 |
| `timeline` | roadmap (간트) | 단계별 일정 |
| `story` | textfigure (텍스트+패널) | Why/What/How 서사 |
| `list` | bullets | 일반 목록 |

## 테마 자동선택

`purpose`를 각 테마의 `best_for`(themes.json)와 매칭해 최고 점수 테마를 고릅니다. **격식 목적**
(재무·IR·정부·데이터리포트·학술·이사회·M&A·컨설팅 …)은 `formal:true` 테마로 제한합니다.
예: `재무`→data-report/minimal-white, `스타트업피치`→startup-pitch, `제품소개`→keynote-product,
`교육`→academic/pastel. `--theme`로 강제 지정 가능.

## 실행

```bash
python3 tools/plan_deck.py brief.json --out spec.json        # [--theme NAME] [--no-dividers]
python3 _engine/render_deck.py --palette skills/deck-<회사>/palette.json \
  --spec spec.json --out deck.pptx --pdf
python3 _engine/validate.py deck.pptx --palette skills/deck-<회사>/palette.json --check-contrast
```

## 레이아웃 중복 회피

dashiAI 패턴을 차용해, 연속한 두 섹션이 같은 레이아웃(예: story 연속)이면 하나를 numbered로
회전시켜 단조로움을 줄입니다. 섹션마다 디바이더를 넣어 리듬을 만들며, `--no-dividers`로 끌 수
있습니다.
