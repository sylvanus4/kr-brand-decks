# 비주얼 테마 (24종)

**테마 = 시각 스타일**(타이포·표지/섹션 처리·accent·밀도·아이콘). **팔레트(브랜드 색)와 직교**
하므로, 같은 회사 색에 24가지 다른 룩을 입힐 수 있고, 같은 테마를 23개 브랜드 전체에 적용할
수도 있습니다. 정의: [`_engine/themes.json`](../_engine/themes.json).

## 사용

```bash
python3 _engine/render_deck.py --palette <brand>.json --spec <spec>.json --theme startup-pitch --out deck.pptx
```
또는 스펙 `meta.theme`에 이름을 넣으면 됩니다. 미지정 시 기본(corporate-clean 계열)으로 렌더.
[`tools/plan_deck.py`](../tools/plan_deck.py)는 `purpose`에 맞는 테마를 **자동 선택**합니다.

## 테마 파라미터 (팔레트 위에서 바뀌는 것)

`cover_style`(solid·minimal·band·sidebar) · `accent_style`(tick·underline·block·none) ·
`divider_style`(solid·minimal·huge) · `title_pt`/`cover_title_pt` · `cover_align`(left·center) ·
`content_bg`(bg·surface) · `hairline` · `eyebrow_upper` · `section_icons`/`card_icons`/`closing_mark` ·
`emoji`(3개 놀이형 테마만).

## 24종

FORMAL = 재무·IR·정부·데이터 안전(이모지 없음). CASUAL = 소셜·스타트업·교육·제품.

| 테마 | 한줄 | 톤 | 적합 |
|---|---|---|---|
| `corporate-clean` | 무난하고 흔들림 없는 기업 표준 | FORMAL | 기업소개·제안서·사내교육 |
| `minimal-white` | 여백이 콘텐츠다 — 프리미엄 미니멀 | FORMAL | 재무·IR·컨설팅 |
| `executive-dark` | 회의실의 무게감 | FORMAL | IR·이사회·M&A |
| `editorial-magazine` | 잡지를 넘기는 느낌 | FORMAL | 브랜드스토리·매거진 |
| `bold-brutalist` | 규칙을 깨는 확신 — 초대형 블록 | FORMAL | 디자인·컨퍼런스·런칭 |
| `swiss-grid` | 격자 위의 정직함 | FORMAL | 테크·디자인시스템·정부 |
| `tech-gradient` | 소프트웨어 제품의 광택 | CASUAL | 테크·SaaS·제품소개 |
| `pastel-soft` | 부드럽고 다정한 톤 | CASUAL | 소셜·웰니스·교육 |
| `mono-typographic` | 글자가 곧 이미지 | FORMAL | 컨셉·전략·아트디렉션 |
| `big-number` | 숫자가 주인공 | FORMAL | 데이터리포트·실적·성장지표 |
| `blueprint` | 설계도 위에 그리는 아이디어 | FORMAL | 엔지니어링·아키텍처·인프라 |
| `kraft-warm` | 손으로 만든 듯한 온기 | CASUAL | 로컬·F&B·라이프스타일 |
| `neon-dark` | 야간 도시의 에너지 | CASUAL | 게이밍·이벤트·Web3 |
| `playful-rounded` | 유쾌하고 접근하기 쉬움 | CASUAL | 소셜·교육·커뮤니티 |
| `data-report` | 숫자가 말하게 한다 | FORMAL | 재무·IR·데이터리포트·정부 |
| `keynote-product` | 제품 하나를 무대 위에 | FORMAL | 제품소개·테크런칭·하드웨어 |
| `academic` | 근거와 인용의 신뢰 | FORMAL | 교육·학술·정책 |
| `startup-pitch` | 빠르고 자신있게 | CASUAL | 스타트업피치·투자유치 |
| `luxury-serif` | 조용한 자신감 | FORMAL | 럭셔리·뷰티·프리미엄 |
| `geometric-bold` | 도형이 곧 메시지 | CASUAL | 브랜드·크리에이티브·이벤트 |
| `duotone` | 두 색으로 전부 말하기 | FORMAL | 브랜드캠페인·매거진·컨설팅 |
| `terminal-mono` | 개발자의 화면 | FORMAL | 테크·개발자·오픈소스 |
| `newsprint` | 오늘자 신문 1면 | FORMAL | 뉴스·미디어·정책요약 |
| `gradient-vibrant` | 에너지 넘치는 컬러 | CASUAL | 소셜·이벤트·크리에이터 |

## 시그니처 장식 (theme decorate)

일부 테마는 고유한 **배경 장식**을 그립니다(`decor` 태그, `_engine/render_deck.py`의
`theme_decorate`):
- `blueprint` — 좌표 그리드 + 코너 눈금(설계도 느낌)
- `terminal-mono` — 터미널 3닷 + `user@deck:~$ present ▮` 프롬프트
- `swiss-grid` — 노출된 세로 컬럼 그리드
- `neon-dark` — 얇은 accent 프레임(글로우 근사)
- `bold-brutalist` — 상·하단 굵은 accent 바
- `luxury-serif` — 인셋 헤어라인 프레임
- `newsprint` — 마스트헤드 룰 + 컬럼 구분선

> 참고: 폰트는 Pretendard 단일이라 세리프/모노/그라디언트/텍스처가 필요한 테마는 타이포·배치·
> accent·밀도·장식으로 **느낌을 근사**합니다(python-pptx 네이티브 도형 범위 내). 색은 팔레트가 소유.
