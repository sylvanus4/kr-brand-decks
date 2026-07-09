---
name: creative-template
description: >-
  Generate a CREATIVE AI template-background image, gate it for creativity, and build a
  branded deck that uses the image on the cover + section dividers (content stays clean).
  Use when "창의적인 ppt 템플릿", "AI로 템플릿 이미지 만들어서 슬라이드", "generate a creative
  slide template", "이미지 배경 템플릿 덱". Needs OPENAI_API_KEY for generation (degrades to
  placeholder). Do NOT use for solid-color themed decks (use render_deck.py --theme) or for
  filling an existing .pptx (use tools/fill_template.py). Unofficial brand-inspired themes.
---

# creative-template — AI 생성 창의 템플릿 → 슬라이드 파이프라인

솔리드 컬러 테마가 "평범"할 때, **gpt-image로 창의적인 배경 이미지를 생성**해 덱의 표지·섹션
디바이더 템플릿으로 쓰고 슬라이드를 만든다. 콘텐츠 슬라이드는 가독성을 위해 브랜드 팔레트로
유지한다("이미지=분위기, 텍스트=정보"). 창의성이 부족한 프롬프트는 **게이트에서 차단**된다.

## 파이프라인 (각 단계 게이트)

```
컨셉(concept) 입력
   │
   ▼  1. 프롬프트 구성 = concept + 브랜드 팔레트(hex) + 가독성 규칙(darker lower third, no text/logo)
   ▼  2. 창의성 게이트 (tools/eval_template_prompt.py) — 점수 < 임계면 자동 1회 개선 후 재심사, 그래도 미달이면 중단
   ▼  3. 생성 (gpt-image-1): cover-bg.png + divider-bg.png  (OPENAI_API_KEY 필요)
   ▼  4. 조립: 표지·디바이더 slide에 bg_image 주입, 콘텐츠는 브랜드 팔레트 유지
   ▼  5. 렌더 + 검증 (render_deck.py / validate.py)
```

## 사용

```bash
export OPENAI_API_KEY="sk-..."     # 본인 키
python3 tools/creative_template.py \
  --palette skills/deck-samsung-semi/palette.json \
  --concept "silicon wafers dissolving into a nighttime city skyline of glowing data streams, isometric cinematic, darker lower third" \
  --company "삼성전자 반도체" --out-dir out/creative/samsung-semi
# 산출: out/creative/samsung-semi/ 에 cover-bg.png · divider-bg.png · spec.json · deck.pptx · deck.pdf
```

- `--threshold 75` 창의성 임계(기본 75) · `--force` 게이트 건너뜀 · `--placeholder` 생성 없이 자리표시자
- 게이트만 단독: `python3 tools/eval_template_prompt.py "<프롬프트>" --json`

## 창의성 게이트 (eval_template_prompt.py)

프롬프트를 **컨셉 독창성·아트디렉션 구체성·브랜드 적합·가독성 가이드**로 채점(0~100).
`OPENAI_API_KEY`가 chat 모델에 접근 가능하면 **LLM 심판**(루브릭 + 더 강한 프롬프트 재작성),
아니면 **휴리스틱**(클리셰 감점, 컨셉/스타일/브랜드/가독성 가점)으로 폴백. 임계 미달이면 생성
비용을 쓰기 전에 차단하고 개선안을 제시한다([[close-the-agent-loop]] verify-gate 동형).

## 엔진 연동

표지·섹션 디바이더 slide에 `"bg_image": "<png>"`가 있으면 엔진이 **cover-fit 풀블리드 + 하단
캡션 밴드 + 타이틀 오버레이**(imagefull 스타일)로 렌더한다. 콘텐츠 레이아웃은 그대로 팔레트 사용.

## 상표 고지

브랜드명·컬러·상표는 각 소유주 자산. AI 이미지는 **로고·워드마크 없이** 생성(프롬프트에 no
logo/no watermark 강제). 비공식 팬메이드/교육용.
