# bansou.admoat.net（使っていない旧サイト）の全ページを、admoat.net の同じ内容のページへ飛ばす「転送用サイト」を作る。
# 使い方：python3 作る.py  → site/ の中に転送ページができる（GitHub Pages で公開する）
import os, html, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "site")
MAIN = "https://admoat.net/"
HP = "/Users/ikedanoborusei/Documents/AdMoat_HP_form"  # admoat.net の作業用コピー（転送先が本当にあるか確かめる）

# 記事以外のページ
FIXED = {"": "accompaniment-support.dc.html", "service": "accompaniment-support.dc.html",
         "cases": "works.dc.html", "about": "company.dc.html", "contact": "contact.dc.html",
         "privacy": "privacy.dc.html", "blog": "blog.dc.html"}
# admoat.net に同じ名前の記事がないもの → いちばん近い記事へ
NEAR = {"meta-ads-cpa-calculation": "column-cpa", "meta-ads-breakeven-cpa": "column-cpa", "meta-ads-cpa": "column-cpa",
        "meta-ads-roas-store": "column-roas", "meta-ads-ltv-calculation": "column-ltv", "ltv-meta-ads-budget": "column-ltv",
        "meta-ads-attribution-basics": "column-attribution", "meta-ads-creative-fatigue": "column-meta-ads-creative-improvement"}

def page(target, title="AdMoat"):
    u = html.escape(MAIN + target)
    return f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<title>{html.escape(title)}</title>
<link rel="canonical" href="{u}">
<meta http-equiv="refresh" content="0; url={u}">
<meta name="viewport" content="width=device-width,initial-scale=1">
<script>location.replace("{u}"+location.hash);</script>
</head><body style="font-family:sans-serif;text-align:center;padding:40px 16px;">
<p>このページは移転しました。</p><p><a href="{u}">新しいページを開く</a></p>
</body></html>
'''

def write(path, target):
    assert os.path.exists(os.path.join(HP, target.split("#")[0] or "index.html")), "転送先がありません: " + target
    d = os.path.join(OUT, path)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(target, "移転しました｜AdMoat"))

shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
n = 0
for line in open(os.path.join(HERE, "元のページ一覧.txt"), encoding="utf-8"):
    p = line.strip().replace("https://bansou.admoat.net", "").strip("/")
    if not line.strip(): continue
    if p in FIXED: t = FIXED[p]
    elif p.startswith("blog/"):
        s = p[5:]; t = (NEAR.get(s) or "column-" + s) + ".dc.html"
    else: raise SystemExit("知らないページ: " + p)
    write(p, t); n += 1
# 一覧にないページ → トップへ
open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(page("accompaniment-support.dc.html", "移転しました｜AdMoat"))
open(os.path.join(OUT, "CNAME"), "w").write("bansou.admoat.net\n")
open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nAllow: /\n")
open(os.path.join(OUT, ".nojekyll"), "w").write("")
print("転送ページ", n, "件を作りました")
