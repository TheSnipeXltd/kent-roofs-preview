"""Production pass over every page in the site folder. Safe to re-run.
python tools/finalize.py .
Does: index rename links, self-hosted fonts, favicons, noindex (until launch), skip link,
mobile call button + chat button, footer 'More' column, responsive WebP images, privacy/cookie text."""
import sys, re, glob, json, os
root = sys.argv[1]
dims = json.load(open(f"{root}/data/images.json", encoding="utf-8-sig"))
CHAT = '<a class="chat" href="https://wa.me/447961994386?text=Hi%20Kent%20Roofs%2C%20I%27d%20like%20a%20quote." aria-label="Chat on WhatsApp"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8.5 8.5 0 0 1-12.4 7.5L3 21l1.6-5.4A8.5 8.5 0 1 1 21 12z"/></svg><span>Chat</span></a>'
CALL = '<a class="callfab" href="tel:+447961994386" aria-label="Call Kent Roofs on 07961 994 386"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg></a>'
HEADBITS = '''<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="theme-color" content="#141517">
<meta name="robots" content="noindex,nofollow"><!--noindex-until-launch-->
<link rel="preload" href="fonts/bricolage-variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/hanken-variable.woff2" as="font" type="font/woff2" crossorigin>'''
MORE = '<div><p class="fh">More</p><a href="projects.html">Projects</a><br><a href="commercial-and-residential.html">Commercial and residential</a><br><a href="housing.html">Housing associations</a><br><a href="guides.html">Guides</a><br><a href="about.html">About</a></div>\n    '

def images(h, page):
    hero_done = False
    def sub(m):
        nonlocal hero_done
        pre, name, post = m.group(1), m.group(2), m.group(3)
        d = dims.get(name)
        if not d: return m.group(0)
        attrs = (pre + post)
        attrs = re.sub(r'\s*loading="[^"]*"', '', attrs)
        is_hero = 'class="shot"' in h[max(0, m.start()-60):m.start()] and not hero_done
        if is_hero: hero_done = True
        sizes = "(max-width:900px) 92vw, 460px" if is_hero else "(max-width:700px) 86vw, 380px"
        extra = 'fetchpriority="high"' if is_hero else 'loading="lazy" decoding="async"'
        return (f'<img {attrs.strip()} src="img/{name}-1200.webp" srcset="img/{name}-640.webp {d["w640"]}w, img/{name}-1200.webp {d["w1200"]}w" '
                f'sizes="{sizes}" width="{d["w1200"]}" height="{d["h1200"]}" {extra}>')
    return re.sub(r'<img ([^>]*?)src="img/(p\d+)\.jpg"([^>]*)>', sub, h)

for path in sorted(glob.glob(f"{root}/*.html")):
    n = os.path.basename(path)
    h = open(path, encoding="utf-8").read()
    h = h.replace("direction-a-sleek.html", "index.html")
    # self-hosted fonts: drop Google links
    h = re.sub(r'<link rel="preconnect" href="https://fonts\.(googleapis|gstatic)\.com"[^>]*>\s*', '', h)
    h = re.sub(r'<link href="https://fonts\.googleapis\.com/[^>]*>\s*', '', h)
    # head additions (once)
    if "noindex-until-launch" not in h and "<!--seo-->" not in h:
        h = h.replace('<link rel="stylesheet" href="site.css">', '<link rel="stylesheet" href="site.css">\n' + HEADBITS, 1)
    # skip link
    if "skip-link" not in h:
        h = h.replace("<body>", '<body>\n<a class="skip-link" href="#top">Skip to content</a>', 1)
    # floating buttons
    if 'class="chat"' not in h:
        h = h.replace('<script src="site.js">', CHAT + '\n<script src="site.js">', 1)
    if 'class="callfab"' not in h:
        h = h.replace('<script src="site.js">', CALL + '\n<script src="site.js">', 1)
    # keep the floating buttons inside a labelled region (screen readers)
    if 'class="fabs"' not in h:
        h = re.sub(r'(<a class="chat".*?</a>)\s*(<a class="callfab".*?</a>)', r'<aside class="fabs" aria-label="Quick contact">\1\2</aside>', h, count=1, flags=re.S)
    # footer: More column (once)
    if "<h4>More</h4>" not in h and ">More</p>" not in h:
        h = h.replace('<div><h4>Contact</h4>', MORE + '<div><h4>Contact</h4>', 1)
    h = re.sub(r'<h4>(.*?)</h4>', r'<p class="fh">\1</p>', h)  # footer labels are not headings
    # images
    h = images(h, n)
    # index: preload the hero image
    if n == "index.html" and 'rel="preload" as="image"' not in h:
        d = dims["p0021"]
        h = h.replace('<link rel="preload" href="fonts/bricolage-variable.woff2"', f'<link rel="preload" as="image" href="img/p0021-1200.webp" imagesrcset="img/p0021-640.webp {d["w640"]}w, img/p0021-1200.webp {d["w1200"]}w" imagesizes="(max-width:900px) 92vw, 460px">\n<link rel="preload" href="fonts/bricolage-variable.woff2"', 1)
    # privacy and cookie text: fonts are now served from this site
    if n == "privacy.html":
        h = re.sub(r'<h2>Google Fonts</h2>\s*<p>.*?</p>\s*', '', h, flags=re.S)
    if n == "cookies.html":
        h = re.sub(r'<li>Google Fonts supplies.*?</li>', '<li>The typefaces are served from this website, so no font requests go to other companies.</li>', h, flags=re.S)
    open(path, "w", encoding="utf-8").write(h)
print("finalized", len(glob.glob(f"{root}/*.html")), "pages")
