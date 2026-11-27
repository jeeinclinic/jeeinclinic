# -*- coding: utf-8 -*-
"""유루증(/eent/eye/tearing/) 페이지 생성. python3 scripts/build_tearing.py && python3 scripts/apply_nav.py (scripts/에서)
의료법 제56조 제2항 준수: 치료 효과 단정·'전문의' 강조·타 기관 비교·논문 성과 과장 없음."""
import json, os, re
import build_fees as bf
esc = bf.esc
OUT = os.path.join(bf.ROOT, "eent", "eye", "tearing", "index.html")

PLEDGE = [
    ("눈 상태를 먼저 나눠 봅니다", "눈물이 너무 많이 만들어지는지, 빠져나가는 길이 좁아졌는지를 문진과 진찰로 먼저 가려 봅니다."),
    ("함께 있는 불편도 같이 봅니다", "눈 건조감, 코 증상, 알레르기, 생활환경처럼 눈물에 영향을 주는 요인을 함께 살핍니다."),
    ("치료 방법은 설명 후 정합니다", "침·약침·봉침·한약·증류한약액 중 어떤 방법을 쓸지 진찰 후 설명드리고, 동의하신 뒤에 진행합니다."),
]

QA = [
    ("유루증은 어떤 상태인가요?",
     ["유루증(눈물흘림증)은 슬프거나 눈이 아픈 것도 아닌데 눈물이 눈 밖으로 넘쳐 뺨으로 흐르는 상태입니다. 눈물이 많이 흐르면 시야가 뿌옇게 느껴져 자꾸 닦게 되고, 눈 주변 피부가 짓무르기도 합니다.",
      "눈물은 눈 표면을 적신 뒤 눈 안쪽 끝의 눈물점으로 들어가 눈물소관, 눈물주머니, 비루관을 지나 코 안쪽으로 빠져나가는 것이 정상입니다. 이 흐름 어딘가에 문제가 생기면 눈물이 넘칠 수 있습니다."],
     "병명이 아니라 '눈물이 넘쳐흐른다'는 증상을 부르는 말입니다. 원인에 따라 살펴야 할 곳이 달라서 먼저 원인을 나누어 보는 것이 중요합니다.", []),
    ("왜 눈물이 흐르나요?",
     ["크게 두 가지로 나누어 봅니다. 첫째는 눈물이 빠져나가는 길이 좁아지거나 막힌 경우입니다. 노화, 만성 염증 등으로 눈물점이나 눈물관, 비루관이 좁아지면 눈물이 고였다가 넘칩니다.",
      "둘째는 길은 열려 있지만 눈물이 지나치게 만들어지는 경우입니다. 찬바람·건조한 공기·알레르기·눈 표면의 염증처럼 눈이 자극을 받으면 반사적으로 눈물이 많이 나옵니다."],
     "겨울에 찬바람을 맞을 때만 심해지는 분도 있고, 한쪽 눈만 계속 고이는 분도 있습니다. 어느 쪽 눈인지, 언제 심해지는지를 진료 때 알려 주시면 원인을 가리는 데 도움이 됩니다.", []),
    ("눈물이 흐르는데 눈은 왜 뻑뻑한가요?",
     ["두 증상이 함께 나타나는 분이 있습니다. 눈 표면을 덮는 눈물막은 기름층·수성층·점액층으로 이루어져 있는데, 이 막이 불안정하면 눈이 건조하고 이물감이 생깁니다. 이때 눈이 자극에 예민해져서 바람이나 먼지에 눈물이 반사적으로 쏟아지기도 합니다.",
      "그래서 '눈물이 많은데 눈은 건조한' 상태가 생길 수 있고, 이런 경우에는 눈물을 줄이는 것만이 아니라 눈 표면 상태를 함께 살펴야 합니다."],
     "눈물의 양이 아니라 눈물막의 질과 안정성이 문제인 경우가 있습니다. 안구건조 페이지에서 눈물막을 더 자세히 설명하고 있습니다.",
     [("눈물막과 안구건조증 (질병관리청 건강정보)", "https://health.kdca.go.kr/healthinfo/index.jsp")]),
    ("한의학에서는 유루증을 어떻게 보나요?",
     ["한의학에서는 눈물이 흐르는 양상과 함께 나타나는 증상을 살펴, 몸의 상태를 찬 쪽·열 쪽, 진액이 부족한 쪽 등으로 나누어 이해합니다. 눈 증상만 보지 않고 소화, 수면, 피로, 코 증상 같은 전신 상태를 함께 묻는 것이 특징입니다.",
      "같은 유루증이라도 사람마다 몸 상태가 다르기 때문에, 진찰 후 환자분께 맞게 진료 계획을 세웁니다."],
     "같은 유루증이라도 사람마다 원인과 몸 상태가 달라 진료 계획도 달라집니다.", []),
    ("진료는 어떻게 진행되나요?",
     ["먼저 증상이 언제 시작됐는지, 한쪽인지 양쪽인지, 눈곱·가려움·충혈이 있는지, 찬바람이나 실내 건조에서 심해지는지, 콧병이나 알레르기가 있는지 여쭙습니다. 이어서 눈 주변을 살피고 한의학적 진찰을 합니다.",
      "진찰 결과를 바탕으로 침치료, 약침치료, 봉침치료, 한약, 눈에 넣는 증류한약액 치료 중에서 환자분의 상태에 맞는 방법을 정합니다. 침·약침·봉침은 눈 주변과 몸의 관련 부위에 시술하고, 한약은 몸 상태에 맞춰 처방하며, 증류한약액은 눈에 직접 넣어 사용하는 방식입니다. 하나만 쓰기도 하고 여러 가지를 함께 쓰기도 합니다."],
     "봉침은 벌독을 이용하는 치료라 시술 전에 반응 검사를 하고, 벌독 알레르기가 있거나 과거 봉침 후 이상 반응이 있었다면 반드시 알려 주셔야 합니다. 임신 중이시거나 복용 중인 약이 있어도 미리 말씀해 주세요. 어떤 치료를 받을지는 설명을 듣고 직접 선택하시면 됩니다.", []),
    ("집에서 할 수 있는 관리가 있나요?",
     ["찬바람이 심한 날에는 모자나 안경으로 눈을 가려 주고, 실내가 건조하면 가습으로 습도를 맞춰 주세요. 화면을 오래 볼 때는 눈 깜빡임이 줄어 눈 표면이 마르기 쉬우니 중간중간 눈을 쉬어 주세요.",
      "눈을 자주 비비거나 닦으면 눈 주변 피부와 눈 표면이 더 자극받으니 부드러운 휴지로 눌러 닦는 정도로 하고, 손은 깨끗이 씻으세요. 인공눈물 등 안약은 눈 상태에 따라 맞는 종류가 달라서 약사나 의료진과 상담해 쓰시길 권합니다."],
     "생활 관리는 진료를 대신하는 것이 아니라 불편을 줄이는 데 도움이 되는 기본 수칙입니다.",
     [("눈이 뻑뻑하고 침침할 때 관리법 (질병관리청 건강정보)", "https://health.kdca.go.kr/healthinfo/biz/health/ntcnInfo/healthSourc/thtimtCntnts/thtimtCntntsView.do?thtimt_cntnts_sn=212")]),
]

GENERAL = [
    ("진료를 받으면 눈물이 멎나요?",
     "원인과 상태에 따라 경과가 다르고 결과를 미리 약속드릴 수는 없습니다. 진찰 후 원인으로 보이는 부분과 진료 방향, 생활 관리를 설명드리고 경과를 보며 조정합니다."),
    ("진료 예약은 어떻게 하나요?",
     "전화, 카카오톡 문의, 네이버 예약으로 가능합니다. 진료시간은 평일 9시 30분~20시 30분, 토요일 9시~15시입니다."),
]

EXTRA_CSS = ".memo a{color:var(--pine);text-decoration:underline;text-underline-offset:2px}\n"


def block(i, d):
    q, paras, note, srcs = d
    body = "".join("<p>%s</p>" % esc(p) for p in paras) + '<p class="memo"><b>알아두실 점</b> · %s</p>' % esc(note)
    if srcs:
        body += '<p class="memo">참고 자료 · ' + " / ".join('<a href="%s" target="_blank" rel="noopener nofollow">%s</a>' % (esc(u), esc(n)) for n, u in srcs) + "</p>"
    return ('<details class="qa" id="q%d"%s><summary><span class="q">Q</span>%s</summary><div class="a"><span class="aa">A</span><div>%s</div></div></details>'
            % (i + 1, " open" if i == 0 else "", esc(q), body))


def build():
    src = open(bf.TEMPLATE, encoding="utf-8").read()
    he = src.index("</head>")
    head = src[:he]
    title = "유루증(눈물흘림증) — 원인과 진료 안내 | 부천 지인한의원"
    desc = "눈물이 자꾸 흐르는 유루증의 원인(눈물길 문제·눈물 과다 분비), 안구건조와 함께 나타나는 이유, 진료 방법과 생활 관리를 부천 지인한의원이 쉽게 설명합니다."
    head = re.sub(r"<title>.*?</title>", "<title>%s</title>" % esc(title), head, count=1, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % esc(desc), head, count=1)
    head = head.replace("https://jeeinclinic.com/clinic/parking/", "https://jeeinclinic.com/eent/eye/tearing/")
    head = head.replace("</style>", "  /* TEAR:START */" + bf.CSS + EXTRA_CSS + "  /* TEAR:END */\n</style>", 1)
    faq = [(d[0], " ".join(d[1])) for d in QA] + list(GENERAL)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    pledge = "".join("<div><b>%s</b>%s</div>" % (esc(b), esc(t)) for b, t in PLEDGE)
    qa = "\n  ".join(block(i, d) for i, d in enumerate(QA))
    gen = "\n  ".join(bf.general_block(i, q, a) for i, (q, a) in enumerate(GENERAL))
    art = """<article>
  <div class="eyebrow">눈 · 유루증</div>
  <h1>이유 없이 흐르는 눈물,<br><em style="font-style:normal;color:var(--seal)">유루증</em></h1>
  <p class="lead">슬프지도 아프지도 않은데 눈물이 넘쳐 자꾸 닦게 되시나요? 유루증은 눈물이 너무 많이 만들어지거나, 빠져나가는 길이 좁아졌을 때 생깁니다. 원인을 나누어 보는 방법과 진료 방법, 집에서의 관리를 정리했습니다.</p>
  <h2 class="h2b" style="margin-top:26px">진료의 기본 원칙</h2>
  <div class="pledge">%s</div>
  <h2 class="h2b" style="margin-top:30px">유루증 Q&amp;A</h2>
  %s
  <h2 class="h2b" style="margin-top:34px">자주 묻는 질문</h2>
  %s
  <div class="closing"><b>눈물의 원인을 먼저 나누어 봅니다.</b><p>궁금한 점은 진료 중에 언제든 물어보세요.</p></div>
  <p class="src">※ 이 글은 일반적인 의학 정보이며 개인의 진단·치료를 대신하지 않습니다. 정확한 진단과 치료는 의료진과 상담하세요.</p>
  <div class="ctas">
    <a class="c-call" href="tel:0507-1387-2933">📞 0507-1387-2933</a>
    <a class="c-kakao" href="https://pf.kakao.com/_xmxhmpxj/chat" target="_blank" rel="noopener">💬 카카오톡 문의</a>
    <a class="c-naver" href="https://booking.naver.com/booking/13/bizes/185044" target="_blank" rel="noopener">네이버 예약</a>
  </div>
  <h2>눈 관련 다른 안내</h2>
  <div class="sib"><a href="/eent/eye/dry-eye/">안구건조</a><a href="/eent/eye/tearing/" aria-current="page">유루증</a><a href="/eent/eye/eye-fatigue/">눈 피로</a><a href="/eent/eye/eyelid-twitching/">눈떨림</a><a href="/eent/eye/itchy-eye/">눈 가려움</a></div>
</article>""" % (pledge, qa, gen)
    rest = src[he + len("</head>"):]
    a0, a1 = rest.index("<article>"), rest.index("</article>") + len("</article>")
    page = head + "</head>" + rest[:a0] + art + rest[a1:]
    page = page.replace("</head>", '<script type="application/ld+json">%s</script>\n</head>' % json.dumps(ld, ensure_ascii=False), 1)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(page)
    print("written", OUT)

if __name__ == "__main__":
    build()
