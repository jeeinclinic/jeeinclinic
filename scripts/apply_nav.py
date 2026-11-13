# -*- coding: utf-8 -*-
"""전 페이지 공통 상단 메뉴(모바일 포함) 적용기. 여러 번 실행해도 결과가 같습니다(멱등).

- 모든 *.html 의 </header> 앞에 메뉴 줄(<nav class="sitenav">)을 넣고, </style> 앞에 CSS를 넣는다.
- 메뉴 항목을 바꾸려면 아래 ITEMS 만 수정하고 이 스크립트를 실행하면 사이트 전체에 반영된다.
- build_topics.py / build_columns.py / build_faq.py 가 페이지를 새로 만든 뒤에도 마지막에 실행해야 한다(워크플로에 포함).
"""
import html, os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ITEMS = [  # (주소, 이름)
    ("/hours/", "야간진료 안내"),
    ("/columns/", "칼럼"),
    ("/notes/", "생활한방노트"),
    ("/about/", "원장 소개"),
]
N_START, N_END = "<!-- SITENAV:START -->", "<!-- SITENAV:END -->"
C_START, C_END = "/* SITENAV:START */", "/* SITENAV:END */"

CSS = """%s
  .sitenav{border-top:1px solid rgba(34,39,31,.08)}
  .sitenav-in{margin:0 auto;padding:0 14px;display:flex;gap:2px;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;white-space:nowrap}
  .sitenav-in::-webkit-scrollbar{display:none}
  .sitenav a{flex:none;font-family:'Noto Sans KR',-apple-system,'Malgun Gothic',sans-serif;font-size:13px;font-weight:700;line-height:1.2;text-decoration:none;color:#5D6455;padding:11px 10px}
  .sitenav a:hover{color:#22271F}
  .sitenav a[aria-current="page"]{color:#2B4232;box-shadow:inset 0 -2px 0 #B8792C}
  @media (min-width:761px){.sitenav.mobile-only{display:none}}
%s""" % (C_START, C_END)


def page_url(rel):
    rel = rel.replace(os.sep, "/")
    return "/" if rel == "index.html" else "/" + (rel[:-len("index.html")] if rel.endswith("/index.html") else rel)


def nav_markup(url, width, mobile_only):
    links = []
    for href, name in ITEMS:
        cur = ' aria-current="page"' if (url == href or url.startswith(href)) else ""
        links.append('<a href="%s"%s>%s</a>' % (href, cur, html.escape(name)))
    cls = "sitenav mobile-only" if mobile_only else "sitenav"
    return '%s\n<nav class="%s" aria-label="주요 메뉴"><div class="sitenav-in" style="max-width:%dpx">%s</div></nav>\n%s\n' % (
        N_START, cls, width, "".join(links), N_END)


def files():
    out = subprocess.run(["git", "ls-files", "*.html"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    extra = [os.path.relpath(os.path.join(d, f), ROOT) for d, _, fs in os.walk(ROOT) if ".git" not in d for f in fs if f.endswith(".html")]
    return sorted(set(out) | set(extra))


def main():
    changed = 0
    for rel in files():
        path = os.path.join(ROOT, rel)
        src = open(path, encoding="utf-8").read()
        if "</header>" not in src or "</style>" not in src:
            continue
        s = re.sub(re.escape(N_START) + r".*?" + re.escape(N_END) + r"\n?", "", src, flags=re.S)
        s = re.sub(r"\n?" + re.escape(C_START) + r".*?" + re.escape(C_END) + r"\n?", "\n", s, flags=re.S)
        m = re.search(r"\.topbar\{max-width:(\d+)px", s)
        width = int(m.group(1)) if m else 720
        url = page_url(rel)
        s = s.replace("</style>", CSS + "</style>", 1)
        s = s.replace("</header>", nav_markup(url, width, rel == "index.html") + "</header>", 1)
        if s != src:
            open(path, "w", encoding="utf-8").write(s)
            changed += 1
    print("sitenav applied: %d files changed" % changed)


if __name__ == "__main__":
    main()
