# -*- coding: utf-8 -*-
"""칼럼 페이지(/columns/) 생성기.

- data/columns.json  : 홈페이지용으로 재작성한 칼럼(사이트 내 페이지) 목록 — 여기에 항목을 추가하면 자동 반영
- data/topics.json   : 진료분야별 칼럼 모음(허브) 글 수
- data/blog-posts.json : 네이버 블로그 최신 글
→ /columns/index.html
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://jeeinclinic.com"
LATEST_BLOG = 12


def esc(s):
    return html.escape(s, quote=True)


def load(name, default):
    p = os.path.join(ROOT, "data", name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else default


def trim(desc):
    desc = re.sub(r"\s+", " ", desc or "").strip()
    best = -1
    for m in re.finditer(r"(다\.|요\.|요\?|까\?|죠\.|!|\?)", desc):
        best = m.end()
    return desc[:best] if best > 60 else desc + "…"


CSS = open(os.path.join(ROOT, "scripts", "topic_style.css"), encoding="utf-8").read()
CSS += """
  .col.site{border-color:rgba(43,66,50,.28)}
  .col.site .cgo{color:var(--pine)}
  .col .ctag{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.5px;color:var(--seal);border:1px solid rgba(178,58,46,.35);border-radius:999px;padding:1px 8px;margin-left:8px;vertical-align:1px}
  .others a .n{color:var(--ochre);margin-left:5px;font-weight:700}
"""


def main():
    cols = sorted(load("columns.json", []), key=lambda c: c["date"], reverse=True)
    topics = load("topics.json", {})
    posts = sorted(load("blog-posts.json", []), key=lambda p: p.get("date", ""), reverse=True)
    posts = [p for p in posts if "진료시간" not in p["title"]][:LATEST_BLOG]
    lastmod = max([c["date"] for c in cols] + [p["date"] for p in posts[:1]] or ["2026-11-13"])

    site_cards = "\n".join(
        '    <a class="col site" href="%s">\n'
        '      <span class="cdate">%s<span class="ctag">%s</span></span>\n'
        '      <span class="ctitle">%s</span>\n'
        '      <span class="cdesc">%s</span>\n'
        '      <span class="cgo">칼럼 읽기 →</span>\n'
        '    </a>' % (esc(c["url"]), esc(c["date"].replace("-", ".")), esc(c.get("topic", "")), esc(c["title"]), esc(c["summary"]))
        for c in cols)

    hub_links = [("/facial-palsy/", "구안와사 · 안면마비", None), ("/trigeminal-neuralgia/", "삼차신경통", None)]
    hub_links += [("/%s/" % k, v["name"], v["count"]) for k, v in topics.items()]
    hubs = "\n      ".join(
        '<a href="%s">%s%s</a>' % (h, esc(n), ('<span class="n">%d</span>' % c) if c else "") for h, n, c in hub_links)

    blog_cards = "\n".join(
        '    <a class="col" href="%s" target="_blank" rel="noopener">\n'
        '      <span class="cdate">원장 블로그 · %s</span>\n'
        '      <span class="ctitle">%s</span>\n'
        '      <span class="cdesc">%s</span>\n'
        '      <span class="cgo">네이버 블로그에서 읽기 ↗</span>\n'
        '    </a>' % (esc(p["link"]), esc(p["date"].replace("-", ".")), esc(p["title"]), esc(trim(p["desc"])))
        for p in posts)

    ld = {
        "@context": "https://schema.org", "@type": "CollectionPage",
        "name": "이은혜 원장 칼럼 | 부천 지인한의원", "url": SITE + "/columns/", "inLanguage": "ko",
        "publisher": {"@id": SITE + "/#clinic"},
        "mainEntity": {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": SITE + c["url"], "name": c["title"]}
            for i, c in enumerate(cols)]},
    }
    desc = "부천 지인한의원 이은혜 대표원장의 건강 칼럼 — 구안와사·삼차신경통, 소아, 여성질환, 통증, 피부까지 진료 현장에서 자주 받는 질문에 답합니다."

    page = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- 이 파일은 scripts/build_columns.py가 생성합니다. 칼럼 추가는 data/columns.json에서 하세요. -->
<title>칼럼 — 이은혜 원장 건강 칼럼 | 부천 지인한의원</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{SITE}/columns/">
<meta property="og:type" content="website">
<meta property="og:title" content="칼럼 — 이은혜 원장 건강 칼럼 | 부천 지인한의원">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{SITE}/columns/">
<link rel="icon" type="image/png" href="/images/favicon-512.png">
<link rel="apple-touch-icon" href="/images/favicon-512.png">
<meta property="og:image" content="https://jeeinclinic.com/images/og-main.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://jeeinclinic.com/images/og-main.png">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@500;700;900&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
<style>
{CSS}
</style>
</head>
<body>

<header>
  <div class="topbar">
    <a class="brand" href="/"><span class="bseal">知人</span><span class="btxt"><span class="b1">지인한의원</span><span class="b2">부천 중동 · JEEIN CLINIC</span></span></a>
    <span style="display:flex;gap:8px;align-items:center"><a class="home-btn" href="/">🏠 홈</a><a class="top-call" href="tel:032-323-2933">032-323-2933</a></span>
  </div>
</header>

<div class="wrap">
<article>

  <div class="eyebrow">COLUMN · 칼럼</div>
  <h1>진료실에서 자주 받는 질문,<br><em>칼럼</em>으로 답합니다</h1>
  <p class="byline">글·감수 <strong><a href="/about/" style="color:inherit">이은혜</a></strong> 한의사 (지인한의원 대표원장)</p>

  <div class="answer">구안와사·삼차신경통 같은 안면 신경 질환부터 소아, 여성질환, 통증, 피부까지 — 환자분들이 진료실에서 실제로 물어보시는 질문을 원장이 직접 쓰고 감수한 글로 모았습니다.</div>

  <h2>지인한의원 칼럼 <span class="cnt">{len(cols)}편</span></h2>
  <p class="sub">홈페이지에서 바로 읽을 수 있도록 정리한 칼럼입니다.</p>
  <div class="cols">
{site_cards}
  </div>

  <h2>진료분야별 칼럼 모음</h2>
  <p class="sub">분야를 고르면 해당 주제의 원장 칼럼을 한 번에 볼 수 있습니다.</p>
  <div class="others">
      {hubs}
  </div>

  <h2>최신 블로그 글</h2>
  <p class="sub">원장이 네이버 블로그에 직접 쓴 최신 글이 자동으로 올라옵니다. <a href="/blog/" style="font-weight:700">전체 칼럼 검색하기 →</a></p>
  <div class="cols">
{blog_cards}
  </div>

  <div class="cta-box">
    <h3>궁금한 증상이 있다면, 편하게 문의하세요</h3>
    <p>부천시 원미구 소향로 135, 3층 (부천시청역 2번 출구 도보 3분) · 평일 매일 저녁 8:30까지 · 토 09:00–15:00</p>
    <div class="ctas">
      <a class="c-call" href="tel:032-323-2933">📞 032-323-2933</a>
      <a class="c-kakao" href="https://pf.kakao.com/_xmxhmpxj/chat" target="_blank" rel="noopener">💬 카카오톡</a>
      <a class="c-naver" href="https://booking.naver.com/booking/13/bizes/185044" target="_blank" rel="noopener">네이버 예약</a>
    </div>
  </div>

  <p class="disc" style="margin-bottom:0">본 칼럼은 일반적인 건강 정보이며 의학적 진단·처방을 대신하지 않습니다. 증상이 계속되거나 심해지면 반드시 의료기관에 내원해 진료를 받으시기 바랍니다. 치료 효과와 기간은 개인에 따라 다를 수 있습니다.</p>

</article>
</div>

<footer>
  <div class="wrap">
    <div class="f-brand">지인한의원</div>
    <p>경기도 부천시 원미구 소향로 135, 3층 · 대표(원장) 이은혜 · 전화 032-323-2933</p>
    <p>진료시간 — 월~금 09:30–20:30 / 토 09:00–15:00 / 일·공휴일 휴진 (점심시간 없이 진료)</p>
  </div>
</footer>

</body>
</html>
"""
    d = os.path.join(ROOT, "columns")
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, "index.html")
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    if old != page:
        open(path, "w", encoding="utf-8").write(page)
    print("columns: site=%d blog=%d lastmod=%s changed=%s" % (len(cols), len(posts), lastmod, old != page))


if __name__ == "__main__":
    main()
