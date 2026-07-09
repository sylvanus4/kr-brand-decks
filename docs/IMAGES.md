# 히어로 이미지 (AI Image Generation)

표지·섹션 슬라이드에 브랜드 톤의 AI 생성 이미지를 넣어 데크를 한층 끌어올릴 수 있습니다.
**완전히 선택 사항**이며, 키가 없으면 자리표시자(placeholder)로 안전하게 대체됩니다.

플래그십 샘플(삼성반도체·SK하이닉스)의 표지가 이 방식으로 생성된 예시입니다.

## 1. OpenAI API 키 설정 (본인 키)

이미지 생성은 **본인의 OpenAI 키**로만 동작합니다. 이 저장소의 유일한 외부 통신입니다.

1. https://platform.openai.com/api-keys 에서 키 발급 (`sk-...`).
2. 환경변수로 설정:
   ```bash
   export OPENAI_API_KEY="sk-...여기에-본인-키..."
   # 영구 적용하려면 ~/.zshrc 또는 ~/.bashrc 에 추가
   ```
3. 라이브러리 설치:
   ```bash
   pip install openai pillow
   ```
4. 모델은 `--model`(기본 `gpt-image-1`)로 지정. 계정에서 사용 가능한 이미지 모델명을 쓰세요.

> 🔒 키는 **절대 커밋하지 마세요.** 저장소의 pre-commit(gitleaks) 훅이 키 유출을 커밋 단계에서
> 차단합니다. 자세히 → [../SECURITY.md](../SECURITY.md).

## 2. 이미지 계획(plan) 작성

```json
{
  "style_suffix": ", abstract brand-colored tech art, glowing accents, minimal cinematic, no text, no logo, no watermark",
  "size": "1024x1024",
  "quality": "high",
  "images": [
    { "slide": 1, "box_in": [8.25, 1.5, 4.55, 4.55], "prompt": "a silicon wafer with glowing blue data flows" }
  ]
}
```
- `box_in = [x, y, w, h]` — 인치 단위(슬라이드 13.333 × 7.5). 표지 오른쪽 빈 공간을 노려 배치.
- `slide` 는 1부터. `style_suffix` 는 모든 이미지에 공통 적용(브랜드 톤·"no logo/watermark" 유지).
- ⛔ 로고·워드마크는 프롬프트에서 항상 제외(상표 보호). 다크 표지에는 다크 배경 이미지를 요청.

## 3. 실행

```bash
# 키 있으면 생성, 없으면 자리표시자 (mode=auto 기본)
python3 _engine/place_images.py \
  --in skills/deck-samsung-semi/examples/samsung-semi-6p.pptx \
  --plan images.json \
  --out skills/deck-samsung-semi/examples/samsung-semi-6p.pptx \
  --palette skills/deck-samsung-semi/palette.json \
  --mode auto --model gpt-image-1

# PDF 재생성
soffice --headless --convert-to pdf --outdir <examples_dir> <deck>.pptx
```

`--mode` : `auto`(키 있으면 생성) · `generate`(강제 생성, 키 없으면 자리표시자+경고) ·
`placeholder`(생성 안 함, 배치만).

## 4. 동작 방식 (안전)

```
OPENAI_API_KEY 있음?
  ├─ 예 → OpenAI Images API 호출 → 이미지를 박스에 fit → 삽입
  └─ 아니오/실패 → 프롬프트가 적힌 X-박스 자리표시자를 그 자리에 배치 (빌드 중단 없음)
```

- 키가 없어도 파이프라인은 절대 멈추지 않습니다(자리표시자로 대체).
- 생성 이미지는 래스터라 팔레트 재색칠(restyle)의 영향을 받지 않습니다. 표지 텍스트와 겹치지
  않도록 `box_in`은 빈 공간에 두세요(표지 오른쪽 절반 권장).

## 비용 참고

이미지 생성은 OpenAI 사용량에 과금됩니다(본인 계정). 20개사 전부가 아니라 대표 몇 개만
히어로를 넣는 것을 권장합니다. 나머지는 깔끔한 텍스트 표지도 충분히 제출급입니다.
