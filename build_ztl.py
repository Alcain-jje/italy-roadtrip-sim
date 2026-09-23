# -*- coding: utf-8 -*-
"""
data/ 의 원천(로마 ArcGIS 공식, 피렌체 공식 GeoJSON, OSM Overpass 릴레이션)을
하나의 ztl_data.js (window.ZTL_OFFICIAL = [...]) 로 합친다.

실행:  python build_ztl.py
원천 재수집은 BRIEF.md §5 / §9 참고. 라이선스: 로마 RSM CC-BY 3.0 IT, 피렌체 CC-BY 4.0, OSM ODbL.
"""
import json, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
PREC = 5  # 소수 5자리 ≈ 1 m

# 활성 시간 규칙. d = 요일(JS getDay: 0=일 … 6=토), f/t = 'HH:MM' (t < f 이면 자정 넘김). 'always' = 상시. None = 판정 안 함(표시용)
WD = [1, 2, 3, 4, 5]
S_ROMA_CENTRO   = [dict(d=WD, f='06:30', t='18:00'), dict(d=[6], f='14:00', t='18:00')]
S_ROMA_TRIDENTE = [dict(d=WD + [6], f='06:30', t='19:00')]
S_ROMA_TRAST_D  = [dict(d=WD + [6], f='06:30', t='10:00')]
S_ROMA_TRAST_N  = [dict(d=[5, 6], f='21:30', t='03:00')]
S_ROMA_CENTRO_N = [dict(d=[5, 6], f='23:00', t='03:00')]
S_FIRENZE       = [dict(d=WD, f='07:30', t='20:00'), dict(d=[6], f='07:30', t='16:00')]
S_MILANO_C      = [dict(d=[1, 2, 3, 5], f='07:30', t='19:30'), dict(d=[4], f='07:30', t='18:00')]
S_MILANO_B      = [dict(d=WD, f='07:30', t='19:30')]


def rnd(coords):
    if isinstance(coords[0], (int, float)):
        return [round(coords[0], PREC), round(coords[1], PREC)]
    return [rnd(c) for c in coords]


def load(name):
    with io.open(os.path.join(DATA, name), encoding='utf-8') as f:
        return json.load(f)


# ---------------------------------------------------------------- OSM 릴레이션 → 폴리곤
def stitch_rings(ways):
    """outer way 조각들을 끝점 연결로 닫힌 링들로 조립한다."""
    segs = [[(p['lon'], p['lat']) for p in w['geometry']] for w in ways if w.get('geometry')]
    rings = []
    while segs:
        ring = segs.pop(0)
        changed = True
        while changed and ring[0] != ring[-1]:
            changed = False
            for i, s in enumerate(segs):
                if s[0] == ring[-1]:
                    ring += s[1:]; segs.pop(i); changed = True; break
                if s[-1] == ring[-1]:
                    ring += list(reversed(s))[1:]; segs.pop(i); changed = True; break
                if s[-1] == ring[0]:
                    ring = s[:-1] + ring; segs.pop(i); changed = True; break
                if s[0] == ring[0]:
                    ring = list(reversed(s))[:-1] + ring; segs.pop(i); changed = True; break
        if ring[0] != ring[-1]:
            ring.append(ring[0])  # 미세 불일치 시 강제 닫기
        rings.append([list(c) for c in ring])
    return rings


def osm_relation_polygon(rel):
    outers = [m for m in rel.get('members', []) if m['type'] == 'way' and m.get('role') in ('outer', '')]
    rings = stitch_rings(outers)
    rings = [r for r in rings if len(r) >= 4]
    if not rings:
        return None
    if len(rings) == 1:
        return {'type': 'Polygon', 'coordinates': [rnd(rings[0])]}
    return {'type': 'MultiPolygon', 'coordinates': [[rnd(r)] for r in rings]}


def osm_entries(fname, spec):
    """spec: {relation_id: dict(name, city, kind, hours)}"""
    out = []
    if not os.path.exists(os.path.join(DATA, fname)):
        print('skip (missing)', fname); return out
    j = load(fname)
    for e in j['elements']:
        if e['type'] != 'relation' or e['id'] not in spec:
            continue
        geom = osm_relation_polygon(e)
        if not geom:
            print('  ! no ring for', e['id']); continue
        s = spec[e['id']]
        out.append(dict(name=s['name'], city=s['city'], kind=s['kind'], hours=s['hours'], sched=s.get('sched'),
                        source='OSM relation %d (ODbL)' % e['id'], geometry=geom))
        print('  osm', e['id'], s['name'], geom['type'])
    return out


# ---------------------------------------------------------------- 빌드
entries = []

# 1) 로마 공식 (Roma Servizi per la Mobilità, ArcGIS Open Data, CC-BY 3.0 IT)
j = load('roma_confini_ZTL_centro_diurna.geojson')
for f in j['features']:
    entries.append(dict(name='Roma ZTL Centro Storico (diurna)', city='Roma', kind='ztl',
                        hours='월~금 06:30~18:00, 토 14:00~18:00', sched=S_ROMA_CENTRO,
                        source='Roma Servizi per la Mobilità · confini_ZTL_centro_diurna (CC-BY 3.0 IT)',
                        geometry={'type': f['geometry']['type'], 'coordinates': rnd(f['geometry']['coordinates'])}))
    print('  roma official confini', f['geometry']['type'])
j = load('roma_settori_ZTL_centro.geojson')
for f in j['features']:
    nm = (f['properties'].get('Name') or '').strip()
    desc = (f['properties'].get('descriptio') or '').replace('<br>', ' ').strip()
    entries.append(dict(name='Roma ZTL Centro %s' % nm, city='Roma', kind='sector',
                        hours=desc or 'ZTL DIURNA', sched=None,
                        source='Roma Servizi per la Mobilità · settori_ZTL_centro (CC-BY 3.0 IT)',
                        geometry={'type': f['geometry']['type'], 'coordinates': rnd(f['geometry']['coordinates'])}))
print('  roma official sectors', len(j['features']))

# 2) 로마 보조 (OSM) — 공식 데이터가 게이트 좌표만 제공하는 구역
entries += osm_entries('overpass_roma_geom.json', {
    2459883: dict(name='Roma ZTL Tridente (A1)', city='Roma', kind='ztl', hours='월~토 06:30~19:00 (Tridente 강화구역)', sched=S_ROMA_TRIDENTE),
    2572441: dict(name='Roma ZTL Trastevere (diurna)', city='Roma', kind='ztl', hours='월~토 06:30~10:00', sched=S_ROMA_TRAST_D),
    2691714: dict(name='Roma ZTL Trastevere (notturna)', city='Roma', kind='night', hours='금·토 21:30~03:00 (야간)', sched=S_ROMA_TRAST_N),
    2573034: dict(name='Roma ZTL Centro (notturna)', city='Roma', kind='night', hours='금·토 23:00~03:00 (야간)', sched=S_ROMA_CENTRO_N),
    2573007: dict(name='Roma ZTL Testaccio (notturna)', city='Roma', kind='night', hours='금·토 23:00~03:00 (야간)', sched=S_ROMA_CENTRO_N),
    2573006: dict(name='Roma ZTL San Lorenzo (notturna)', city='Roma', kind='night', hours='금·토 21:30~03:00 (야간)', sched=S_ROMA_TRAST_N),
    2461289: dict(name='Roma Fascia Verde (LEZ, 참고)', city='Roma', kind='info', hours='저공해 기준 미달 차량만 제한 · 렌트카 통상 OK', sched=None),
})

# 3) 피렌체 공식 (Comune di Firenze Open Data, CC-BY 4.0)
j = load('firenze_ztl_diurna.json')
for f in j['features']:
    sec = f['properties'].get('tipologia')
    entries.append(dict(name='Firenze ZTL Settore %s' % sec, city='Firenze', kind='ztl',
                        hours='월~금 07:30~20:00, 토 07:30~16:00 (+4~9월 목~토 야간)', sched=S_FIRENZE,
                        source='Comune di Firenze · ztl_diurna (CC-BY 4.0)',
                        geometry={'type': f['geometry']['type'], 'coordinates': rnd(f['geometry']['coordinates'])}))
print('  firenze official', len(j['features']))

# 4) 밀라노 (공식 포털 해외 IP 차단 → OSM 경계 사용) + 피렌체 Scudo Verde(참고)
entries += osm_entries('overpass_milano_geom.json', {
    18957600: dict(name='Milano Area C', city='Milano', kind='ztl', hours='월~금 07:30~19:30 (목 ~18:00) 유료(€7.5) · 미결제 시 과태료', sched=S_MILANO_C),
    9633879: dict(name='Milano Area B (LEZ, 참고)', city='Milano', kind='info', hours='월~금 07:30~19:30 · 저공해차 통행 가능(렌트카 통상 OK)', sched=S_MILANO_B),
    19205738: dict(name='Firenze Scudo Verde (LEZ, 참고)', city='Firenze', kind='info', hours='Euro 0~1 등 노후차만 제한 · 렌트카 통상 OK', sched=None),
})

out = os.path.join(HERE, 'ztl_data.js')
with io.open(out, 'w', encoding='utf-8') as f:
    f.write('// 자동 생성: python build_ztl.py — 수정 금지. 원천/라이선스는 각 항목 source 참고.\n')
    f.write('window.ZTL_OFFICIAL = ')
    json.dump(entries, f, ensure_ascii=False, separators=(',', ':'))
    f.write(';\n')
print('wrote', out, len(entries), 'entries', os.path.getsize(out), 'bytes')
