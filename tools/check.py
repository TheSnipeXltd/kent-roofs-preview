"""Site checker. python tools/check.py .            (errors that break the site)
                python tools/check.py . --launch   (also fails on unconfirmed placeholders)
Checks: broken links/anchors/images, alt text, titles, descriptions, one h1, image sizes,
external requests, unused images, placeholders."""
import sys, re, os, glob
from html.parser import HTMLParser
root = sys.argv[1].rstrip("/\\")
launch = "--launch" in sys.argv

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.ids=set(); s.links=[]; s.imgs=[]; s.res=[]; s.h1=0; s.title=""; s.desc=""; s.in_title=False; s.ph=[]; s._ph=False; s.buf=""
    def handle_starttag(s, t, a):
        a = dict(a)
        if "id" in a: s.ids.add(a["id"])
        if t == "a" and "href" in a: s.links.append(a["href"])
        if t == "img": s.imgs.append(a)
        if t == "h1": s.h1 += 1
        if t == "title": s.in_title = True
        if t == "meta" and a.get("name") == "description": s.desc = a.get("content", "")
        if t == "link" and a.get("rel") in ("stylesheet", "preload", "icon"): s.res.append(a.get("href", ""))
        if t == "script" and a.get("src"): s.res.append(a["src"])
        if "class" in a and re.search(r'(^|\s)ph(\s|$)', a["class"]): s._ph = True; s.buf = ""
    def handle_data(s, d):
        if s.in_title: s.title += d
        if s._ph: s.buf += d
    def handle_endtag(s, t):
        if t == "title": s.in_title = False
        if s._ph and t in ("span", "p"): s.ph.append(s.buf.strip()); s._ph = False

pages = {}
for f in sorted(glob.glob(f"{root}/*.html")):
    p = P(); p.feed(open(f, encoding="utf-8").read()); pages[os.path.basename(f)] = p
errors, warns = [], []
titles = {}
used = set()
for n, p in pages.items():
    if n != "404.html":
        if p.h1 != 1: errors.append(f"{n}: {p.h1} h1 elements")
        if not p.desc: errors.append(f"{n}: no meta description")
    titles.setdefault(p.title.strip(), []).append(n)
    for h in p.links:
        if h.startswith(("http", "tel:", "mailto:")): continue
        target, _, frag = h.partition("#")
        t = target or n
        if not os.path.exists(f"{root}/{t}"): errors.append(f"{n}: broken link {h}"); continue
        used.add(t)
        if frag and t in pages and frag not in pages[t].ids: errors.append(f"{n}: missing anchor {h}")
    for i in p.imgs:
        src = i.get("src", ""); ss = i.get("srcset", "")
        if not src and not ss: continue  # empty placeholder image (photo viewer)
        for u in [src] + [x.strip().split()[0] for x in ss.split(",") if x.strip()]:
            if u.startswith("http"): errors.append(f"{n}: external image {u}"); continue
            if u and not os.path.exists(f"{root}/{u}"): errors.append(f"{n}: missing image {u}")
            used.add(u)
        if "alt" not in i: errors.append(f"{n}: image without alt {src}")
        if "width" not in i and "/clients/" not in src and "mark.jpg" not in src and "intro-logo" not in src: warns.append(f"{n}: image without width/height {src}")
    for r in p.res:
        if r.startswith("http") and not r.startswith("https://plausible.io/"): errors.append(f"{n}: external resource {r}")
        else: used.add(r)
for t, ns in titles.items():
    if len(ns) > 1: errors.append(f"duplicate title '{t}': {', '.join(ns)}")
css = open(f"{root}/site.css", encoding="utf-8").read(); js = open(f"{root}/site.js", encoding="utf-8").read()
for f in glob.glob(f"{root}/img/**/*", recursive=True) + glob.glob(f"{root}/*.png") + glob.glob(f"{root}/*.ico") + glob.glob(f"{root}/*.jpg"):
    if not os.path.isfile(f): continue
    rel = os.path.relpath(f, root).replace("\\", "/")
    if rel in used or rel in css or rel in js: continue
    if any(rel in open(g, encoding="utf-8").read() for g in glob.glob(f"{root}/*.html")): continue
    warns.append(f"unused file {rel}")
ph = {n: p.ph for n, p in pages.items() if p.ph}
total = sum(len(v) for v in ph.values())
print(f"{len(pages)} pages checked")
for e in errors: print("ERROR  ", e)
for w in warns: print("warning", w)
print(f"placeholders still to confirm: {total} across {len(ph)} pages" + ("" if total == 0 else "  (run tools/placeholders.py for the list)"))
if launch and total: errors.append("placeholders remain")
print("RESULT:", "FAIL" if errors else "OK")
sys.exit(1 if errors else 0)
