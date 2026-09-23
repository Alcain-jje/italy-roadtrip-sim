# 이탈리아 렌트카 ZTL 회피 경로 시뮬레이터 — 요청 초안 (2026-09-08)

> 용도: 다음 세션(Fable)에 그대로 붙여 넣는 요청문. 미확정 항목 없음(2026-09-08 확정).

## 1. 한 줄 목표
10/6~10/12 이탈리아 렌트카 여행의 일자별 이동 경로를 지도 위에 애니메이션으로 재생하고,
ZTL(통행제한구역) 폴리곤을 겹쳐 보여 "경로가 ZTL을 통과하는지"를 자동 판정하는 단일 HTML 파일.

## 2. 핵심 원칙 (Fable이 재발견하지 않도록 미리 확정)
- ZTL 회피는 "라우팅"보다 "주차 지점 선택" 문제다. 도시 간 이동은 고속도로라 ZTL을 안 지난다.
  → 각 목적지마다 **ZTL 밖 주차장 좌표**를 웨이포인트로 잡고, 그 사이를 라우팅한다.
- 라우팅 엔진: OSRM 공개 데모 서버(`router.project-osrm.org`, 키 불필요) 사용.
  openrouteservice의 avoid_polygons는 무료 구간 제한(구간 150km, 폴리곤 20km/200km²)이라 장거리 구간에 부적합 → 쓰지 말 것.
- ZTL 판정: 경로 폴리라인 ∩ ZTL 폴리곤 (turf.js `booleanIntersects`). 교차 시 해당 구간 빨간색 + 경고.
- ZTL 폴리곤은 정확한 공식 데이터를 처음부터 다 넣지 말고, 우선 **주요 도심 근사 폴리곤(수작업 5~10점)**으로 시작. 정밀화는 2단계.
- 스택: Leaflet 1.9 + turf.js (cdnjs) + OSM 타일. 빌드 도구 없음, 파일 1개.

## 3. 일정·숙소 (확정)
| 날짜 | 요일 | 이동/체류 | 숙소(밤) | 좌표(근사) |
|---|---|---|---|---|
| 10/4~10/6 | 일~화 | 로마 체류(대중교통) | hu Roma Camping in Town, Via Aurelia 831, 00165 Roma | 41.8868, 12.4061 |
| 10/6 | 화 | Hertz 로마 테르미니역 지점(Via Giolitti 34, 41.8989, 12.5033) 픽업 → 캠핑장 주차. 테르미니→Via Aurelia는 ZTL Centro Storico 남쪽 우회(Viale Trastevere·Gianicolense 경유) | 동일 | |
| 10/7 | 수 | 로마 → 푸로레(아말피) | La Vigna di Bacco, Via G.B. Lama 9, 84010 Furore (무료 주차, 주차장에서 계단 아래) | 40.6203, 14.5488 |
| 10/8 | 목 | 숙소 거점 → 포지타노 → 아말피 (라벨로 제외) | 동일 | |
| 10/9 | 금 | 푸로레 → 토스카나 남부 | Antico Casale L'Impostino, Loc. Impostino, Casal di Pari, Civitella Marittima | 43.023671, 11.307418 |
| 10/10 | 토 | 피엔차 → 시에나 경유 → 피렌체 (방문지 잠정, 변경 가능) | hu Firenze Camping in Town, Via Generale C.A. dalla Chiesa 1/3, 50136 Firenze | 43.7652, 11.3074 (Rovezzano, A1 Firenze Sud 인근) |
| 10/11 | 일 | 피렌체 체류(차 캠핑장 주차, 이동 없음) | 동일 | |
| 10/12 | 월 | 피렌체 → Hertz 밀라노 중앙역 지점(Piazza Luigi di Savoia, 45.4850, 9.2048) 반납 | 밀라노 중앙역 근처(미정) | 45.4866, 9.2045 (Centrale) |
| 10/13 | 화 | 출국 | | |

## 4. 구간별 라우팅 지침
- 10/7 로마→푸로레: A1 → A3(나폴리 우회) → Castellammare 출구 → **SS366 아제롤라 고개 → 푸로레**.
  SS163 해안도로(소렌토·포지타노 경유)는 시간·정체 때문에 피한다. (포지타노 시내 ZTL 주의)
- 10/8 아말피 일주: 푸로레 → 포지타노 → 아말피 → 푸로레(SS163 왕복). 홀짝제는 10월엔 **토·일에만** 적용 → 목요일이라 해당 없음. 포지타노·아말피 도심 ZTL은 주차장(Positano: Di Gennaro/Mandara 등 SS163 위 유료주차, Amalfi: Luna Rossa 등)까지만 진입.
- 10/9 푸로레→치비텔라 마리티마: A3 → A1 북상 → Orvieto/Chiusi 출구 → SS2/SP 지방도. 중간 경유 후보: 폼페이(주차장 밖에서), 오르비에토(푸니쿨라 주차장).
- 10/10 토스카나: 치비텔라 → 피엔차(마을 입구 무료 주차장) → 시에나(**Stadio/Il Campo/Santa Caterina 주차장**까지만) → 피렌체. 피렌체 진입 시 hu Firenze는 ZTL 밖(Campo di Marte 동쪽) → A1 Firenze Sud 출구 → Viale Europa 경로로 ZTL 미통과.
- 10/12 피렌체→밀라노: A1 직행 약 300km. 밀라노 Area C(Bastioni 내부, 월~금 7:30~19:30 유료)는 **미진입**. Centrale은 Area B 안·Area C 밖. Area B는 저공해 차량 통행 가능(렌트카는 통상 문제없음)이지만 표시는 해둔다.

## 5. ZTL 폴리곤 대상 (1단계: 근사 수작업 / 2단계: 공식데이터)
- 로마 Centro Storico ZTL (Tridente 포함) — 2단계 출처: Roma Servizi per la Mobilità 데이터셋(GeoServices REST)
- 피렌체 ZTL diurna(A~O 섹터) — 2단계 출처: opendata.comune.fi.it "ZTL diurna" (SHP/KMZ)
- 밀라노 Area C + Area B — 2단계 출처: dati.comune.milano.it `ds51_disciplina_aree.geojson`
- 시에나, 포지타노, 아말피, 피엔차, 몬탈치노, 산지미냐노 — 1단계 근사만(작아서 충분)
- 참고: ztlitaly.com 도시별 지도(대조용)

## 6. 화면 기능 (YAGNI — 이것만)
1. 지도 전체(이탈리아 중북부), 숙소 5개 마커(체크인·아웃 날짜 툴팁), 주차장 마커.
2. 좌측 패널: 날짜별 구간 목록 + 거리/예상시간(OSRM 응답값) + ZTL 교차 여부 배지.
3. ▶ 재생 버튼: 선택한 날짜 구간을 폴리라인 따라 마커가 이동(속도 슬라이더).
4. ZTL 레이어 토글. 교차 구간은 빨간색.
5. 웨이포인트 드래그 시 재라우팅 → ZTL 판정 갱신 (경유지 실험용).
- 안 함: 실시간 교통, 요금 계산, 로그인, 저장 서버. 좌표 수정은 파일 상단 `CONFIG` JS 객체 편집으로.

## 7. Fable에 붙일 최종 요청문 (복사용)
```
아래 BRIEF.md를 읽고 single-file HTML(Leaflet+turf, OSRM 데모)로 시뮬레이터를 만들어줘.
1단계는 ZTL 근사 폴리곤으로만 진행, 공식 데이터 로딩은 하지 마.
표의 좌표를 그대로 써. 방문지(피엔차·시에나)는 잠정이니 CONFIG에서 쉽게 바꿀 수 있게.
완료 기준: 6개 구간(10/6,7,8,9,10,12) 라우팅 성공 + ZTL 교차 0건 + 재생 동작. 브라우저로 확인해 스크린샷 1장.
설명은 최소로, 코드 파일 1개만 산출.
```

## 8. 구현 결과 (2026-09-08, 1단계 완료)
- 산출물: `index.html` 1개 (Leaflet 1.9.4 + turf 6.5 + OSRM 데모, 빌드 없음). 실행: `python -m http.server 8124 -d C:\workspace\italy-roadtrip-sim` 후 http://localhost:8124
- 6구간 라우팅 성공, ZTL 교차 0건. 총 1,372 km.
- 좌표는 Nominatim 실측으로 교정(hu Firenze는 초안보다 1.5km 동쪽 Rovezzano가 맞음).
- 발견 사항: Positano ZTL은 9인승 이상 차량 전용 → 승용차는 Garage Mandara까지 진입 가능(참고 표시로 전환). Amalfi는 SS163 해안도로 통행 가능, 성내만 ZTL. Siena Stadio 주차장은 성벽 안이지만 ZTL 밖.
- 10/6 테르미니→캠핑장은 OSRM 기본 경로가 Corso Vittorio를 지나 Centro Storico를 통과 → Porta Portese 경유점 추가로 남쪽 우회.
- (2단계에서 공식 폴리곤 로딩 완료 → §9)

## 9. 2단계 (2026-09-08) — 공식 ZTL 데이터 + 재생 버그 수정
- **버그 수정**: 재생 시 `turf.getCoords(pt).reverse()`가 turf.along()이 반환한 경로 원본 좌표 배열을 in-place로 뒤집어, 정점과 정확히 겹치는 순간 경로 좌표가 [lat,lng]로 바뀌어 경로가 에리트레아(위도 14.5·경도 40.6) 방향으로 튀고 차가 경로를 벗어났음. `toLatLng()`로 복사본 사용.
- **데이터 파이프라인**: `data/`(원천) → `python build_ztl.py` → `ztl_data.js`(window.ZTL_OFFICIAL, 22개 폴리곤, 239KB). index.html은 이 파일이 있으면 해당 도시의 수작업 근사를 무시.
  - 로마 공식(Roma Servizi per la Mobilità ArcGIS Open Data, CC-BY 3.0 IT): `services2.arcgis.com/NZMqCJwY3kMjFOqf/arcgis/rest/services/{confini_ZTL_centro_diurna,settori_ZTL_centro}/FeatureServer/0/query?f=geojson`. Tridente·Trastevere·notturna·Testaccio·San Lorenzo·Fascia Verde 서비스는 게이트(점)만 제공 → OSM 릴레이션 2459883/2572441/2691714/2573034/2573007/2573006/2461289로 보완.
  - 피렌체 공식(CC-BY 4.0): `https://datigis.comune.fi.it/json/ztl_diurna.json` (Settore A·B·O). Scudo Verde(LEZ)는 OSM 19205738.
  - 밀라노: dati.comune.milano.it가 해외 IP 403("Accesso non consentito") → OSM 릴레이션 18957600(Area C)·9633879(Area B) 사용. Overpass `out geom` → outer way 끝점 연결로 링 조립.
  - Siena·Pienza·Amalfi·Positano: OSM에 enforcement(카메라) 릴레이션만 있고 폴리곤 없음 → 수작업 근사 유지(4개).
- **판정 규칙 변경**: 경계를 25m 안쪽으로 줄인 폴리곤(turf.buffer -0.025km)으로 교차 판정. 이유: 공식/OSM 경계가 Lungotevere·viali 등 경계 도로 위에 그려져 있어 그 도로 주행이 진입으로 오탐됨(10/6 Lungotevere Aventino가 Trastevere 폴리곤에 걸림). 적용 후 6구간 위반 0·야간경고 0.
- kind 4종: ztl(위반) / night(금·토 야간만, 경고) / sector(로마 섹터 구분선, 표시만) / info(LEZ·버스ZTL, 표시만).
- (시간대별 활성 판정은 §10에서 완료)

## 10. 3단계 (2026-09-08) — 시간대별 ZTL 활성 판정
- 구간마다 `iso`(날짜)·`depart`(출발시각, 카드의 time 입력으로 변경 가능). ZTL 진입 시각 = 출발 + (진입지점 km / 총 km) × OSRM 소요시간.
- 진입지점: 경로 정점 중 첫 내부점까지의 길이, 없으면 lineIntersect 교차점 중 최소 lineSlice 길이. 판정 폴리곤은 25m 내측 버퍼(z.test).
- 스케줄 표현 `sched`: `'always'` | `[{d:[요일 0=일…6=토], f:'HH:MM', t:'HH:MM'}]`(t<f면 자정 넘김, 전날 규칙도 검사) | null(판정 안 함). 공식 데이터는 build_ztl.py 상단 S_* 상수, 수작업은 CONFIG.ztl.
  - Roma Centro 월~금 06:30~18:00·토 14:00~18:00 / Tridente 월~토 06:30~19:00 / Trastevere 월~토 06:30~10:00 / 야간 3종 금·토 21:30(23:00)~03:00
  - Firenze 월~금 07:30~20:00·토 07:30~16:00 / Milano Area C 월·화·수·금 07:30~19:30, 목 ~18:00 / Siena·Pienza·Amalfi 상시
- 결과 3단계: 위반(활성, 빨강) / 비활성 시간 통과(주황, 배지 "비활성 시간 통과") / 규칙없음(회색). 상태바는 위반·비활성 통과 건수 분리. 재생 중 현재 시각 표시, 활성 구역 내부면 빨간 발광·비활성이면 주황.
- 검증: isActive 단위 케이스 10개 통과(자정 넘김 포함), 피렌체 가상 경로로 토 09시 활성/토 17시 비활성/일 09시 비활성 확인. 실제 6구간은 기본 출발시각에서 위반 0·비활성 통과 0.
- 주의: 소요시간은 OSRM 추정(정체·휴식 미반영)이므로 경계 시각(예: 로마 토 14:00) 근처면 여유를 둘 것. 공휴일 규칙(PH off)은 미반영 — 여행기간 내 이탈리아 공휴일 없음.

## 11. 여행 계획 동기화 (2026-09-23)
- `PLAN.md` 신설: 10/4~10/13 일자별 동선·식당·카페·예약 체크리스트. 시뮬레이터 6구간과 웨이포인트/출발시각 동기화.
- 추가 웨이포인트: Napoli Parcheggio Brin(40.84618,14.28030) / Pompei Porta Marina(40.74848,14.48193) / Orvieto Campo della Fiera(42.71679,12.10523) / Montepulciano P1(43.09682,11.78522) / Bologna Piazza VIII Agosto(44.50038,11.34536). 모두 Nominatim 실측.
- 근사 ZTL 추가: Napoli Centro Antico, Bologna Centro(매일 07~20). 볼로냐 초기 폴리곤이 viali·주차장을 덮어 위반 오탐 → 북쪽 Via Irnerio 선까지로 축소하고 주차장 접근 노치 반영. 그래도 OSRM이 Via San Felice로 시내 관통 → Porta Galliera(44.5046,11.3436) 경유점을 진입·이탈 양쪽에 넣어 viali 우회 강제. 폴리곤 북변을 Viale Masini 남쪽(44.5022)·Via Milazzo 진입로 서쪽(lon<11.35 제외)으로 재조정 → 최종 6구간 위반 0 (총 1,425 km).
- 출발시각: 10/6 15:00(바티칸 투어 후 Pizzarium 여유), 10/7 08:00, 10/9 08:30, 10/10 08:45, 10/12 08:30.

## 12. 정차지 주차 최적화 (2026-09-23)
- 10/9 Furore→Orvieto 사이 Autogrill Casilina Ovest(A1 북행, 41.49638,13.68388; OSM way 188389658) 경유점 추가. 출발 후 약 1h45~2h.
- Orvieto: Campo della Fiera 유지(€1.5/h, ZTL 밖, 무료 엘리베이터·에스컬레이터). 무료 대안 Piazza della Pace+푸니쿨라(€1.3/인)는 3인 기준 더 비쌈.
- Bologna: Piazza VIII Agosto(€3.3/h) → **Parcheggio Staveco**(Viale Panzacchi 10, 44.48596,11.34421, €2/h·최대 €12, 07~01)로 변경. 입구가 viali 위라 ZTL 진입 경로 문제가 사라져 Porta Galliera 경유점 제거. 근사 폴리곤 SW 변을 viali 안쪽(44.4905,11.332 → 44.4880,11.344)으로 조정해 순환도로 주행 오탐 제거. 6구간 위반 0, 총 1,443 km.
