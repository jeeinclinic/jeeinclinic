# -*- coding: utf-8 -*-
"""진단 및 검사(/special/diagnosis/) 페이지 생성.

원내 검사 장비 7종(3차원 맥영상 검사기·유비오맥파·인바디 270S·자동혈압계·자동신장체중계·
혈당측정기·혈액검사기 DRI-CHEM NX500i)을 환자 눈높이로 설명한다.
내용은 제조사 공개 자료·공개 문헌에 근거하며, 근거 링크는 페이지 하단 '참고 자료'에 둔다.

  python3 scripts/build_diagnosis.py && python3 scripts/apply_nav.py

의료법 제56조 제2항(의료광고 금지) 때문에 '최고·정확히 진단·다른 곳에 없는' 같은 표현,
치료 효과를 단정하는 표현, 다른 의료기관과의 비교는 넣지 않는다.
검사는 '진단'이 아니라 '진료 참고 자료'로만 쓴다고 명시한다.
"""
import json
import os
import re

import build_fees as bf

ROOT = bf.ROOT
TEMPLATE = bf.TEMPLATE
OUT = os.path.join(ROOT, "special", "diagnosis", "index.html")
esc = bf.esc

PLEDGE = [
    ("진찰이 먼저입니다", "검사는 한의사의 진찰을 대신하지 않습니다. 문진과 진찰로 먼저 판단하고, 필요한 검사만 보조로 사용합니다."),
    ("결과는 직접 설명드립니다", "검사가 끝나면 수치와 그래프가 무엇을 뜻하는지 한의사가 쉬운 말로 설명드립니다."),
    ("범위를 넘는 소견은 연계합니다", "결과에서 한의 진료 범위를 넘는 소견이 의심되면 정밀검사가 가능한 의료기관 진료를 안내합니다."),
]

# (장비, 보는 것, 대표적으로 쓰는 때)
OVERVIEW = [
    ("3차원 맥영상 검사기 (대요메디)", "맥의 깊이·빠르기·형태·세기, 혈관·혈압·심장 기능 정보", "맥진을 객관 자료로 남길 때, 한약 복용 전후 변화를 볼 때"),
    ("유비오맥파", "맥파와 심박변이도 기반의 스트레스·자율신경 균형 참고 지표", "피로·불면·긴장으로 몸의 조절 상태를 볼 때"),
    ("인바디 270S", "근육량·체지방량·체수분", "다이어트·부종·체력 저하 상담"),
    ("자동혈압계", "혈압과 맥박", "두통·어지럼·부종, 한약 처방 전 기본 확인"),
    ("자동신장체중계", "키와 체중 (체질량지수 계산)", "소아 성장, 체중 관리 경과 확인"),
    ("혈당측정기", "손끝 혈액의 혈당 수치", "갈증·피로·체중 변화 상담 시 선별 참고"),
    ("혈액검사기 (DRI-CHEM NX500i)", "간·신장 기능, 혈당, 지질 등 혈액 생화학 수치", "한약 복용 전 몸 상태 확인, 경과 확인"),
]

# (id, 질문, [문단...], 알아두실 점, [(근거 이름, URL)...])
DEVICES = [
    ("d1", "3차원 맥영상 검사기는 무엇을 알려주나요?",
     ["맥진(脈診)은 손목의 맥을 짚어 몸의 상태를 살피는 한의학의 대표적인 진찰법입니다. 한의사의 손끝 감각으로 보던 맥을 기기로 함께 측정해 그래프와 수치로 남기는 장비가 3차원 맥영상 검사기이며, 본원은 대요메디(주) 제품을 사용합니다.",
      "제조사 자료에 따르면 이 검사기는 맥을 보는 기본 요소인 깊이·빠르기·형태·세기를 물리적으로 정의해 단계별로 결과를 보여 주고, 혈관·혈압·심장 기능과 전체적인 혈액순환 정보를 함께 제공합니다. 같은 분의 맥이 시간이 지나며 어떻게 달라졌는지 비교해 볼 수 있다는 점도 장점입니다.",
      "제조사는 이 기술이 건강보험심사평가원의 의료기술평가를 거쳐 건강보험 행위로 등재된 한의 진단 기술이며, 맥진기 국제표준(ISO)을 개발했다고 소개합니다."],
     "맥영상은 병명을 알려 주는 검사가 아니라, 한의사가 맥을 해석할 때 참고하는 객관 자료입니다. 긴장·식사·시간대에 따라 맥은 달라질 수 있어, 충분히 안정하신 뒤에 측정하고 변화를 이어서 비교합니다.",
     [("대요메디, 3차원 맥영상 검사기 소개 기사 (스포츠경향, 2024.3.18)", "https://sports.khan.co.kr/article/202403180714003")]),
    ("d2", "유비오맥파는 어떤 검사인가요?",
     ["손가락 끝에 센서를 대고 맥박의 파형을 읽어, 심장이 뛰는 간격의 미세한 변화(심박변이도)와 혈관 쪽 신호를 함께 살피는 검사입니다. 심박변이도는 몸의 긴장(교감신경)과 이완(부교감신경)의 균형을 가늠하는 지표로 널리 연구되어 왔습니다.",
      "피곤한데 잠이 오지 않거나, 늘 긴장되어 있다고 느끼시는 분의 몸 상태를 객관적인 자료로 함께 살펴보는 데 사용합니다."],
     "이 검사는 스트레스 정도를 가늠하는 참고 지표이며, 마음 상태의 진단이 아닙니다. 같은 계열 장비(uBioMacpa Pro)를 대학생 대상으로 검증한 2025년 연구에서도 스트레스 설문 점수와 통계적으로 유의한 상관이 확인되었으나 그 크기는 크지 않았습니다. 그래서 본원에서는 이 결과를 단독으로 판단하지 않고 문진과 함께 해석합니다.",
     [("uBioMacpa Pro 스트레스 측정 도구 검증 연구 (PeerJ, 2025)", "https://peerj.com/articles/19830")]),
    ("d3", "인바디 270S로는 무엇을 보나요?",
     ["체중계로는 알 수 없는 근육량·체지방량·체수분을 나누어 보는 체성분 분석 장비입니다. 손과 발의 전극에 닿은 채 서 있으면, 몸에 느껴지지 않을 정도의 약한 전류가 흐르며 전기 저항(임피던스)을 측정합니다. 수분이 많은 근육은 전기가 잘 흐르고 지방은 덜 흐르는 성질을 이용한 방식(생체전기임피던스법)입니다.",
      "제조사에 따르면 270S는 3개 주파수·5개 몸 부위에서 총 15회의 임피던스를 측정하고, 나이·성별·인종에 따른 경험적 추정치를 쓰지 않고 측정값으로 결과를 계산한다고 합니다. 검사는 수십 초면 끝납니다.",
      "다이어트, 부종, 근육 감소가 걱정되는 분께 몸무게 한 가지가 아니라 '무엇이 변했는지'를 설명드리는 데 사용합니다."],
     "식사·운동·땀·수분 섭취와 부종 상태에 따라 수치가 달라질 수 있어, 같은 조건에서 반복 측정해 변화를 비교하는 것이 의미 있습니다. 심박동기 등 전자 의료기기를 몸에 삽입하신 분은 미리 알려 주세요.",
     [("InBody 270S 제품 안내 (인바디)", "https://inbody.in/product/inbody-270.php"),
      ("InBody 270S 사양 (인바디)", "https://ekp.inbody.com/en/inbody/contents/view_270")]),
    ("d4", "혈압은 왜 재나요?",
     ["혈압과 맥박은 몸 상태를 보는 가장 기본적인 수치입니다. 두통·어지럼·가슴 두근거림·부종으로 오신 분께 확인하고, 한약을 처방하기 전에도 기본으로 살펴봅니다.",
      "자동혈압계는 팔에 커프를 감싸 측정하기 때문에 측정하는 사람에 따른 차이를 줄이고, 같은 방법으로 반복 측정해 변화를 비교하기 좋습니다."],
     "혈압은 긴장하거나 방금 움직였을 때 높게 나올 수 있어, 앉아서 충분히 쉰 뒤 측정하고 필요하면 다시 잽니다. 한 번의 수치로 고혈압을 진단하지 않으며, 높은 수치가 반복되면 의료기관 진료를 안내해 드립니다.",
     []),
    ("d5", "키와 체중은 왜 꼼꼼히 재나요?",
     ["키와 체중으로 체질량지수(BMI)를 계산하고, 소아 성장 진료에서는 같은 기기로 일정한 간격을 두고 재어 자라는 속도를 살펴봅니다. 다이어트 상담에서는 체중 변화의 경과를 확인하는 기본 자료가 됩니다.",
      "자동신장체중계는 키와 체중을 한 번에 측정하고 기록할 수 있어, 아이들이 오실 때마다 같은 조건으로 비교하기 쉽습니다."],
     "시간대와 옷차림에 따라 체중은 달라질 수 있어, 가능하면 비슷한 조건에서 측정합니다.",
     []),
    ("d6", "혈당측정기로는 무엇을 확인하나요?",
     ["손끝에서 아주 적은 양의 혈액을 채취해 그 순간의 혈당을 바로 확인하는 장비입니다. 갈증이 심하거나 쉽게 피로하고 체중이 크게 변한 분, 식후 어지럼이나 무기력감을 호소하시는 분의 선별 참고 자료로 사용합니다.",
      "혈당측정기의 정확도에는 국제표준(ISO 15197:2013)이 있습니다. 이 표준은 측정값의 95% 이상이 기준 검사값과 비교해 100mg/dL 미만에서는 ±15mg/dL 이내, 100mg/dL 이상에서는 ±15% 이내에 들어야 한다고 요구합니다."],
     "혈당은 식사 시간에 따라 크게 달라지고, 혈당측정기 수치만으로 당뇨병을 진단하지 않습니다. 높게 나오면 의료기관에서 정밀검사를 받으시도록 안내해 드립니다.",
     [("ISO 15197:2013 혈당측정기 정확도 기준 (ISO)", "https://www.iso.org/news/2013/06/Ref1749.html"),
      ("ISO 15197:2013 정확도 평가 방법 (Jendrike 등, 2017)", "https://pmc.ncbi.nlm.nih.gov/articles/PMC5951056")]),
    ("d7", "한의원에서 혈액검사는 어떻게 하나요?",
     ["본원은 후지필름의 건식 화학 분석기 DRI-CHEM NX500i를 사용합니다. 얇은 필름(슬라이드) 한 장에 혈장 등 시료를 한 방울(검사 1항목당 약 10μL) 떨어뜨리면, 필름 안에서 일어난 색 변화를 장비가 읽어 수치로 바꿔 주는 방식입니다. 제조사 자료에 따르면 자동으로 시료를 떨어뜨리고 결과가 수 분 안에 나옵니다.",
      "이 장비가 측정할 수 있는 대표 항목은 간 기능(AST, ALT, GGT, ALP, 빌리루빈), 신장 기능(BUN, 크레아티닌), 혈당, 지질(총콜레스테롤, 중성지방, HDL 콜레스테롤), 요산, 단백질·알부민, 전해질, 염증 수치(CRP) 등입니다. 실제로 어떤 항목을 검사할지는 환자분의 상태에 따라 달라집니다.",
      "제조사는 검사 정보가 슬라이드 뒷면 바코드로 자동 입력되고, 유효기간이 지난 슬라이드는 결과가 나오지 않도록 설계되어 있으며, 등록된 검사자만 장비를 사용할 수 있는 기능이 있다고 설명합니다. 사람의 실수로 생길 수 있는 오류를 줄이기 위한 장치입니다.",
      "한약을 드시기 전 간·신장 기능 등 몸 상태를 확인하고, 복용 중간에 경과를 살피는 참고 자료로 사용합니다. 검사 전에 목적을 설명드리고 동의를 받은 뒤 진행하며, 채혈은 위생 절차에 따라 필요한 만큼만 합니다."],
     "혈액검사 결과는 질병의 확진이 아니라 진료를 위한 참고 자료입니다. 수치가 정상 범위를 벗어났을 때는 결과를 설명드리고, 정밀검사와 진료가 가능한 의료기관을 안내해 드립니다.",
     [("DRI-CHEM NX500 제품 개요 (후지필름)", "https://www.fujifilm.com/cy/en/healthcare/in-vitro-diagnostics/chemical-analysis/dri-chem-nx500"),
      ("DRI-CHEM NX500 측정 항목·사양 (후지필름)", "https://www.fujifilm.com/au/en/healthcare/poct/chemical-analysis/dri-chem-nx500/specifications")]),
]

GENERAL = [
    ("검사 결과로 병명을 진단하나요?",
     "아니요. 이 장비들의 결과는 한의사가 진찰할 때 참고하는 보조 자료입니다. 문진과 진찰, 그리고 검사 결과를 종합해 한의학적으로 판단하며, 질병의 확진이 필요하다고 보이면 해당 의료기관 진료를 안내해 드립니다."),
    ("검사는 모두 받아야 하나요?",
     "아니요. 진찰 후 필요하다고 판단되는 검사만 권해 드립니다. 어떤 검사를 왜 하는지 먼저 설명드리고, 원하지 않으시면 말씀해 주세요. 검사를 받지 않으셔도 진료는 진행됩니다."),
    ("결과가 정상 범위를 벗어나면 어떻게 되나요?",
     "수치가 무엇을 뜻하는지 먼저 설명드립니다. 한의 진료로 경과를 살필 수 있는 상태인지 판단하고, 한의 진료 범위를 넘는 소견이 의심되면 정밀검사와 진료가 가능한 의료기관을 안내합니다."),
    ("검사가 아프거나 위험하지는 않나요?",
     "맥영상 검사기, 유비오맥파, 인바디, 혈압계, 신장체중계는 몸에 상처를 내지 않는 검사입니다. 혈당 검사와 혈액검사는 필요한 만큼만 소량 채혈합니다. 인바디는 심박동기 등 전자 의료기기를 삽입하신 분께 맞지 않을 수 있으니 미리 알려 주세요."),
]


def overview_table():
    out = ['<div class="ft-wrap"><table class="ft"><caption>검사 장비 한눈에 보기</caption>'
           '<thead><tr><th scope="col">장비</th><th scope="col">보는 것</th><th scope="col" style="text-align:left">주로 쓰는 때</th></tr></thead><tbody>']
    for name, what, when in OVERVIEW:
        out.append('<tr><th scope="row">%s</th><td>%s</td><td>%s</td></tr>' % (esc(name), esc(what), esc(when)))
    out.append("</tbody></table></div>")
    return "".join(out)


def device_block(i, dev):
    did, q, paras, note, srcs = dev
    body = "".join("<p>%s</p>" % esc(p) for p in paras)
    body += '<p class="memo"><b>알아두실 점</b> · %s</p>' % esc(note)
    if srcs:
        body += '<p class="memo">근거 자료 · ' + " / ".join(
            '<a href="%s" target="_blank" rel="noopener nofollow">%s</a>' % (esc(u), esc(n)) for n, u in srcs) + "</p>"
    return ('<details class="qa" id="%s"%s><summary><span class="q">Q</span>%s</summary>'
            '<div class="a"><span class="aa">A</span><div>%s</div></div></details>'
            % (did, " open" if i == 0 else "", esc(q), body))


EXTRA_CSS = """
  .memo a{color:var(--pine);text-decoration:underline;text-underline-offset:2px}
  .ft tbody td{color:var(--ink-soft)}
"""


def build():
    src = open(TEMPLATE, encoding="utf-8").read()
    head_end = src.index("</head>")
    head = src[:head_end]
    title = "진단 및 검사 — 맥영상·인바디·혈액검사 장비 안내 | 부천 지인한의원"
    desc = ("부천 지인한의원이 진료에 사용하는 검사 장비 안내. 3차원 맥영상 검사기, 유비오맥파, 인바디 270S, 혈압계, "
            "신장체중계, 혈당측정기, 혈액검사기(DRI-CHEM NX500i)로 무엇을 보는지 쉽게 설명합니다.")
    head = re.sub(r"<title>.*?</title>", "<title>%s</title>" % esc(title), head, count=1, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % esc(desc), head, count=1)
    head = head.replace("https://jeeinclinic.com/clinic/parking/", "https://jeeinclinic.com/special/diagnosis/")
    head = re.sub(r"\n  /\* DIAG:START \*/.*?/\* DIAG:END \*/", "", head, flags=re.S)
    head = head.replace("</style>", "  /* DIAG:START */" + bf.CSS + EXTRA_CSS + "  /* DIAG:END */\n</style>", 1)

    faq = [(d[1], " ".join(d[2])) for d in DEVICES] + list(GENERAL)
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

    pledge = "".join("<div><b>%s</b>%s</div>" % (esc(b), esc(t)) for b, t in PLEDGE)
    devices = "\n  ".join(device_block(i, d) for i, d in enumerate(DEVICES))
    general = "\n  ".join(bf.general_block(i, q, a) for i, (q, a) in enumerate(GENERAL))

    article = """<article>
  <div class="eyebrow">특별한치료법 · 진단 및 검사</div>
  <h1>진찰은 손끝에서 시작해,<br><em style="font-style:normal;color:var(--seal)">수치로 확인</em>합니다</h1>
  <p class="lead">지인한의원은 문진·맥진 같은 한의학적 진찰에 더해, 몸 상태를 수치와 그래프로 확인할 수 있는 검사 장비를 갖추고 있습니다. 어떤 장비로 무엇을 보는지, 결과를 어떻게 사용하는지 환자분이 이해하실 수 있도록 풀어 설명드립니다.</p>
  <h2 class="h2b" style="margin-top:26px">검사를 사용하는 원칙</h2>
  <div class="pledge">%s</div>
  %s
  <h2 class="h2b" style="margin-top:30px">장비별 안내 Q&amp;A</h2>
  %s
  <h2 class="h2b" style="margin-top:34px">검사에 대해 자주 묻는 질문</h2>
  %s
  <div class="closing">
    <b>한의학적 진찰과 객관적인 자료를 함께 봅니다.</b>
    <p>한의사의 진찰을 중심에 두고, 검사 결과는 환자분께 설명드리는 근거 자료로 사용합니다. 궁금한 점은 진료 중에 언제든 물어보세요.</p>
  </div>
  <p class="src">※ 장비 설명은 제조사 공개 자료와 공개 문헌에 근거했으며, 장비의 성능과 측정 항목은 제품·설정에 따라 다를 수 있습니다. 검사 결과는 질병의 진단이 아니라 진료 참고 자료입니다.</p>
  <div class="ctas">
    <a class="c-call" href="tel:0507-1387-2933">📞 0507-1387-2933</a>
    <a class="c-kakao" href="https://pf.kakao.com/_xmxhmpxj/chat" target="_blank" rel="noopener">💬 카카오톡 문의</a>
    <a class="c-naver" href="https://booking.naver.com/booking/13/bizes/185044" target="_blank" rel="noopener">네이버 예약</a>
  </div>
  <h2>특별한치료법의 다른 안내</h2>
  <div class="sib"><a href="/special/high-dose-bee-venom/">고농도봉침</a><a href="/treatments/">약침·매선·도침·정안침</a><a href="/special/suseung-hwagang/">수승화강약침</a><a href="/special/uihak-ipmun-maekjin/">의학입문맥진</a><a href="/special/diagnosis/" aria-current="page">진단 및 검사</a></div>
</article>""" % (pledge, overview_table(), devices, general)

    a0 = src.index("<article>")
    a1 = src.index("</article>") + len("</article>")
    page = head + "</head>" + src[head_end + len("</head>"):a0] + article + src[a1:]
    page = page.replace("</head>", '<script type="application/ld+json">%s</script>\n</head>' % json.dumps(ld, ensure_ascii=False), 1)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(page)
    print("diagnosis page written:", OUT, len(page))


if __name__ == "__main__":
    build()
