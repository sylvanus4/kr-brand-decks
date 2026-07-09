# 새 회사 추가하기 (Add a company)

새 회사(홈페이지/브랜드)를 입력해 기존 20개사와 **동일한 방식**으로 브랜드 데크 스킬을
만드는 절차입니다. 색만 정하면 나머지(스킬 문서·6장 샘플·검증)는 코드가 만들어 줍니다.

## 1. 브랜드 색을 찾는다 (가장 중요)

정확한 **accent(대표색) hex** 하나가 핵심입니다. 순서대로 확인하세요.
1. 회사 공식 **CI / 브랜드 가이드** 페이지 (예: `<회사>.com/about/ci`) — 가장 정확.
2. 없으면 브랜드컬러 레퍼런스 교차확인: brandcolors.net, brandpalettes.com, brandcolorcode.com.
3. 홈페이지 로고/헤더 색을 스포이드로 추출(브라우저 개발자도구 → 색상 픽커).

> ⚠️ **밝은 색(노랑·연두·주황)** 이면 흰 배경 텍스트 대비가 부족합니다. 이때는 `--accent-ink`
> (밝은 배경 위 텍스트용 어두운 변형)와 `--divider-bg`(표지용, 흰 글씨가 읽히는 어두운 톤)를
> 함께 지정하세요. 생성기가 대비를 자동 검사해 경고합니다.

## 2. 한 줄로 스캐폴딩

```bash
python3 tools/new_company.py \
  --slug hyundai-mobis --label "Hyundai Mobis" --label-ko "현대모비스" \
  --accent 002C5F \
  --tagline "미래 모빌리티 부품·전동화 솔루션" \
  --owner "현대모비스 (Hyundai Mobis Co., Ltd.)" \
  --homepage https://www.mobis.co.kr
```

밝은 색 예시(가상):
```bash
python3 tools/new_company.py --slug foo --label "Foo" --label-ko "푸" \
  --accent FFCC00 --accent-ink 8A6A00 --divider-bg 2B2B2B --on-accent 191919 \
  --tagline "..." --owner "..."
```

생성되는 것: `skills/deck-<slug>/` 에 `palette.json · brand.json · spec.sample.json ·
SKILL.md · brand.md · .claude-plugin/plugin.json` + `examples/<slug>-6p.pdf` (검증 PASS까지).

## 3. 내용을 채운다

`skills/deck-<slug>/spec.sample.json`을 열어 **내용만** 편집합니다(색/폰트/레이아웃은 코드 소유):
- `cover.title` / `subtitle`, `divider`, `icongrid.cells`(사업 영역 4개), `kpi.metrics`, `closing`.
- 수치는 **실제 값**만. 없으면 `※ 예시` 라벨을 유지하세요(날조 금지).

## 4. 다시 렌더 · 검증

```bash
python3 _engine/render_deck.py --palette skills/deck-<slug>/palette.json \
  --spec skills/deck-<slug>/spec.sample.json --out skills/deck-<slug>/examples/<slug>-6p.pptx --pdf
python3 _engine/validate.py skills/deck-<slug>/examples/<slug>-6p.pptx \
  --palette skills/deck-<slug>/palette.json --expect-slides 6   # VERDICT: PASS 라야 함
```

## 5. (선택) 마켓플레이스에 포함

영구적으로 관리하려면 `tools/brands_data.py`에 항목을 추가하고 `python3 tools/build_all.py`를
실행하세요. 전 회사가 일괄 재생성되고 `.claude-plugin/marketplace.json`이 갱신됩니다.

## 6. (선택) 히어로 이미지 추가

표지/섹션에 AI 생성 이미지를 넣으려면 [IMAGES.md](IMAGES.md) 참조 (`OPENAI_API_KEY` 필요,
없으면 자리표시자로 안전하게 대체).

## 팁 — 색 신뢰수준을 정직하게

공식 hex를 못 찾고 추정했다면 `palette.json`의 `_source`와 `brand.md`에 "추정(unverified)"을
남기세요. 공개 저장소에서는 정직한 출처 표기가 신뢰를 만듭니다 ([BRANDS.md](../BRANDS.md) 참고).
