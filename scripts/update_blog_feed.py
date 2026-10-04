#!/usr/bin/env python3
"""네이버 블로그 RSS 동기화:
1) 메인(index.html) 카드 — 최신 3개
2) data/blog-posts.json — 수집된 글 누적 (중복 없이)
3) blog/index.html — 전체 아카이브 목록 자동 생성
실패하면 아무것도 바꾸지 않고 정상 종료 (기존 상태 유지)."""
import html
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RSS_URL = "https://rss.blog.naver.com/jeeinomd2020.xml"
INDEX = ROOT / "index.html"
DATA = ROOT / "data" / "blog-posts.json"
ARCHIVE = ROOT / "blog" / "index.html"
START, END = "<!-- BLOG-FEED:START -->", "<!-- BLOG-FEED:END -->"
A_START, A_END = "<!-- ARCHIVE:START -->", "<!-- ARCHIVE:END -->"
MAX_CARDS = 3
EXCERPT_LEN = 85


def clean(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def post_id(link: str) -> str:
    m = re.search(r"/jeeinomd2020/(\d+)", link)
    return m.group(1) if m else link


def fetch_posts():
    req = urllib.request.Request(RSS_URL, headers={"User-Agent": "Mozilla/5.0 (jeeinclinic.com feed sync)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        root = ET.fromstring(r.read())
    posts = []
    for item in root.iter("item"):
        title = clean(item.findtext("title", ""))
        link = (item.findtext("link") or "").strip()
        desc = clean(item.findtext("description", ""))
        pub = item.findtext("pubDate", "")
        try:
            date = datetime.strptime(pub[:16].strip(), "%a, %d %b %Y").strftime("%Y-%m-%d")
        except ValueError:
            date = pub[:10]
        if title and link:
            posts.append({"id": post_id(link), "title": title, "link": link.split("?")[0], "desc": desc[:200], "date": date})
    return posts


def merge(new_posts):
    DATA.parent.mkdir(exist_ok=True)
    stored = {}
    if DATA.exists():
        for p in json.loads(DATA.read_text(encoding="utf-8")):
            stored[p["id"]] = p
    added = 0
    for p in new_posts:
        if p["id"] not in stored:
            added += 1
        stored[p["id"]] = p  # 최신 정보로 갱신
    merged = sorted(stored.values(), key=lambda p: (p["date"], p["id"]), reverse=True)
    DATA.write_text(json.dumps(merged, ensure_ascii=False, indent=1), encoding="utf-8")
    return merged, added


def excerpt(p):
    d = p["desc"][:EXCERPT_LEN]
    return html.escape(d + ("…" if len(p["desc"]) > EXCERPT_LEN else ""))


def render_cards(posts):
    cards = []
    for p in posts[:MAX_CARDS]:
        cards.append(
            f'''    <a class="bcard" href="{html.escape(p["link"])}" target="_blank" rel="noopener">
      <span class="bdate">BLOG · {p["date"]}</span>
      <h3>{html.escape(p["title"])}</h3>
      <p>{excerpt(p)}</p>
      <span class="bgo">네이버에서 읽기 ↗</span>
    </a>''')
    return "\n".join(cards)


def render_archive(posts):
    rows, cur_month = [], None
    for p in posts:
        month = p["date"][:7]
        if month != cur_month:
            cur_month = month
            y, m = month.split("-") if "-" in month else (month, "")
            rows.append(f'    <h2 class="month">{y}년 {int(m)}월</h2>' if m else f'    <h2 class="month">{month}</h2>')
        s = html.escape((p["title"] + " " + p["desc"]).lower(), quote=True)
        rows.append(
            f'''    <a class="row" data-s="{s}" href="{html.escape(p["link"])}" target="_blank" rel="noopener">
      <span class="rdate">{p["date"]}</span>
      <span class="rtitle">{html.escape(p["title"])}</span>
    </a>''')
    return "\n".join(rows)


def splice(path, start, end, body):
    src = path.read_text(encoding="utf-8")
    if start not in src or end not in src:
        print(f"markers missing in {path}")
        return False
    before, rest = src.split(start, 1)
    _, after = rest.split(end, 1)
    new = before + start + "\n" + body + "\n" + end + after
    if new != src:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def main():
    try:
        fetched = fetch_posts()
    except Exception as e:
        print(f"feed fetch failed, keeping existing state: {e}")
        return 0
    if not fetched:
        print("no posts in feed")
        return 0
    posts, added = merge(fetched)
    c1 = splice(INDEX, START, END, render_cards(posts))
    c2 = splice(ARCHIVE, A_START, A_END, render_archive(posts))
    # 아카이브 글 수 표기 갱신
    src = ARCHIVE.read_text(encoding="utf-8")
    src2 = re.sub(r'(<span id="count">)\d*(</span>)', rf'\g<1>{len(posts)}\g<2>', src)
    if src2 != src:
        ARCHIVE.write_text(src2, encoding="utf-8")
        c2 = True
    print(f"posts total={len(posts)} new={added} index_changed={c1} archive_changed={c2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
