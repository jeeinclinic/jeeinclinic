# -*- coding: utf-8 -*-
"""통증 > 질환 부위 페이지(/pain/<부위>/)와 병명 '준비 중' 페이지(/pain/<부위>/<병명>/)를 만든다.
- 부위 페이지는 병명 목록을 보여 주고, 이 스크립트가 만든 파일(PAIN-PART 표시)만 다시 쓴다.
- 병명 페이지는 build_menu_pages 의 준비 중 템플릿을 쓴다(내용을 채우면 MENU-PLACEHOLDER 줄을 지운다).
"""
import html, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from pain_config import parts  # noqa: E402
import build_menu_pages as bmp  # noqa: E402

PART_MARK = "<!-- PAIN-PART -->"


def part_page(name, slug, items):
    url = "/pain/%s/" % slug
    chips = "".join('<a href="%s%s/">%s</a>' % (url, s, html.escape(n)) for n, s in items)
    sib = '  <h2>증상별 안내</h2>\n  <div class="sib">%s</div>' % chips
    out = bmp.TPL % dict(mark=PART_MARK, label=html.escape(name), url=url, group="통증 · 질환", sib=sib)
    out = re.sub(r'<div class="soon">.*?</div>',
                 '<div class="soon"><strong>%s 관련 증상을 모았습니다.</strong><br>아래에서 해당하는 증상을 선택해 주세요. '
                 '항목별 안내는 순차적으로 준비하고 있으며, 그 전에 궁금하신 점은 전화나 카카오톡으로 문의해 주세요.</div>'
                 % html.escape(name), out, count=1, flags=re.S)
    return out


def main():
    made = 0
    for name, slug, items in parts():
        path = os.path.join(ROOT, "pain", slug, "index.html")
        cur = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if cur is not None and PART_MARK not in cur and bmp.MARK not in cur:
            pass  # 직접 고친 페이지는 건드리지 않는다
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, "w", encoding="utf-8").write(part_page(name, slug, items))
            made += 1
        for n, s in items:
            made += bmp.write(name, n, "/pain/%s/%s/" % (slug, s), items_urls(slug, items))
    print("pain pages: %d" % made)


def items_urls(slug, items):
    return [(n, "/pain/%s/%s/" % (slug, s)) for n, s in items]


if __name__ == "__main__":
    main()
