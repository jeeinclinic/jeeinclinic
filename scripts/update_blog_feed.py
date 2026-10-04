#!/usr/bin/env python3
"""네이버 블로그 RSS에서 최신 글 3개를 가져와 index.html의 블로그 카드를 갱신.
실패하면 아무것도 바꾸지 않고 정상 종료 (기존 카드 유지)."""
import html
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

RSS_URL = "https://rss.blog.naver.com/jeeinomd2020.xml"
INDEX = Path(__file__).resolve().parent.parent / "index.html"
START, END = "<!-- BLOG-FEED:START -->", "<!-- BLOG-FEED:END -->"
MAX_POSTS = 3
EXCERPT_LEN = 85


def clean(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


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
            posts.append({"title": title, "link": link, "desc": desc, "date": date})
        if len(posts) >= MAX_POSTS:
            break
    return posts


def render(posts):
    cards = []
    for p in posts:
        desc = p["desc"][:EXCERPT_LEN] + ("…" if len(p["desc"]) > EXCERPT_LEN else "")
        cards.append(
            f'''    <a class="bcard" href="{html.escape(p["link"])}" target="_blank" rel="noopener">
      <span class="bdate">BLOG · {p["date"]}</span>
      <h3>{html.escape(p["title"])}</h3>
      <p>{html.escape(desc)}</p>
      <span class="bgo">네이버에서 읽기 ↗</span>
    </a>''')
    return "\n".join(cards)


def main():
    try:
        posts = fetch_posts()
    except Exception as e:  # 네트워크·파싱 실패 시 기존 카드 유지
        print(f"feed fetch failed, keeping existing cards: {e}")
        return 0
    if not posts:
        print("no posts in feed, keeping existing cards")
        return 0
    src = INDEX.read_text(encoding="utf-8")
    if START not in src or END not in src:
        print("markers not found in index.html")
        return 1
    before, rest = src.split(START, 1)
    _, after = rest.split(END, 1)
    new = before + START + "\n" + render(posts) + "\n" + END + after
    if new == src:
        print("no change")
        return 0
    INDEX.write_text(new, encoding="utf-8")
    print(f"updated {len(posts)} cards (latest: {posts[0]['date']} {posts[0]['title'][:30]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
