# -*- coding: utf-8 -*-
"""menu_config.py 의 하위 메뉴 중 아직 페이지가 없는 것을 '준비 중' 안내 페이지로 만든다.
- 이미 있는 페이지는 건드리지 않는다. (MENU-PLACEHOLDER 표시가 있는 파일만 다시 만든다)
- 검색 제외(noindex), sitemap 제외.
"""
import html, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from menu_config import MENU  # noqa: E402

MARK = "<!-- MENU-PLACEHOLDER -->"

TPL = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
%(mark)s
<title>%(label)s | 부천 지인한의원</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://jeeinclinic.com%(url)s">
<link rel="icon" type="image/png" href="/images/favicon-512.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@500;700;900&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  :root{--paper:#F3F0E4;--paper-deep:#EAE6D4;--ink:#22271F;--ink-soft:#5D6455;--pine:#2B4232;--pine-deep:#17231A;--ochre:#B8792C;--ochre-soft:#F0E1C6;--seal:#B23A2E;--line:rgba(34,39,31,.13)}
  *{box-sizing:border-box}
  body{margin:0;background:var(--paper);color:var(--ink);font-family:'Noto Sans KR',-apple-system,'Malgun Gothic',sans-serif;line-height:1.85}
  h1,h2,h3{font-family:'Noto Serif KR',serif;word-break:keep-all}
  a{color:inherit}
  .wrap{max-width:720px;margin:0 auto;padding:0 22px}
  header{position:sticky;top:0;z-index:50;background:rgba(243,240,228,.97);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
  .topbar{max-width:720px;margin:0 auto;padding:14px 22px;display:flex;align-items:center;justify-content:space-between}
  .brand{display:flex;align-items:center;gap:10px;text-decoration:none}
  .brand .bseal{width:34px;height:34px;border-radius:7px;background:#B23A2E;color:#FBF6E8;display:flex;align-items:center;justify-content:center;font-family:'Noto Serif KR',serif;font-weight:900;font-size:13px}
  .brand .btxt{display:flex;flex-direction:column;line-height:1.25}
  .brand .b1{font-family:'Noto Serif KR',serif;font-weight:900;font-size:16.5px;color:var(--pine-deep)}
  .brand .b2{font-weight:500;font-size:9.5px;color:var(--ink-soft);letter-spacing:1.8px}
  .home-btn,.top-call{white-space:nowrap;font-size:13px;font-weight:700;text-decoration:none;padding:8px 14px;border-radius:9px}
  .home-btn{color:var(--pine);border:1.5px solid var(--pine)}
  .top-call{background:var(--pine);color:#F3F0E4}
  @media (max-width:420px){.brand .b2{display:none}.home-btn,.top-call{padding:7px 10px;font-size:12.5px}}
  article{padding:56px 0 60px}
  .eyebrow{font-size:12px;font-weight:700;letter-spacing:3px;color:var(--ochre);margin-bottom:14px}
  h1{font-size:clamp(26px,5vw,36px);font-weight:900;line-height:1.4;color:var(--pine-deep);margin:0 0 22px}
  .soon{background:#FFFDF4;border-left:4px solid var(--ochre);border-radius:0 13px 13px 0;padding:22px 24px;font-size:15.5px;margin-bottom:28px}
  .ctas{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:34px}
  .ctas a{flex:1;min-width:130px;text-align:center;padding:13px 10px;border-radius:11px;font-size:13.5px;font-weight:700;text-decoration:none}
  .c-call{background:var(--pine);color:#F3F0E4}.c-kakao{background:#FEE500;color:#3C1E1E}.c-naver{background:#03C75A;color:#fff}
  h2{font-size:17px;font-weight:900;color:var(--pine-deep);margin:0 0 10px}
  .sib{display:flex;flex-wrap:wrap;gap:8px}
  .sib a{font-size:14px;font-weight:700;text-decoration:none;color:var(--pine);border:1.5px solid var(--line);background:#FFFDF4;padding:8px 14px;border-radius:999px}
  .sib a[aria-current]{background:var(--pine);color:#F3F0E4;border-color:var(--pine)}
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
  <div class="eyebrow">%(group)s</div>
  <h1>%(label)s</h1>
  <div class="soon"><strong>안내 페이지를 준비하고 있습니다.</strong><br>자세한 내용은 곧 정리해 드리겠습니다. 그 전에 궁금하신 점은 전화나 카카오톡으로 편하게 문의해 주세요.</div>
  <div class="ctas">
    <a class="c-call" href="tel:032-323-2933">📞 032-323-2933</a>
    <a class="c-kakao" href="https://pf.kakao.com/_xmxhmpxj/chat" target="_blank" rel="noopener">💬 카카오톡</a>
    <a class="c-naver" href="https://booking.naver.com/booking/13/bizes/185044" target="_blank" rel="noopener">네이버 예약</a>
  </div>
%(sib)s
</article>
</div>
</body>
</html>
"""


def main():
    made = 0
    for group, kids in MENU:
        for label, url in kids:
            if not url.startswith("/") or "#" in url or url.count("/") < 2:
                continue
            path = os.path.join(ROOT, url.strip("/"), "index.html")
            if os.path.exists(path):
                if MARK not in open(path, encoding="utf-8").read():
                    continue  # 실제 내용 페이지
            elif url in ("/mission/", "/about/"):
                continue
            sibs = [(l, u) for l, u in kids if len(kids) > 1]
            sib = ""
            if len(kids) > 1:
                sib = '  <h2>%s의 다른 안내</h2>\n  <div class="sib">%s</div>' % (
                    html.escape(group), "".join(
                        '<a href="%s"%s>%s</a>' % (u, ' aria-current="page"' if u == url else "", html.escape(l))
                        for l, u in kids if not u.startswith("http")))
            out = TPL % dict(mark=MARK, label=html.escape(label), url=url, group=html.escape(group), sib=sib)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, "w", encoding="utf-8").write(out)
            made += 1
    print("menu placeholder pages: %d" % made)


if __name__ == "__main__":
    main()
