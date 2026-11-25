# -*- coding: utf-8 -*-
"""비용안내(/clinic/fees/) 페이지 생성 — 질문·답변(Q&A) 형식 비급여 진료비 공개 페이지.

금액 원본: 지인한의원 비급여 수가표(2026.11 엑셀) + 원내 게시 안내판(제증명 수수료).
금액·항목을 바꾸려면 이 파일의 SECTIONS 만 고치고 아래를 실행한다.

  python3 scripts/build_fees.py && python3 scripts/apply_nav.py

주의: 의료법 제56조 제2항(의료광고 금지) 때문에 '할인·이벤트·최고·효과' 같은 표현은 넣지 않는다.
금액은 의료법 제45조에 따른 비급여 진료비용 고지 내용이다.
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "clinic", "parking", "index.html")
OUT = os.path.join(ROOT, "clinic", "fees", "index.html")
BASE = "2026년 11월"

# (id, 질문, 답변 도입, [(표 제목, 설명, [(항목, 내용, 금액), ...]), ...], 답변 끝 메모)
SECTIONS = [
    ("herbal", "맞춤 한약(탕약)은 얼마인가요?",
     "체질과 증상에 맞춰 달이는 한약입니다. 하루 2포 기준 가격을 올려 두었습니다. 녹용 등 재료의 등급에 따라 금액이 달라집니다.",
     [("한약 기본 금액", "하루 2포, 20일분 · 30일분 기준",
       [("일반 한약", "3일분", "3만원"), ("", "10일분", "25만원"), ("", "20일분", "35만원"), ("", "30일분", "45만원"),
        ("녹용 상급 한약", "20일분", "55만원"), ("", "30일분", "75만원"),
        ("녹용 최상급 한약", "20일분", "65만원"), ("", "30일분", "85만원"),
        ("프리미엄 한약(러시아 원용)", "20일분", "75만원"), ("", "30일분", "95만원"),
        ("태반보약", "20일분", "50만원"), ("", "30일분", "65만원"),
        ("녹각 추가", "한약에 추가할 때", "5만원 추가")]),
      ("황후탕(보궁탕)", "축어탕 단독 또는 일반·녹용 한약과 함께 드실 때의 금액",
       [("축어탕", "단독 10일분", "25만원"),
        ("축어탕 + 일반 한약", "20일분", "53만원"), ("", "30일분", "63만원"),
        ("축어탕 + 상급 한약", "20일분", "73만원"), ("", "30일분", "90만원"),
        ("축어탕 + 최상급 한약", "20일분", "83만원"), ("", "30일분", "100만원")]),
      ],
     ""),
    ("kids", "소아(어린이) 한약은 얼마인가요?",
     "나이에 따라 첩수와 포 수가 달라집니다. 같은 나이대 안에서 재료 등급별 금액을 올려 두었습니다.",
     [("소아 한약", "",
       [("5첩 (돌~3세 · 20포 · 10~15일분)", "일반", "17만원"), ("", "상급", "23만원"),
        ("", "최상급", "25만원"), ("", "프리미엄(원용)", "27만원"),
        ("10첩 (3~6세 · 30포 · 15~20일분)", "일반", "25만원"), ("", "상급", "35만원"),
        ("", "최상급", "40만원"), ("", "프리미엄(원용)", "45만원"),
        ("15첩 (7~13세 · 40포 · 15~20일분)", "일반", "29만원"), ("", "상급", "45만원"),
        ("", "최상급", "55만원"), ("", "프리미엄(원용)", "65만원")])],
     ""),
    ("pill", "환약(알약 형태)과 가루·스틱 제품은 얼마인가요?",
     "탕약 대신 드시기 편한 환약, 그리고 환약 형태의 보약류 가격입니다.",
     [("환약", "삼오환·통치환·신통환·상통환·하통환·소청룡환은 4C, 나머지는 6C 기준",
       [("4C 환약", "1일 (2포)", "4천원"), ("", "30일분", "9만원"),
        ("6C 환약", "1일 (2포)", "6천원"), ("", "30일분", "18만원")]),
      ("경옥고", "",
       [("경옥고", "220g", "7만원"), ("", "700g", "20만원"), ("", "1.2kg", "30만원"),
        ("", "환약 (30일분)", "18만원"), ("", "스틱 30포", "11만원"),
        ("", "낱개 2포", "1만원"),
        ("녹용경옥고", "스틱 30포", "22만원"), ("", "낱개 1포", "1만원")]),
      ("총명탕·총명음", "",
       [("총명탕", "20포", "25만원"), ("", "45포", "35만원"),
        ("총명음 (스틱)", "30개", "15만원"), ("", "60개", "28만원"), ("", "90개", "40만원")]),
      ("그 밖의 환약·보약류", "",
       [("연령고본단", "30개", "11만원"), ("", "60개", "20만원"),
        ("향성파적환 · 파적고", "2개", "1만원"), ("", "10개", "5만원"),
        ("고본건양단", "1개", "1만 5천원"), ("보양우귀환", "1개", "3만원"),
        ("소합향원", "1개", "2만원"),
        ("우황청심환 (현탁액)", "1개", "1만 8천원"),
        ("신선불취단(환)", "10개", "6만원"), ("", "30개", "16만원")])],
     ""),
    ("gongjin", "공진단은 종류별로 얼마인가요?",
     "공진단은 들어가는 약재(녹용·사향 등)에 따라 종류가 나뉩니다. 사향 함량이 다른 공진단 두 종류를 포함해 모두 올려 두었습니다.",
     [("공진단 종류별 금액", "",
       [("녹용 · 총명 · 침향 공진단", "1알", "2만원"), ("", "10알", "20만원"), ("", "30알", "50만원"),
        ("사향(6M) 공진단 · 지인공진단", "1알", "6만원"), ("", "10알", "60만원"),
        ("사향(10M) 공진단 · 황제공진단", "1알", "10만원"), ("", "10알", "100만원"),
        ("구인(활력) 공진단", "1알", "8만원"), ("", "10알", "80만원")])],
     ""),
    ("treat", "침·봉침·약침·추나 같은 치료는 얼마인가요?",
     "건강보험이 적용되지 않는 비급여 치료 금액입니다. 같은 치료를 여러 번 받으시는 경우 10회 기준 금액도 함께 올려 두었습니다. 건강보험이 적용되는 진료(침·뜸·부항 등)는 건강보험 기준에 따라 본인부담금만 내시며, 이 표에는 포함되지 않습니다.",
     [("봉침 · 약침", "",
       [("봉침 (활력봉침)", "1회", "3만원"), ("", "10회", "25만원"),
        ("탈모·태반·DNA·홍삼·수승화강 약침", "1회", "3만원"), ("", "10회", "27만원"),
        ("약침 (A1, A2, nm)", "기본 1회", "6천원"), ("", "추가 1회", "1만원"),
        ("산삼비만약침", "1회 (1부위 · 4대)", "3만원"), ("", "10회 (총 40대)", "27만원"),
        ("", "1회 (2부위 · 8대)", "6만원"), ("", "10회 (총 80대)", "50만원")]),
      ("매선 · 정안침 · 다이어트침", "",
       [("통증매선 (약실)", "1회 (4개)", "3만원"), ("", "10회", "27만원"),
        ("치료 정안침", "1회", "3만원"), ("", "10회", "27만원"),
        ("다이어트 침", "1회", "2만원"), ("", "10회", "18만원"),
        ("유착박리술 (특수침약침)", "1회", "1만원")]),
      ("추나 (비급여)", "",
       [("복잡추나", "1회", "4만원"), ("", "10회", "36만원"),
        ("단순추나", "1회", "2만원"), ("", "10회", "15만원")]),
      ("감기약 · 기침약", "",
       [("진해고", "3포", "1만 2천원"), ("", "1박스 (10포)", "4만원"),
        ("해감 (종합감기약)", "1박스 (15포)", "5만원"), ("", "2박스", "9만원")])],
     ""),
    ("skin", "피부·미용 관련 관리는 얼마인가요?",
     "얼굴·몸 관리와 다이어트 보조 제품 금액입니다. 매선은 개수에 따라 금액이 달라집니다.",
     [("얼굴 관리", "",
       [("미세약초침 (얼굴, AMTS)", "1회", "11만원"), ("", "3회", "30만원"),
        ("홍삼 부스터", "1회", "15만원"), ("", "3회", "40만원"),
        ("전체 매선 (얼굴)", "1회 (10개)", "11만원"), ("", "1회 (20개)", "15만원"),
        ("", "1회 (40개)", "25만원"), ("", "1회 (50개)", "30만원"),
        ("미용 정안침", "1회", "10만원"), ("", "10회", "70만원"),
        ("윤곽약침 1cc", "1회", "3만원"), ("", "10회", "27만원")]),
      ("몸 관리 · 붓기", "",
       [("다이어트 탄력매선 (바디)", "1회 (10개)", "15만원"), ("", "1회 (20개)", "20만원"),
        ("", "1회 (40개)", "30만원"), ("", "1회 (60개)", "40만원"),
        ("붓기탕", "2주", "14만원"), ("붓기침", "5회", "15만원")]),
      ("다이어트 보조 제품", "",
       [("다이어트 탕약", "30일분", "45만원"), ("다이어트 환약", "30일분", "30만원"),
        ("비대면 다이어트", "1개월 (90포)", "15만원"),
        ("마시는 공진단", "5앰플", "20만원"),
        ("선식", "1박스 (30포)", "9만원"), ("절식", "3일", "7만원"),
        ("클린환", "1P", "2천원"), ("", "30포", "5만원"),
        ("감비차", "10개", "2만 5천원"), ("", "50개", "8만 5천원")])],
     ""),
    ("docs", "진단서·소견서 같은 서류 발급 비용은 얼마인가요?",
     "진료기록부 사본, 진단서 등 제증명 수수료입니다. 의료법 시행규칙 제42조의2 제3항에 따라 접수창구에도 같은 내용을 게시하고 있습니다.",
     [("제증명 수수료", "",
       [("일반진단서", "1회", "1만원"), ("소견서 (진단명 표기)", "1회", "1만원"),
        ("진료확인서 (보험사 제출용)", "1회", "3천원"), ("진료기록부 사본", "1장당", "1천원")])],
     ""),
]

# 일반 질문(표 없는 답변)
GENERAL = [
    ("건강보험이 적용되는 진료와 어떻게 다른가요?",
     "침·뜸·부항 등 건강보험이 적용되는 진료는 건강보험 기준에 따라 본인부담금만 내시고, 이 페이지의 금액에는 포함되지 않습니다. 한약, 약침, 봉침, 매선, 비급여 추나 같은 항목은 건강보험이 적용되지 않는 비급여라서 이 페이지에 올린 금액을 기준으로 안내드립니다."),
    ("금액이 바뀌면 어떻게 확인하나요?",
     "이 페이지의 금액은 %s 기준입니다. 재료비 등으로 금액이 바뀌면 이 페이지와 원내 게시를 함께 고칩니다. 내원 전에 정확한 금액이 궁금하시면 전화(0507-1387-2933)나 카카오톡으로 문의해 주세요." % BASE),
    ("표에 없는 항목은 어떻게 하나요?",
     "표에 없는 항목도 처방이나 치료를 시작하기 전에 해당 비용을 먼저 안내해 드립니다."),
]

# 환자 입장에서 먼저 보이는 질문과 답변 (질문, [문단...])
USER_QA = [
    ("진료 비용을 미리 확인할 수 있나요?",
     ["네. 지인한의원은 환자분들이 진료를 받기 전 비용을 충분히 확인하실 수 있도록 비급여 진료 항목과 가격을 홈페이지에 공개하고 있습니다.",
      "한약, 녹용 보약, 공진단, 약침, 추나, 미용 및 피부 관리 등 다양한 항목의 비용을 확인하실 수 있습니다."]),
    ("한약 가격은 어떻게 결정되나요?",
     ["한약은 처방 구성, 복용 기간, 사용하는 약재의 종류와 등급 등에 따라 비용이 달라집니다.",
      "일반 한약부터 녹용을 포함한 한약, 프리미엄 원용 녹용 한약까지 구분하여 안내하고 있으며, 환자분의 건강 상태와 필요에 맞춰 상담 후 처방합니다."]),
    ("녹용 한약은 등급에 따라 가격이 다른가요?",
     ["네. 녹용의 종류와 등급에 따라 비용에 차이가 있습니다.",
      "녹용 상급, 녹용 최상급, 프리미엄 원용 녹용 한약으로 구분하여 가격을 안내하고 있으며, 녹용이 들어가지 않는 일반 한약의 가격도 함께 확인하실 수 있습니다."]),
    ("약침이나 추나 치료 비용도 미리 알 수 있나요?",
     ["네. 약침은 종류와 용량, 치료 부위 등에 따라 비용이 달라질 수 있으며, 추나 치료도 치료 유형에 따라 비용이 구분됩니다.",
      "각 항목의 기본 비용과 치료 횟수에 따른 비용을 사전에 확인하실 수 있습니다."]),
    ("안내된 가격 외에 추가 비용이 발생할 수도 있나요?",
     ["치료 내용이나 처방 구성, 추가 시술 여부에 따라 해당 항목의 비용이 더해질 수 있습니다. 이때도 항목별 금액은 이 페이지에 안내된 그대로입니다.",
      "지인한의원은 환자분이 예상하지 못한 비용으로 불편을 겪지 않도록 추가 비용이 발생하는 경우 사전에 안내하고 동의를 구하는 것을 원칙으로 합니다."]),
    ("어떤 치료를 받을지는 누가 정하나요?",
     ["진찰한 한의사가 환자분의 상태를 보고 필요하다고 판단한 치료를 권해 드립니다. 비용이 더 드는 치료라도 필요하다고 판단되면 그 이유와 비용을 먼저 설명해 드리고, 환자분이 이해하고 동의하신 뒤에 진행합니다.",
      "가격은 치료를 권하는 기준이 아닙니다. 이 페이지의 가격표는 정해진 금액을 숨김없이 알려 드리기 위한 것이고, 실제 치료 가능 여부와 적합한 방법은 상담 후 결정됩니다.",
      "궁금한 비용이나 치료 항목이 있으시면 언제든 편하게 문의해 주세요."]),
]


def esc(s):
    return html.escape(s, quote=True)


def table_html(title, note, rows):
    out = ['<div class="ft-wrap"><table class="ft"><caption>%s%s</caption>'
           '<thead><tr><th scope="col">항목</th><th scope="col">구성</th><th scope="col">비용</th></tr></thead><tbody>'
           % (esc(title), (" <small>%s</small>" % esc(note)) if note else "")]
    i = 0
    while i < len(rows):
        name = rows[i][0]
        span = 1
        while i + span < len(rows) and rows[i + span][0] == "":
            span += 1
        for k in range(span):
            _, spec, price = rows[i + k]
            cells = ""
            if k == 0:
                cells += '<th scope="%s"%s>%s</th>' % ("rowgroup" if span > 1 else "row", ' rowspan="%d"' % span if span > 1 else "", esc(name))
            cells += "<td>%s</td><td class=\"pr%s\">%s</td>" % (esc(spec), " long" if len(price) > 7 else "", esc(price))
            out.append("<tr%s>%s</tr>" % (' class="gs"' if k == 0 and i > 0 else "", cells))
        i += span
    out.append("</tbody></table></div>")
    return "".join(out)


def qa_block(qid, q, intro, tables, memo, open_=False):
    body = "<p>%s</p>" % esc(intro)
    body += "".join(table_html(*t) for t in tables)
    if memo:
        body += '<p class="memo">%s</p>' % esc(memo)
    return ('<details class="qa" id="%s"%s><summary><span class="q">Q</span>%s</summary>'
            '<div class="a"><span class="aa">A</span><div>%s</div></div></details>'
            % (qid, " open" if open_ else "", esc(q), body))


def panel_block(qid, q, intro, tables, memo):
    body = "<p>%s</p>" % esc(intro)
    body += "".join(table_html(*x) for x in tables)
    if memo:
        body += '<p class="memo">%s</p>' % esc(memo)
    return ('<section class="tp" id="%s" role="tabpanel" aria-labelledby="t-%s"><h3 class="tq"><span class="q">Q</span>%s</h3>'
            '<div class="a"><span class="aa">A</span><div>%s</div></div></section>' % (qid, qid, esc(q), body))


TAB_JS = """<script>(function(){var w=document.querySelector('.tabwrap');if(!w)return;
var tabs=[].slice.call(w.querySelectorAll('[role=tab]')),ps=[].slice.call(w.querySelectorAll('.tp'));w.classList.add('tabs-on');
function show(id){tabs.forEach(function(t){var o=t.getAttribute('data-t')===id;t.classList.toggle('on',o);t.setAttribute('aria-selected',o)});ps.forEach(function(p){p.classList.toggle('on',p.id===id)})}
tabs.forEach(function(t){t.addEventListener('click',function(){var id=t.getAttribute('data-t');show(id);try{history.replaceState(null,'','#'+id)}catch(e){}})});
var h=location.hash.slice(1),ok=ps.some(function(p){return p.id===h});show(ok?h:ps[0].id);if(ok)setTimeout(function(){w.scrollIntoView()},50);
})();</script>"""


def user_block(i, q, paras, open_=False):
    return ('<details class="qa" id="u%d"%s><summary><span class="q">Q</span>%s</summary>'
            '<div class="a"><span class="aa">A</span><div>%s</div></div></details>'
            % (i, " open" if open_ else "", esc(q), "".join("<p>%s</p>" % esc(x) for x in paras)))


def general_block(i, q, a):
    return ('<details class="qa" id="g%d"><summary><span class="q">Q</span>%s</summary>'
            '<div class="a"><span class="aa">A</span><div><p>%s</p></div></div></details>' % (i, esc(q), esc(a)))


CSS = """
  .lead{font-size:16px;color:var(--ink-soft);margin:0 0 22px}
  .pledge{display:grid;gap:10px;margin:0 0 26px}
  @media (min-width:640px){.pledge{grid-template-columns:repeat(3,1fr)}}
  .pledge div{background:#FFFDF4;border:1px solid var(--line);border-radius:14px;padding:16px 18px;font-size:14px;line-height:1.7}
  .pledge b{display:block;font-family:'Noto Serif KR',serif;color:var(--pine-deep);font-size:15px;margin-bottom:2px}
  .asof{display:inline-block;background:var(--ochre-soft);color:#6B4311;font-size:12.5px;font-weight:700;padding:4px 12px;border-radius:999px;margin:0 0 18px}
  .tabs{display:flex;gap:7px;overflow-x:auto;padding:2px 2px 10px;margin:0 0 6px;scrollbar-width:thin}
  .tabs button{flex:none;font:700 14px/1 'Noto Sans KR',sans-serif;color:var(--pine);background:#FFFDF4;border:1.5px solid var(--line);padding:11px 16px;border-radius:999px;cursor:pointer;white-space:nowrap}
  .tabs button.on{background:var(--pine);color:#F3F0E4;border-color:var(--pine)}
  .tabs-on .tp:not(.on){display:none}
  .tp{background:#FFFDF4;border:1px solid var(--line);border-radius:14px;padding:16px 18px 6px}
  .tq{display:flex;gap:12px;align-items:flex-start;margin:0 0 12px;font-size:15.5px;line-height:1.55;color:var(--pine-deep);font-family:'Noto Sans KR',sans-serif;font-weight:700}
  .tp .a{padding:0}
  @media (max-width:600px){.tp{padding:14px 12px 4px}}
  .jump{display:flex;flex-wrap:wrap;gap:7px;margin:0 0 24px}
  .jump a{font-size:13px;font-weight:700;text-decoration:none;color:var(--pine);border:1.5px solid var(--line);background:#FFFDF4;padding:7px 12px;border-radius:999px}
  .qa{background:#FFFDF4;border:1px solid var(--line);border-radius:14px;margin:0 0 10px;scroll-margin-top:90px}
  .qa>summary{list-style:none;cursor:pointer;display:flex;gap:12px;align-items:flex-start;padding:16px 18px;font-weight:700;font-size:15.5px;line-height:1.55;color:var(--pine-deep)}
  .qa>summary::-webkit-details-marker{display:none}
  .qa>summary::after{content:"";margin-left:auto;flex:none;width:9px;height:9px;margin-top:7px;border-right:2px solid var(--ink-soft);border-bottom:2px solid var(--ink-soft);transform:rotate(45deg);transition:transform .15s}
  .qa[open]>summary::after{transform:rotate(-135deg);margin-top:11px}
  .q,.aa{flex:none;width:26px;height:26px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font:900 13px/1 'Noto Serif KR',serif}
  .q{background:var(--pine);color:#F3F0E4}
  .aa{background:var(--ochre);color:#fff}
  .a{display:flex;gap:12px;padding:0 18px 18px;align-items:flex-start}
  .a>div{flex:1;min-width:0}
  .a p{margin:2px 0 14px;font-size:14.5px;color:var(--ink-soft);line-height:1.8}
  .a .memo{font-size:13px}
  .ft-wrap{overflow-x:auto;margin:0 0 16px;border:1px solid var(--line);border-radius:12px}
  table.ft{border-collapse:collapse;width:100%;font-size:13.5px;line-height:1.55;min-width:340px}
  .ft caption{text-align:left;font-weight:900;font-family:'Noto Serif KR',serif;color:var(--pine-deep);font-size:14.5px;padding:11px 12px 8px;background:var(--paper-deep)}
  .ft caption small{display:block;font:500 12px/1.5 'Noto Sans KR',sans-serif;color:var(--ink-soft);margin-top:2px}
  .ft th,.ft td{padding:9px 12px;border-top:1px solid var(--line);text-align:left;vertical-align:top}
  .ft thead th{background:var(--pine);color:#F3F0E4;font-size:12.5px;border-top:0}
  .ft thead th:last-child{text-align:right}
  .ft tbody th{font-weight:700;color:var(--pine-deep);background:#FAF7EA;width:38%}
  .ft td.pr{text-align:right;font-weight:800;color:#8A5412;white-space:nowrap}
  .ft td.pr.long{white-space:normal;min-width:6em}
  @media (max-width:600px){.a{flex-direction:column;gap:6px}.qa>summary{padding:14px}.a{padding:0 12px 14px}table.ft{min-width:0;font-size:13px}.ft th,.ft td{padding:8px 8px}.ft tbody th{width:36%}.ft thead th{font-size:12px}}
  .ft tr.gs>*{border-top:2px solid var(--line)}
  .h2b{font-size:19px;margin:6px 0 14px}
  .closing{background:var(--pine);color:#F3F0E4;border-radius:16px;padding:22px 24px;margin:30px 0 14px}
  .closing b{font-family:'Noto Serif KR',serif;font-size:17px;display:block;margin-bottom:6px}
  .closing p{margin:0;font-size:14.5px;opacity:.92;line-height:1.8}
  .src{font-size:12.5px;color:var(--ink-soft);margin:6px 0 24px;line-height:1.7}
"""


def build():
    src = open(TEMPLATE, encoding="utf-8").read()
    head_end = src.index("</head>")
    head = src[:head_end]
    head = re.sub(r"<title>.*?</title>", "<title>비용안내 — 한약·약침·봉침 비급여 진료비 공개 | 부천 지인한의원</title>", head, count=1, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">',
                  '<meta name="description" content="부천 지인한의원 비급여 진료비를 질문과 답 형식으로 모두 공개합니다. 한약, 소아 한약, 공진단, 약침, 봉침, 추나, 제증명 수수료까지 항목별 금액을 확인하세요. %s 기준.">' % BASE,
                  head, count=1)
    head = head.replace("https://jeeinclinic.com/clinic/parking/", "https://jeeinclinic.com/clinic/fees/")
    head = re.sub(r"\n  /\* FEES:START \*/.*?/\* FEES:END \*/", "", head, flags=re.S)
    head = head.replace("</style>", "  /* FEES:START */" + CSS + "  /* FEES:END */\n</style>", 1) if "</style>" in head else head

    faq = []
    qa_html = []
    for i, (qid, q, intro, tables, memo) in enumerate(SECTIONS):
        qa_html.append(panel_block(qid, q, intro, tables, memo))
        faq.append((q, intro))
    user_html = []
    for i, (q, paras) in enumerate(USER_QA):
        user_html.append(user_block(i, q, paras, open_=(i == 0)))
        faq.append((q, " ".join(paras)))
    gen_html = []
    for i, (q, a) in enumerate(GENERAL):
        gen_html.append(general_block(i, q, a))
        faq.append((q, a))
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    jump = "".join('<button type="button" role="tab" id="t-%s" data-t="%s" aria-selected="false">%s</button>' % (s[0], s[0], esc(label)) for s, label in zip(
        SECTIONS, ["한약", "소아 한약", "환약·보약", "공진단", "치료", "피부·미용", "서류 발급"]))

    article = """<article>
  <div class="eyebrow">지인한의원 소개 · 비용안내</div>
  <h1>진료비, <em style="font-style:normal;color:var(--seal)">숨기지 않고</em><br>항목별로 모두 공개합니다</h1>
  <p class="lead">"이 치료 얼마예요?" 하고 궁금하실 때 바로 확인하실 수 있도록, 건강보험이 적용되지 않는 비급여 진료의 수가표를 전 항목 숨김없이 공개합니다.</p>
  <h2 class="h2b" style="margin-top:26px">지인한의원의 비용 안내 원칙</h2>
  <div class="pledge">
    <div><b>정확한 진찰 후 안내</b>환자분의 상태를 진찰한 뒤, 필요한 치료와 그 비용을 치료계획서로 안내해 드립니다.</div>
    <div><b>필요한 치료만 권합니다</b>필요하지 않은 치료는 권하지 않고, 필요한 치료는 이유와 비용을 먼저 설명해 드립니다. 상담 당일 결제를 재촉하지 않습니다.</div>
    <div><b>충분한 상담</b>비용에 대해 궁금한 점은 부담 없이 물어보세요. 충분히 설명해 드립니다.</div>
  </div>
  <span class="asof">%s 기준 금액</span>
  <h2 class="h2b">지인한의원 진료비용 Q&amp;A</h2>
  %s
  <h2 class="h2b" style="margin-top:34px">예상 비용 · 치료별 가격 안내 (비급여 수가표)</h2>
  <p class="lead" style="font-size:14.5px;margin-bottom:14px">한약부터 약침·추나·피부 관리까지 얼마인지 전 항목 공개합니다. 실제로 어떤 항목이 필요한지는 진찰 후 정해지며, 궁금한 항목의 탭을 누르면 해당 가격표만 보입니다.</p>
  <div class="tabwrap">
  <div class="tabs" role="tablist" aria-label="비용 항목">%s</div>
  %s
  </div>
  %s
  <h2 class="h2b" style="margin-top:34px">비용 안내에 대해 자주 묻는 질문</h2>
  %s
  <div class="closing">
    <b>투명한 비용 안내로 신뢰를 소중히 생각합니다.</b>
    <p>치료를 시작하기 전 충분히 설명하고, 환자분이 이해하고 선택하실 수 있도록 정성을 다하겠습니다.</p>
  </div>
  <p class="src">※ 의료법 제45조 및 같은 법 시행규칙 제42조의2에 따른 비급여 진료비용 고지입니다.</p>
  <div class="ctas">
    <a class="c-call" href="tel:0507-1387-2933">📞 0507-1387-2933</a>
    <a class="c-kakao" href="https://pf.kakao.com/_xmxhmpxj/chat" target="_blank" rel="noopener">💬 카카오톡 문의</a>
    <a class="c-naver" href="https://booking.naver.com/booking/13/bizes/185044" target="_blank" rel="noopener">네이버 예약</a>
  </div>
  <h2>지인한의원 소개의 다른 안내</h2>
  <div class="sib"><a href="/mission/">미션</a><a href="/about/">의료진소개</a><a href="/#info">진료시간</a><a href="/clinic/parking/">주차장안내</a><a href="/#info">오시는길</a><a href="/clinic/fees/" aria-current="page">비용안내</a></div>
</article>""" % (BASE, "\n  ".join(user_html), jump, "\n  ".join(qa_html), TAB_JS, "\n  ".join(gen_html))

    # 본문 교체: <article> ... </article>
    a0 = src.index("<article>")
    a1 = src.index("</article>") + len("</article>")
    page = head + "</head>" + src[head_end + len("</head>"):a0] + article + src[a1:]
    page = page.replace("</head>", '<script type="application/ld+json">%s</script>\n</head>' % json.dumps(ld, ensure_ascii=False), 1)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(page)
    print("fees page written:", OUT, len(page))


if __name__ == "__main__":
    build()
