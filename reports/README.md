# reports — 분기 실적 보고서 예시 (illustrative)

`kr-brand-decks` 엔진으로 만든 **분기 실적 보고서 데크 예시**입니다. 각 기업의 브랜드
팔레트 + 재무 차트 레이아웃(빅넘버 KPI 카드 · 연결손익 표 · 매출/영업이익 이중축 추세 ·
부문별 영업이익 막대)을 사용합니다.

| 파일 | 대상 | 분기 |
|---|---|---|
| `sk-hynix-2026Q1.*` | SK하이닉스 | 2026년 1분기 (확정) |
| `samsung-2026Q2.*` | 삼성전자 | 2026년 2분기 (잠정) |

## ⚠️ 고지

- **비공식(unofficial) 데모**입니다. 각 기업과 제휴·보증 관계가 없습니다.
- 수치는 **공개 보도·IR 자료 기반**이며, 각 데크의 마지막 장에 출처를 표기했습니다.
  잠정실적·부문별 추정·미공시 항목은 데크 본문에 명시했습니다.
- 투자 판단의 근거로 사용하지 마십시오. 정확한 수치는 각 사의 공식 IR 공시를 확인하십시오.
- 상표·로고는 각 소유주의 자산이며, 로고 파일은 포함하지 않습니다.

## 재현

```bash
python3 _engine/render_deck.py --palette skills/deck-sk-hynix/palette.json \
  --spec reports/sk-hynix-2026Q1.spec.json --out reports/sk-hynix-2026Q1.pptx --pdf
```

재무 차트 레이아웃(`bignum` · `trend` · `segment` · `table`)은 `_engine/render_deck.py`
docstring 및 `_engine/charts.py` 참조.
