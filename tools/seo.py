"""Launch SEO pass. Needs "domain" in data/business.json (for example "https://www.kentroofs.co.uk").
python tools/seo.py .
Writes sitemap.xml and robots.txt, removes the pre-launch noindex, adds canonical + share tags + structured data. Safe to re-run."""
import sys, re, glob, json, os, datetime, html
root = sys.argv[1].rstrip("/\\")
d = json.load(open(f"{root}/data/business.json", encoding="utf-8-sig"))
dom = (d.get("domain") or "").rstrip("/")
if not dom.startswith("https://"): sys.exit('Set "domain" (starting https://) in data/business.json first.')
E = lambda s: html.escape(s, quote=True)
today = datetime.date.today().isoformat()
SERV = {"slating":"Slating","tiling":"Tiling","flat-roofing":"Flat roofing","lead-work":"Lead work","fascias-soffits":"Fascias and soffits","roof-repairs":"Roof repairs"}

def biz():
    b = {"@type": "RoofingContractor", "@id": dom + "/#business", "name": "Kent Roofs Limited", "url": dom + "/",
         "telephone": "+447961994386", "image": dom + "/og-image.jpg", "logo": dom + "/icon-512.png",
         "description": "CITB-trained roofer with 15 years of housing association experience. Slating, tiling, flat roofing and lead work across Kent."}
    if d.get("email"): b["email"] = d["email"]
    a = d.get("address_parts") or {}
    if a.get("streetAddress"): b["address"] = {"@type": "PostalAddress", "addressCountry": "GB", **{k: v for k, v in a.items() if v}}
    if d.get("areas"): b["areaServed"] = [{"@type": "AdministrativeArea", "name": t} for t in d["areas"]]
    if d.get("opening_hours"): b["openingHours"] = d["opening_hours"]
    if d.get("same_as"): b["sameAs"] = d["same_as"]
    return b
pages = sorted(glob.glob(f"{root}/*.html"))
urls = []
for p in pages:
    n = os.path.basename(p)
    h = open(p, encoding="utf-8").read()
    h = re.sub(r'<!--seo-->.*?<!--/seo-->\s*', '', h, flags=re.S)
    h = re.sub(r'<meta name="robots" content="noindex,nofollow"><!--noindex-until-launch-->\s*', '', h)
    slug = "" if n == "index.html" else n
    url = f"{dom}/{slug}"
    title = re.search(r"<title>(.*?)</title>", h, re.S).group(1).strip()
    desc = (re.search(r'<meta name="description" content="(.*?)"', h) or [None, ""])[1]
    block = [f'<link rel="canonical" href="{url}">',
             '<meta property="og:type" content="website">', '<meta property="og:locale" content="en_GB">', '<meta property="og:site_name" content="Kent Roofs Limited">',
             f'<meta property="og:title" content="{title}">', f'<meta property="og:description" content="{desc}">',
             f'<meta property="og:url" content="{url}">', f'<meta property="og:image" content="{dom}/og-image.jpg">',
             '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
             '<meta name="twitter:card" content="summary_large_image">']
    ld = []
    if n == "index.html": ld.append({"@context": "https://schema.org", **biz()})
    m = re.match(r"service-(.*)\.html", n)
    if m and m.group(1) in SERV:
        ld.append({"@context": "https://schema.org", "@type": "Service", "name": SERV[m.group(1)], "serviceType": SERV[m.group(1)],
                   "provider": {"@id": dom + "/#business"}, "areaServed": d.get("areas") or "Kent", "url": url, "description": desc})
    for x in ld: block.append('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>")
    h = h.replace("</head>", "<!--seo-->\n" + "\n".join(block) + "\n<!--/seo-->\n</head>", 1)
    open(p, "w", encoding="utf-8").write(h)
    if n != "404.html": urls.append(url)
open(f"{root}/sitemap.xml", "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n")
open(f"{root}/robots.txt", "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\n\nSitemap: {dom}/sitemap.xml\n")
print(f"seo applied to {len(pages)} pages; sitemap has {len(urls)} urls")
