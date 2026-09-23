# Italia Roadtrip ZTL Simulator

이탈리아 렌트카 여행(2026-10-06 ~ 10-12) 경로를 지도 위에 재생하고, 각 구간이 ZTL(통행제한구역)에 진입하는지와 진입 시각 기준 활성 여부를 판정하는 단일 페이지 앱.

- 라이브: https://alcain-jje.github.io/italy-roadtrip-sim/
- 여행 계획: https://alcain-jje.github.io/italy-roadtrip-sim/plan.html

## 구성
| 파일 | 역할 |
|---|---|
| `index.html` | Leaflet + turf.js + OSRM 데모 라우팅. 설정은 상단 `CONFIG` |
| `ztl_data.js` | 공식/OSM ZTL 폴리곤 22개 (`build_ztl.py`로 생성) |
| `build_ztl.py` | `data/` 원천 → `ztl_data.js`. 스케줄 규칙 상단 `S_*` |
| `data/` | 원천 GeoJSON (Roma RSM ArcGIS · Comune di Firenze · OSM Overpass) |
| `PLAN.md` / `plan.html` | 일자별 여행 계획 (md → html 변환) |
| `BRIEF.md` | 설계 결정·데이터 출처·변경 이력 |

## 판정 규칙
- 경로 폴리라인이 ZTL 폴리곤(경계 25 m 내측 버퍼)과 교차하면 진입.
- 진입 시각 = 출발 시각 + (진입 지점까지 거리 / 총 거리) × OSRM 소요 시간.
- 운영 시간(요일·시각) 규칙으로 활성이면 위반(빨강), 비활성이면 주황.

## 데이터 출처 / 라이선스
- Roma Servizi per la Mobilità Open Data (CC-BY 3.0 IT)
- Comune di Firenze Open Data — ZTL diurna (CC-BY 4.0)
- OpenStreetMap contributors (ODbL) — Milano Area C/B, Roma 야간 ZTL 등
- 라우팅: OSRM 공개 데모 서버 · 타일: OpenStreetMap

Siena·Pienza·Amalfi·Napoli·Bologna 폴리곤은 수작업 근사치이며 법적 효력이 없습니다. 현장 표지판을 우선하세요.
