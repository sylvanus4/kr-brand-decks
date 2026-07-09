# 브랜드 리서치 & 출처 (Brand Research & Sources)

각 스킬의 팔레트는 아래 출처에서 확인/교차검증한 브랜드 컬러를 기반으로 합니다. 일부
기업은 공식 페이지가 hex를 텍스트로 노출하지 않아(이미지/PDF 자산에만 존재) 교차검증
또는 추정한 값이며, 신뢰 수준을 함께 표기합니다. **비공식 브랜드 영감 테마**이며 상표·로고는
각 소유주의 자산입니다. 로고 파일은 포함하지 않습니다.

신뢰 수준: ✅ 공식/다중교차확인 · 🟡 2차소스 교차 · ⚠️ 추정(공식 hex 미노출)

| 회사 | accent | divider_bg | 신뢰 | 근거 |
|---|---|---|---|---|
| 삼성전자 반도체 | `#1428A0` | `#0B1740` | ✅ | Samsung Blue, Pantone 286C. brandcolors·brandpalettes·designpieces 수렴 + Samsung SDI 공식 CI RGB(20,40,160) 일치 |
| SK하이닉스 | `#EA002C` | `#1A1A1A` | ✅ | SK Red, Pantone 186C. skhynix.com CI ↔ sk.co.kr 그룹 CI 일치 |
| 삼성전자 모바일 | `#1428A0` | `#000000` | ✅ | Samsung Blue + Galaxy near-black 관행 |
| LG전자 | `#A50034` | `#A50034` | ✅ | LG Heritage Red, Pantone 207C. lgensol.com CI RGB(165,0,52) 일치 |
| LG에너지솔루션 | `#A50034` | `#A50034` | ✅ | lgensol.com 공식 CI RGB(165,0,52) |
| 삼성SDI | `#1428A0` | `#1428A0` | ✅ | samsungsdi.com/about-sdi/ci.html RGB(20,40,160)/Pantone 286C |
| 네이버 | `#03C75A` | `#04371F` | ✅ | navercorp 브랜드가이드 HEX #03C75A. divider는 파생 다크그린(원색은 흰 텍스트 대비 부족) |
| 카카오 | `#FEE500` | `#191919` | ✅ | Kakao Yellow(옐로우엔 다크 텍스트 규정). divider는 near-black |
| 현대자동차 | `#002C5F` | `#002C5F` | ✅ | Hyundai Blue. hyundai.com CI + brandpalettes 교차 |
| 기아 | `#EA0029` | `#05141F` | ✅ | Kia Live Red + Midnight Black, 2021 리브랜드 CI |
| 포스코 | `#053080` | `#053080` | ✅ | POSCO Blue + Light Blue #00A5E5. posco.com CI |
| HD현대 | `#00AD1D` | `#003087` | ⚠️ | 2023 리브랜드 Heritage Green/Discovery Blue 추정(공식 hex 미확정) |
| 두산 | `#0017A8` | `#0017A8` | ✅ | Doosan Blue + Process Blue #0087CE. doosan.com CI |
| 한화 | `#F37321` | `#1B1B1B` | ✅ | Hanwha Orange. hanwha.com 브랜드 가이드 |
| 농심 | `#DF0029` | `#DF0029` | ✅ | eng.nongshim.com/about/ci 공식(흰 텍스트 대비 5:1) |
| SK텔레콤 | `#EA002C` | `#A8001F` | 🟡 | SK 그룹 레드 적용. divider는 대비 안전 위해 다크 조정 |
| 셀트리온 | `#50B848` | `#00552D` | 🟡 | 공식 6단계 그린 시스템(#96F0A5~#00552D). accent 근접 추정, divider 최암색 그린 ⚠️ 블루 아님 |
| KB금융그룹 | `#FFBC00` | `#2B2B2B` | ⚠️ | KB Yellow 대표컬러(정확 hex는 공식 다운로드 자산에만). 옐로우 divider 금지 → 차콜 |
| 신한금융그룹 | `#0046FF` | `#0046FF` | 🟡 | Shinhan Blue. shinhanci.co.kr + color-hex 교차(대비 6.3:1) |
| CJ제일제당 | `#EF151E` | `#A30F16` | ⚠️ | CJ Blossom Red(계열 CJ Logistics 공식값 준용, 전용 PDF 추출 실패). divider 다크 조정 |
| 업스테이지 | `#4D65FF` | `#4D65FF` | 🟡 | Upstage 블루바이올렛 — upstage.ai 웹 CSS 관찰값(공식 CI hex 미공개) |
| 토스 | `#0064FF` | `#0064FF` | 🟡 | Toss Blue — 널리 문서화된 브랜드색, 다수 소스 교차(공식 CI hex 미확정) |
| 엔씨소프트 | `#8243F2` | `#252628` | ⚠️ | NCSOFT 퍼플 — nc.com 'purple-square' 디자인시스템 CSS 관찰값(공식 CI 미확정). divider 다크 #252628 |

## 대비(접근성) 처리

밝은 accent(옐로우·그린·오렌지)는 흰 배경 텍스트 대비가 부족하므로 엔진이 두 역할을 분리합니다:
`accent_ink`(밝은 배경 위 텍스트용 어두운 변형)와 `on_accent`(accent 채움 위 텍스트색). 예:
카카오/KB 옐로우는 칩·텍스트에 다크 잉크, 네이버/셀트리온 그린은 어두운 그린 텍스트를 사용해
모든 슬라이드가 읽히도록 보장합니다.

## 타이포그래피

대부분 기업의 브랜드 전용서체는 사유(외부 라이선스 불가)이므로, 한글 데크 무료 대체로
**[Pretendard](https://github.com/orioncactus/pretendard)**(대안 Noto Sans KR)를 사용합니다.

## 면책

본 문서의 컬러 정보는 공개 자료 기반의 참고이며, 최신 공식 브랜드 가이드와 다를 수 있습니다.
정확한 브랜드 사용 규정은 각 기업의 공식 CI 가이드를 따르십시오.
