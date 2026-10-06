# -*- coding: utf-8 -*-
"""진료분야 허브 페이지 생성기.

topics_config.py + data/blog-posts.json → /<slug>/index.html
블로그 새 글이 키워드에 걸리면 매일 자동으로 '원장 칼럼' 목록에 추가된다.
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from topics_config import TOPICS  # noqa: E402

SITE = "https://jeeinclinic.com"
TODAY_FALLBACK = "2026-10-06"
EXTRA_LINKS = [("/facial-palsy/", "구안와사 · 안면마비"), ("/trigeminal-neuralgia/", "삼차신경통")]
SKIP_TITLES = ["진료시간"]


def load_posts():
    path = os.path.join(ROOT, "data", "blog-posts.json")
    with open(path, encoding="utf-8") as f:
        posts = json.load(f)
    posts = [p for p in posts if not any(s in p["title"] for s in SKIP_TITLES)]
    return sorted(posts, key=lambda p: p.get("date", ""), reverse=True)


def match(topic, post):
    t = post["title"]
    if any(x in t for x in topic.get("exclude", [])):
        return False
    return any(k in t for k in topic["keywords"])


def trim(desc):
    desc = re.sub(r"\s+", " ", desc or "").strip()
    best = -1
    for m in re.finditer(r"(다\.|요\.|요\?|까\?|죠\.|!|\?)", desc):
        best = m.end()
    if best > 60:
        return desc[:best]
    return desc + "…"


def esc(s):
    return html.escape(s, quote=True)


CSS = open(os.path.join(ROOT, "scripts", "topic_style.css"), encoding="utf-8").read()


def nav_html(cur):
    links = EXTRA_LINKS + [("/%s/" % t["slug"], t["name"]) for t in TOPICS]
    out = []
    for href, name in links:
        if href == "/%s/" % cur:
            continue
        out.append('<a href="%s">%s</a>' % (href, esc(name)))
    return "\n      ".join(out)


def build(topic, posts):
    slug = topic["slug"]
    url = "%s/%s/" % (SITE, slug)
    mine = [p for p in posts if match(topic, p)]
    lastmod = mine[0]["date"] if mine else TODAY_FALLBACK

    page_ld = {
        "@context": "https://schema.org",
        "@type": "MedicalWebPage",
        "name": topic["title"].split(" | ")[0],
        "url": url,
        "inLanguage": "ko",
        "about": {"@type": "MedicalCondition", "name": topic["condition"]},
        "publisher": {"@id": SITE + "/#clinic"},
        "lastReviewed": lastmod,
        "reviewedBy": {"@type": "Person", "@id": SITE + "/about/#doctor", "name": "이은혜",
                       "jobTitle": "한의사 · 지인한의원 대표원장"},
    }
    if mine:
        page_ld["hasPart"] = [{
            "@type": "BlogPosting", "headline": p["title"], "url": p["link"],
            "datePublished": p["date"],
            "author": {"@type": "Person", "@id": SITE + "/about/#doctor", "name": "이은혜"},
        } for p in mine[:30]]
    faq_ld = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in topic["faq"]],
    }

    sym = ""
    if topic["symptoms"]:
        lis = "\n".join("      <li>☐ %s</li>" % esc(s) for s in topic["symptoms"])
        sym = '\n  <h2>이런 증상으로 오십니다</h2>\n  <div class="check">\n    <ul>\n%s\n    </ul>\n  </div>\n' % lis

    how = ""
    if topic["how"]:
        how = "\n  <h2>지인한의원은 이렇게 봅니다</h2>\n  %s\n" % topic["how"]

    er = '\n  <div class="er">%s</div>\n' % topic["er"] if topic["er"] else ""

    if mine:
        cards = []
        for p in mine:
            cards.append(
                '    <a class="col" href="%s" target="_blank" rel="noopener">\n'
                '      <span class="cdate">원장 칼럼 · %s</span>\n'
                '      <span class="ctitle">%s</span>\n'
                '      <span class="cdesc">%s</span>\n'
                '      <span class="cgo">네이버 블로그에서 전문 읽기 ↗</span>\n'
                '    </a>' % (esc(p["link"]), esc(p["date"].replace("-", ".")), esc(p["title"]), esc(trim(p["desc"]))))
        cols = "\n".join(cards)
        colsec = ('\n  <h2>이은혜 원장 칼럼 <span class="cnt">%d편</span></h2>\n'
                  '  <p class="sub">원장이 블로그에 직접 쓴 글입니다. 새 글이 올라오면 이 목록에 자동으로 추가됩니다.</p>\n'
                  '  <div class="cols">\n%s\n  </div>\n'
                  '  <p class="sub" style="margin-top:12px"><a href="/blog/" style="font-weight:700">전체 칼럼 검색하기 →</a></p>\n') % (len(mine), cols)
    else:
        colsec = ('\n  <h2>이은혜 원장 칼럼</h2>\n'
                  '  <p class="sub">관련 칼럼이 올라오면 이곳에 자동으로 추가됩니다. <a href="/blog/" style="font-weight:700">전체 칼럼 보기 →</a></p>\n')

    faq = "\n".join('    <details><summary>%s</summary><p>%s</p></details>' % (esc(q), esc(a)) for q, a in topic["faq"])

    src = ""
    if topic.get("sources"):
        src = '  <p class="disc" style="margin-bottom:0">법령·제도 근거: %s</p>\n' % esc(topic["sources"])

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- 이 파일은 scripts/build_topics.py가 생성합니다. 내용 수정은 scripts/topics_config.py에서 하세요. -->
<title>{esc(topic['title'])}</title>
<meta name="description" content="{esc(topic['description'])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(topic['title'].split(' | ')[0])}">
<meta property="og:description" content="{esc(topic['description'])}">
<meta property="og:url" content="{url}">
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
{json.dumps(page_ld, ensure_ascii=False, indent=1)}
</script>
<script type="application/ld+json">
{json.dumps(faq_ld, ensure_ascii=False, indent=1)}
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

  <div class="eyebrow"><a href="/#fields">진료분야</a> › {esc(topic['name'])}</div>
  <h1>{topic['h1']}</h1>
  <p class="byline">글·감수 <strong><a href="/about/" style="color:inherit">이은혜</a></strong> 한의사 (지인한의원 대표원장)</p>

  <div class="answer">{topic['answer']}</div>
{er}{topic.get('extra', '')}{sym}{how}{colsec}
  <h2>자주 묻는 질문</h2>
  <div class="faq">
{faq}
  </div>

  <div class="cta-box">
    <h3>증상이 반복된다면, 원인부터 확인하세요</h3>
    <p>부천시 원미구 소향로 135, 3층 (부천시청역 2번 출구 도보 3분) · 평일 매일 저녁 8:30까지 · 토 09:00–15:00</p>
    <div class="ctas">
      <a class="c-call" href="tel:032-323-2933">📞 032-323-2933</a>
      <a class="c-kakao" href="https://pf.kakao.com/_xmxhmpxj/chat" target="_blank" rel="noopener">💬 카카오톡</a>
      <a class="c-naver" href="https://booking.naver.com/booking/13/bizes/185044" target="_blank" rel="noopener">네이버 예약</a>
    </div>
  </div>

  <h2 style="font-size:17px">다른 진료분야</h2>
  <div class="others">
      {nav_html(slug)}
  </div>

  <p class="disc" style="margin-bottom:0">이 안내는 이은혜 대표원장이 <a href="https://blog.naver.com/jeeinomd2020" target="_blank" rel="noopener" style="font-weight:700">공식 블로그</a>에 직접 쓴 칼럼을 바탕으로 정리했습니다.</p>
{src}  <p class="disc" style="border-top:none;padding-top:8px">본 안내는 일반적인 건강 정보이며 의학적 진단을 대신하지 않습니다. 치료 효과와 기간은 개인에 따라 다를 수 있습니다.</p>

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
""", len(mine), lastmod


def main():
    posts = load_posts()
    summary = {}
    for t in TOPICS:
        page, n, lastmod = build(t, posts)
        d = os.path.join(ROOT, t["slug"])
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, "index.html")
        old = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
        if old != page:
            with open(path, "w", encoding="utf-8") as f:
                f.write(page)
        summary[t["slug"]] = {"name": t["name"], "count": n, "lastmod": lastmod}
        print("%-14s %2d편" % (t["slug"], n))
    with open(os.path.join(ROOT, "data", "topics.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
