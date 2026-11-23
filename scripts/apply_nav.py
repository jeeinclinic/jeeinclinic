# -*- coding: utf-8 -*-
"""전 페이지 공통 상단 메뉴(모바일 포함) 적용기. 여러 번 실행해도 결과가 같습니다(멱등).

- 모든 *.html 의 </header> 앞에 메뉴 줄(<nav class="sitenav">)을 넣고, </style> 앞에 CSS를 넣는다.
- 메뉴 항목을 바꾸려면 아래 ITEMS 만 수정하고 이 스크립트를 실행하면 사이트 전체에 반영된다.
- build_topics.py / build_columns.py / build_faq.py 가 페이지를 새로 만든 뒤에도 마지막에 실행해야 한다(워크플로에 포함).
"""
import html, os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from menu_config import MENU, UTIL, kid  # noqa: E402

N_START, N_END = "<!-- SITENAV:START -->", "<!-- SITENAV:END -->"
C_START, C_END = "/* SITENAV:START */", "/* SITENAV:END */"

CSS = """%s
  .gnb{position:relative;border-top:1px solid rgba(34,39,31,.08);font-family:'Noto Sans KR',-apple-system,'Malgun Gothic',sans-serif;line-height:1.3}
  .gnb *{box-sizing:border-box}
  .gnb a{text-decoration:none;color:#22271F}
  .gnb ul{list-style:none;margin:0;padding:0}
  .gnb-in{max-width:1240px;margin:0 auto;padding:0 14px;display:flex;align-items:center;justify-content:space-between;gap:4px}
  .gnb-burger{display:none;font:inherit;font-size:14px;font-weight:700;color:#F3F0E4;background:#2B4232;border:0;border-radius:9px;padding:9px 14px;cursor:pointer;margin:8px 0}
  .gnb-list{display:flex;flex-wrap:wrap;justify-content:center;flex:1}
  .gnb-item{position:relative}
  .gnb-top{display:block;font-size:14px;font-weight:700;padding:13px 10px;color:#22271F;white-space:nowrap}
  .gnb-item:hover>.gnb-top,.gnb-item:focus-within>.gnb-top,.gnb-item.cur>.gnb-top{color:#2B4232;box-shadow:inset 0 -2px 0 #B8792C}
  .gnb-tg{display:none}
  .gnb-sub{display:none;position:absolute;left:50%%;top:100%%;transform:translateX(-50%%);min-width:168px;background:#FFFDF4;border:1px solid rgba(34,39,31,.13);border-radius:12px;box-shadow:0 14px 34px rgba(23,35,26,.16);padding:8px;z-index:70}
  .gnb-item:hover>.gnb-sub,.gnb-item:focus-within>.gnb-sub{display:block}
  .gnb-item:nth-last-child(-n+3)>.gnb-sub{left:auto;right:0;transform:none}
  .gnb-has2{position:relative}
  .gnb-has2>a::after{content:"›";float:right;margin-left:14px;color:#B8792C;font-weight:700}
  .gnb-sub2{display:none;position:absolute;left:100%%;top:-9px;min-width:140px;background:#FFFDF4;border:1px solid rgba(34,39,31,.13);border-radius:12px;box-shadow:0 14px 34px rgba(23,35,26,.16);padding:8px}
  .gnb-sub2.gnb-wide{columns:2;column-gap:6px;min-width:290px}
  .gnb-sub2.gnb-wide li{break-inside:avoid}
  .gnb-has3{position:relative}
  .gnb-has3>a{white-space:nowrap}
  .gnb-has3>a::after{content:"›";float:right;margin-left:14px;color:#B8792C;font-weight:700}
  .gnb-sub3{display:none;position:absolute;left:100%%;top:-9px;min-width:190px;max-height:70vh;overflow-y:auto;background:#FFFDF4;border:1px solid rgba(34,39,31,.13);border-radius:12px;box-shadow:0 14px 34px rgba(23,35,26,.16);padding:8px}
  .gnb-has3:hover>.gnb-sub3,.gnb-has3:focus-within>.gnb-sub3{display:block}
  .gnb-item:nth-last-child(-n+3) .gnb-sub3{left:auto;right:100%%}
  .gnb-has2:hover>.gnb-sub2,.gnb-has2:focus-within>.gnb-sub2{display:block}
  .gnb-item:nth-last-child(-n+3) .gnb-sub2{left:auto;right:100%%}
  .gnb-sub a{display:block;font-size:13.5px;font-weight:500;color:#22271F;padding:9px 12px;border-radius:8px;white-space:nowrap}
  .gnb-sub a:hover,.gnb-sub a:focus{background:#F0E1C6;color:#17231A}
  .gnb-util{display:flex;gap:2px;flex:none}
  .gnb-util a{font-size:13px;font-weight:700;color:#5D6455;padding:13px 9px;white-space:nowrap}
  .gnb-util a:hover,.gnb-util a[aria-current]{color:#2B4232}
  .gnb-tg2,.gnb-close{display:none}
  @media (max-width:1179px){
    .gnb-in{flex-wrap:wrap;padding:0 14px}
    .gnb-burger{display:inline-block}
    .gnb-util{margin-left:auto}
    .gnb-list{display:none}
    html.gnb-open{overflow:hidden}
    html.gnb-open header{backdrop-filter:none!important;-webkit-backdrop-filter:none!important}
    .gnb.open .gnb-list{display:flex;flex-direction:column;flex-wrap:nowrap;justify-content:flex-start;position:fixed;left:0;right:0;top:0;bottom:0;z-index:100;background:#FFFDF4;margin:0;padding:68px 16px 110px;overflow-y:auto;-webkit-overflow-scrolling:touch;overscroll-behavior:contain}
    .gnb.open .gnb-list::before{content:"전체 메뉴";position:fixed;left:0;right:0;top:0;height:56px;line-height:56px;padding:0 18px;font-weight:900;font-size:17px;color:#17231A;background:#FFFDF4;border-bottom:1px solid rgba(34,39,31,.1);z-index:2}
    .gnb.open .gnb-close{display:block;position:fixed;top:8px;right:10px;z-index:101;width:44px;height:40px;border:0;border-radius:10px;background:#2B4232;color:#F3F0E4;font-size:20px;line-height:1;cursor:pointer}
    .gnb-item{display:flex;flex-wrap:wrap;align-items:stretch;border-bottom:1px solid rgba(34,39,31,.08)}
    .gnb-top{flex:1;font-size:16px;font-weight:700;padding:16px 4px;box-shadow:none!important}
    .gnb-tg,.gnb-tg2{display:block;flex:none;width:52px;border:0;background:none;cursor:pointer;position:relative}
    .gnb-tg::after,.gnb-tg2::after{content:"";position:absolute;left:50%%;top:50%%;width:8px;height:8px;margin:-6px 0 0 -4px;border-right:2px solid #5D6455;border-bottom:2px solid #5D6455;transform:rotate(45deg);transition:transform .15s}
    .gnb-item.open>.gnb-tg::after,.gnb-has2.open>.gnb-tg2::after,.gnb-has3.open>.gnb-tg2::after{transform:rotate(-135deg);margin-top:-2px}
    .gnb-sub,.gnb-item:hover>.gnb-sub,.gnb-item:focus-within>.gnb-sub{display:none;position:static;transform:none!important;min-width:0;width:100%%;border:0;box-shadow:none;background:#F3F0E4;border-radius:12px;padding:4px 8px;margin:0 0 12px}
    .gnb-item.open>.gnb-sub{display:block}
    .gnb-sub a{padding:13px 10px;font-size:15px}
    .gnb-has2,.gnb-has3{display:flex;flex-wrap:wrap;align-items:center}
    .gnb-has2>a,.gnb-has3>a{flex:1;white-space:normal}
    .gnb-has2>a::after,.gnb-has3>a::after{display:none}
    .gnb-sub2,.gnb-sub3,.gnb-has2:hover>.gnb-sub2,.gnb-has2:focus-within>.gnb-sub2,.gnb-has3:hover>.gnb-sub3,.gnb-has3:focus-within>.gnb-sub3,.gnb-item:nth-last-child(-n+3) .gnb-sub2,.gnb-item:nth-last-child(-n+3) .gnb-sub3{display:none;position:static;flex:0 0 100%%;min-width:0;max-height:none;overflow:visible;border:0;box-shadow:none;background:#FFFDF4;border-radius:10px;padding:2px 6px 6px;margin:0 0 6px;left:auto;right:auto;columns:auto}
    .gnb-has2.open>.gnb-sub2,.gnb-has3.open>.gnb-sub3{display:block}
    .gnb-has2.open>.gnb-sub2.gnb-wide{display:grid;grid-template-columns:1fr 1fr;column-gap:4px}
    .gnb-sub2 a,.gnb-sub3 a{font-size:14px;color:#5D6455;padding:12px 8px}
    .gnb-sub3 a{font-size:13.5px}
  }
%s""" % (C_START, C_END)

JS = """<script>(function(){var n=document.querySelector('.gnb');if(!n||n.getAttribute('data-js'))return;n.setAttribute('data-js','1');
var b=n.querySelector('.gnb-burger'),h=document.documentElement;
function setOpen(o){n.classList.toggle('open',o);b.setAttribute('aria-expanded',o);h.classList.toggle('gnb-open',o&&window.innerWidth<1180)}
b.addEventListener('click',function(){setOpen(!n.classList.contains('open'))});
var c=n.querySelector('.gnb-close');if(c)c.addEventListener('click',function(){setOpen(false)});
n.querySelectorAll('.gnb-tg,.gnb-tg2').forEach(function(t){t.addEventListener('click',function(){var li=t.parentNode,o=li.classList.toggle('open');t.setAttribute('aria-expanded',o)})});
document.addEventListener('keydown',function(e){if(e.key==='Escape')setOpen(false)});
document.addEventListener('click',function(e){if(!n.contains(e.target)&&n.classList.contains('open'))setOpen(false)});
n.querySelectorAll('a[href^="/#"]').forEach(function(a){a.addEventListener('click',function(){setOpen(false)})});
window.addEventListener('resize',function(){if(window.innerWidth>=1180)h.classList.remove('gnb-open');else if(n.classList.contains('open'))h.classList.add('gnb-open')});
})();</script>"""


def page_url(rel):
    rel = rel.replace(os.sep, "/")
    return "/" if rel == "index.html" else "/" + (rel[:-len("index.html")] if rel.endswith("/index.html") else rel)


def nav_markup(url):
    path = url.split("#")[0]
    items = []
    for group, kids in MENU:
        kids = [kid(k) for k in kids]
        cur = " cur" if any(u == path or any(x[1] == path for x in s) for _, u, s in kids if not u.startswith("http")) else ""
        first = kids[0][1]
        ext = ' target="_blank" rel="noopener"'
        def li(l, u, s):
            a = '<a href="%s"%s>%s</a>' % (u, ext if u.startswith("http") else "", html.escape(l))
            if s:
                nested = any(len(x) > 2 and x[2] for x in s)
                def li2(x):
                    l2, u2 = x[0], x[1]
                    s3 = x[2] if len(x) > 2 else []
                    if s3:
                        return ('<li class="gnb-has3"><a href="%s">%s</a><button class="gnb-tg2" type="button" aria-expanded="false" aria-label="%s 하위 메뉴"></button><ul class="gnb-sub3">%s</ul></li>'
                                % (u2, html.escape(l2), html.escape(l2), "".join('<li><a href="%s">%s</a></li>' % (u3, html.escape(l3)) for l3, u3 in s3)))
                    return '<li><a href="%s">%s</a></li>' % (u2, html.escape(l2))
                return ('<li class="gnb-has2">%s<button class="gnb-tg2" type="button" aria-expanded="false" aria-label="%s 하위 메뉴"></button><ul class="gnb-sub2%s">%s</ul></li>'
                        % (a, html.escape(l), " gnb-wide" if (len(s) > 10 and not nested) else "", "".join(li2(x) for x in s)))
            return "<li>%s</li>" % a
        subs = "".join(li(l, u, s) for l, u, s in kids) if (len(kids) > 1 or kids[0][0] != group) else ""
        if subs:
            items.append('<li class="gnb-item%s"><a class="gnb-top" href="%s">%s</a>'
                         '<button class="gnb-tg" type="button" aria-expanded="false" aria-label="%s 하위 메뉴"></button>'
                         '<ul class="gnb-sub">%s</ul></li>' % (cur, first, html.escape(group), html.escape(group), subs))
        else:
            items.append('<li class="gnb-item%s"><a class="gnb-top" href="%s">%s</a></li>' % (cur, first, html.escape(group)))
    util = "".join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if path.startswith(h) else "", html.escape(n)) for n, h in UTIL)
    return ('%s\n<nav class="gnb" aria-label="주요 메뉴"><div class="gnb-in">'
            '<button class="gnb-burger" type="button" aria-expanded="false">☰ 전체 메뉴</button>'
            '<button class="gnb-close" type="button" aria-label="메뉴 닫기">✕</button><ul class="gnb-list">%s</ul><div class="gnb-util">%s</div></div></nav>\n%s\n%s\n' % (
                N_START, "".join(items), util, JS, N_END))


def files():
    out = subprocess.run(["git", "ls-files", "*.html"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    extra = [os.path.relpath(os.path.join(d, f), ROOT) for d, _, fs in os.walk(ROOT) if ".git" not in d for f in fs if f.endswith(".html")]
    return sorted(r for r in (set(out) | set(extra)) if os.path.exists(os.path.join(ROOT, r)))


def main():
    changed = 0
    for rel in files():
        path = os.path.join(ROOT, rel)
        src = open(path, encoding="utf-8").read()
        if "</header>" not in src or "</style>" not in src:
            continue
        s = re.sub(re.escape(N_START) + r".*?" + re.escape(N_END) + r"\n?", "", src, flags=re.S)
        s = re.sub(r"\n?" + re.escape(C_START) + r".*?" + re.escape(C_END) + r"\n?", "\n", s, flags=re.S)
        url = page_url(rel)
        s = s.replace("</style>", CSS + "</style>", 1)
        s = s.replace("</header>", nav_markup(url) + "</header>", 1)
        if s != src:
            open(path, "w", encoding="utf-8").write(s)
            changed += 1
    print("sitenav applied: %d files changed" % changed)


if __name__ == "__main__":
    main()
