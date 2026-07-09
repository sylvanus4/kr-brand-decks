# kr-brand-decks

**한국 주요 20개 기업 브랜드 테마 PPTX 데크 스킬 모음** — Claude Code & Cursor용.
20 Claude Code / Cursor skills that generate polished, on-brand PowerPoint decks
themed after major Korean enterprises. Content is yours; the palette, layout, and
format are owned by code — so every deck comes out clean and consistent.

![Gallery of 20 brand cover slides](docs/gallery.png)

> ⚠️ **비공식(unofficial) 브랜드 영감 테마입니다.** 어떤 회사와도 제휴·보증 관계가 없으며,
> 상표·로고는 각 소유주의 자산입니다. 본 저장소는 **로고 파일을 포함하지 않고** 공개된 브랜드
> 컬러만 참고합니다. See [LICENSE](LICENSE) · [SECURITY.md](SECURITY.md).

---

## ✨ 무엇인가

- **20개 독립 스킬** — 회사마다 `deck-<company>` 스킬 하나. 검증된 브랜드 컬러 팔레트 + 레퍼런스급 네이티브 레이아웃(표지·목차·섹션·아이콘그리드·KPI 차트·클로징).
- **회사별 실제 6장 샘플 PDF** 동봉 — `skills/deck-<company>/examples/`.
- **템플릿 불필요** — python-pptx로 슬라이드를 처음부터 생성. 독점 템플릿·외부 서비스 의존 없음.
- **안전** — 100% 로컬 실행, 데이터 외부 전송 없음, API 키 불필요(선택적 AI 이미지 제외).

## 🚀 설치 (3가지 경로)

### A. Claude Code — `/plugin` 마켓플레이스 (권장)
```
/plugin marketplace add sylvanus4/kr-brand-decks
/plugin install deck-samsung-semi@kr-brand-decks
/plugin install deck-sk-hynix@kr-brand-decks
```
설치 후 Claude Code를 재시작하거나 `/reload-plugins`. 갱신: `/plugin marketplace update kr-brand-decks`.
원하는 회사 스킬만 골라 설치하면 됩니다.

### B. git clone + 로컬 스킬 (Claude Code / 수동)
```bash
git clone https://github.com/sylvanus4/kr-brand-decks.git
cd kr-brand-decks
./install.sh            # ~/.claude/skills 에 심링크 (원하는 스킬만 선택 가능)
```

### C. Cursor
```bash
git clone https://github.com/sylvanus4/kr-brand-decks.git
cp kr-brand-decks/.cursor/rules/kr-brand-decks.mdc  <your-project>/.cursor/rules/
```
Cursor의 Agent가 `.cursor/rules/kr-brand-decks.mdc`를 읽어 렌더 명령을 그대로 사용합니다.

### 사전 요구
- Python 3.10+ 와 `pip install python-pptx pillow matplotlib`
- PDF 내보내기(선택): LibreOffice(`soffice`)
- 한글 폰트 권장: [Pretendard](https://github.com/orioncactus/pretendard) (무료)

## 🧑‍💻 사용법

```bash
# 1) 회사 스킬 폴더에서 내용만 편집 (포맷은 건드리지 않는다)
cd skills/deck-samsung-semi
$EDITOR spec.sample.json

# 2) 렌더 (PPTX + PDF)
python3 ../../_engine/render_deck.py \
  --palette palette.json --spec spec.sample.json \
  --out examples/samsung-semi-6p.pptx --pdf

# 3) 품질 게이트 (PASS라야 배포)
python3 ../../_engine/validate.py examples/samsung-semi-6p.pptx \
  --palette palette.json --expect-slides 6
```

Claude Code / Cursor에서는 그냥 이렇게 말하면 됩니다:
> "삼성반도체 브랜드로 우리 제품 소개 6장 만들어줘" → `deck-samsung-semi` 스킬이 스펙을 채우고 렌더까지 수행.

### 레이아웃
`cover · toc · divider · icongrid · kpi · bullets · roadmap · closing` — 스펙 스키마는 [`_engine/render_deck.py`](_engine/render_deck.py) docstring 참조.

## 🏢 수록 기업 (20)

| 스킬 | 회사 | accent | 스킬 | 회사 | accent |
|---|---|---|---|---|---|
| `deck-samsung-semi` | 삼성전자 반도체 | `#1428A0` | `deck-doosan` | 두산 | `#0017A8` |
| `deck-sk-hynix` | SK하이닉스 | `#EA002C` | `deck-hanwha` | 한화 | `#F37321` |
| `deck-samsung-mobile` | 삼성전자 모바일 | `#1428A0` | `deck-nongshim` | 농심 | `#DF0029` |
| `deck-lg-electronics` | LG전자 | `#A50034` | `deck-sk-telecom` | SK텔레콤 | `#EA002C` |
| `deck-lg-energy` | LG에너지솔루션 | `#A50034` | `deck-celltrion` | 셀트리온 | `#50B848` |
| `deck-samsung-sdi` | 삼성SDI | `#1428A0` | `deck-kb-financial` | KB금융그룹 | `#FFBC00` |
| `deck-naver` | 네이버 | `#03C75A` | `deck-shinhan` | 신한금융그룹 | `#0046FF` |
| `deck-kakao` | 카카오 | `#FEE500` | `deck-cj-cheiljedang` | CJ제일제당 | `#EF151E` |
| `deck-hyundai-motor` | 현대자동차 | `#002C5F` | `deck-posco` | 포스코 | `#053080` |
| `deck-kia` | 기아 | `#EA0029` | `deck-hd-hyundai` | HD현대 | `#00AD1D` |

컬러 출처와 타이포·아트디렉션은 각 스킬의 `brand.md` 및 [BRANDS.md](BRANDS.md) 참조. 일부 값은
공식 페이지가 hex를 노출하지 않아 교차검증/추정이며, 각 `brand.md`에 신뢰 수준을 표기했습니다.

## 🔒 보안

100% 로컬, 데이터 외부 전송 없음, 코어 기능에 API 키 불필요. 보안 태세는 산문이 아니라
CI(gitleaks + pre-commit + 매니페스트 검증)로 강제합니다. 자세히 → [SECURITY.md](SECURITY.md).

## 🛠 동작 원리

```
palette.json (검증된 브랜드 색)  +  spec.json (당신의 내용)
        │
        ▼   _engine/render_deck.py  (python-pptx, 포맷은 코드가 소유)
   on-brand .pptx  →  (soffice)  →  .pdf
        │
        ▼   _engine/validate.py  (게이트: 슬라이드 수·accent 적용·lorem 없음)
```

모델은 **내용**만 쓰고, 코드가 **색·폰트·레이아웃**을 소유합니다. 그래서 저비용 모델로도
포맷이 흔들리지 않고 매번 제출급 결과가 나옵니다.

## 🤝 기여 / 회사 추가

새 회사 추가는 `tools/brands_data.py`에 항목 하나(검증된 accent + 사업 내용)만 넣고
`python3 tools/build_all.py`를 돌리면 스킬·샘플 PDF·매니페스트가 자동 생성됩니다.
로컬 체험: `python3 tools/validate_marketplace.py` 로 매니페스트 검증.

## 📄 라이선스

코드/템플릿은 [MIT](LICENSE). 브랜드명·컬러·상표는 각 소유주의 자산이며 식별·교육 목적의
비공식 참고입니다. 로고 파일은 포함하지 않습니다.
