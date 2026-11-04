"""One-off generator for the extra pages (pubs, housing, guides, 404).
Run once from the site folder: python tools/build_extra.py .
After that, edit the generated HTML directly. Run tools/finalize.py afterwards."""
import sys, urllib.parse
out = sys.argv[1]
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>'
S = [("slating","Slating"),("tiling","Tiling"),("flat-roofing","Flat roofing"),("lead-work","Lead work"),("fascias-soffits","Fascias &amp; soffits"),("roof-repairs","Roof repairs")]
wa = lambda t="Hi Kent Roofs, I'd like a quote.": "https://wa.me/447961994386?text=" + urllib.parse.quote(t)
LEG = '<a href="privacy.html">Privacy</a> · <a href="cookies.html">Cookies</a> · <a href="terms.html">Terms</a>'
TM = 'Wetherspoon and Greene King are trademarks of their owners. Kent Roofs Limited is not affiliated with or endorsed by them.'

def head(title, desc, cur=""):
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | Kent Roofs Limited</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="site.css">
<noscript><style>.l>span,.rise{{transform:none;opacity:1}}</style></noscript>
</head>
<body>
<div class="prog" id="prog"></div>
<header id="hdr">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Kent Roofs Limited, home"><img src="img/mark.jpg" alt=""><span>Kent Roofs<small>Limited</small></span></a>
    <nav id="nav" aria-label="Main">
      <a href="index.html#services">Services</a><a href="projects.html">Projects</a><a href="about.html">About</a><a href="index.html#areas">Areas</a><a href="contact.html">Contact</a>
    </nav>
    <a class="btn sm" href="{wa()}">Get a quote</a>
    <button class="burger" id="burger" aria-expanded="false" aria-controls="nav" aria-label="Menu"><i></i><i></i></button>
  </div>
</header>
'''
FOOT = f'''<footer>
  <div class="wrap">
    <div><a class="brand" href="index.html" style="margin-bottom:16px"><img src="img/mark.jpg" alt=""><span>Kent Roofs<small>Limited</small></span></a><p>Slating, tiling, flat roofing and lead work across Kent.</p></div>
    <div><h4>Services</h4>{"<br>".join(f'<a href="service-{s}.html">{n}</a>' for s,n in S)}</div>
    <div><h4>Contact</h4><a href="tel:+447961994386">07961 994 386</a><br><a href="https://wa.me/447961994386">WhatsApp</a><br><span class="ph">hello@domain.co.uk</span><br><span class="ph">Registered address</span></div>
    <div class="small">Kent Roofs Limited · Registered in England and Wales No. <span class="ph">XXXXXXXX</span> · <span class="ph">Insurance details</span> · {LEG}</div>
  </div>
</footer>
<script src="site.js"></script>
</body>
</html>
'''
def crumb(*parts):
    items = '<a href="index.html">Home</a>'
    for i, (n, href) in enumerate(parts):
        items += '<span>/</span>' + (f'<a href="{href}">{n}</a>' if href else f'<span aria-current="page">{n}</span>')
    return f'<nav class="crumb" aria-label="Breadcrumb">{items}</nav>'
def cta(h, text="Message us on WhatsApp"):
    return f'''<div class="cta-box" style="margin-top:0"><h2>{h}</h2><div class="acts"><a class="btn" href="{wa()}">{text} {ARROW}</a><a class="link" href="tel:+447961994386">{PHONE}07961 994 386</a></div></div>'''
def top(h1, lead, crumbs, note=""):
    return f'''<main id="top">
<section class="page-head">
  <div class="wrap">
    {crumb(*crumbs)}
    <h1><span class="l" style="--i:0"><span>{h1}</span></span></h1>
    <p class="lead rise" style="--i:0">{lead}</p>
    {note}
  </div>
</section>
'''
PLATES = '''<div class="plates" role="list" aria-label="Pub clients">
      <div class="plate w" role="listitem"><img src="img/clients/wetherspoon.png" alt="Wetherspoon logo"></div>
      <div class="plate g" role="listitem"><img src="img/clients/greene-king.png" alt="Greene King logo"></div>
      <div class="plate more" role="listitem"><span>And many more<small>Pubs across the UK</small></span></div>
    </div>'''
def faq(items):
    return '<div class="faq">' + "".join(f'<div class="faq-item"><button aria-expanded="false">{q}<i></i></button><div class="faq-a"><div><p>{a}</p></div></div></div>' for q, a in items) + '</div>'
def incl(items): return '<ul class="incl">' + "".join(f"<li>{t}</li>" for t in items) + '</ul>'
def svc_links(skip=()):
    return '<div class="more" style="margin-top:30px">' + "".join(f'<a href="service-{s}.html">{n}{ARROW}</a>' for s, n in S if s not in skip) + '</div>'
def section(cls, inner): return f'<section class="pitch {cls}"><div class="wrap">{inner}</div></section>\n'
PH = lambda t: f'<span class="ph">{t}</span>'

pages = {}

# ---------------- commercial and residential ----------------
pages["commercial-and-residential"] = head("Commercial and residential roofing in Kent", "All types of roofs, commercial and residential, from Kent Roofs Limited. CITB-trained, with 15 years of housing association experience. Call 07961 994 386.") + \
 top("All types of roofs, commercial and residential", "Slating, tiling, flat roofing, lead and the finishing trades for homes and businesses, done by one CITB-trained team that Tom runs himself.", [("Commercial and residential", None)], '<p class="ph note rise" style="--i:1">Wording and any out-of-hours or permit details to confirm with Tom.</p>') + \
 section("g", f'<h2>Commercial work</h2>{PLATES}<p style="color:#cfcec8">Tom has worked with many pubs across the UK, including Wetherspoon and Greene King pubs. A commercial roof has to be fixed without stopping the business for longer than it has to, and safely around staff and customers.</p><p class="fine" style="margin-top:20px">{TM}</p>') + \
 section("c", f'<div class="two"><div><h2>How a commercial job runs</h2><p class="ph note">Approach to confirm with Tom.</p></div>{incl(["Safe access with Tom\'s own cherry pickers, which can reduce the need for full scaffold","Planned around the way your business trades",PH("Out-of-hours and weekend working to confirm"),"Work to your contractor or estate requirements","Tidy site and a clear finish date"])}</div>') + \
 section("s", f'<div class="two"><div><h2>Homes and residential</h2><p class="ph note">Scope to confirm with Tom.</p></div>{incl(["New roofs and re-roofs on houses","Roofing on extensions and dormers","Flat roofs on rear extensions","Repairs after leaks and storm damage","Fascias and soffits","Chimney and brickwork repairs"])}</div>') + \
 section("g", f'<div class="two"><div><h2>Questions from commercial clients</h2><p class="ph note">Draft answers. Tom to confirm.</p></div>{faq([("Can you work around opening hours?", PH("Working hours and out-of-hours options to confirm with Tom.")),("Do you need scaffold?","It depends on the roof and access. Tom has his own cherry pickers, which can be an alternative to full scaffold on some jobs."),("Can you provide your paperwork?", PH("Insurance, risk assessments and method statements to confirm with Tom.")),("Do you cover the whole UK?", PH("Travel range to confirm with Tom."))])}</div>') + \
 section("c", f'<h2>Every type of roof</h2><p style="color:#b7b6b0;margin-top:14px">Each service has its own page.</p>{svc_links()}<div style="margin-top:60px">{cta("Looking after a property or an estate?")}</div>') + "</main>\n" + FOOT

# ---------------- housing ----------------
pages["housing"] = head("Roofing for housing associations", "CITB-trained roofer with 15 years of housing association subcontracting. Slating, tiling, flat roofing and lead work. Call 07961 994 386.") + \
 top("Housing associations and contractors", "Tom spent 15 years subcontracting for housing associations before running Kent Roofs Limited. Working to a programme on live sites is how he already works.", [("Housing associations", None)], '<p class="ph note rise" style="--i:1">Scope, paperwork and any named associations to confirm with Tom. No client names are published until he agrees.</p>') + \
 section("g", f'<div class="two"><div><h2>What that experience covers</h2><p class="ph note">Typical work to confirm with Tom.</p></div>{incl(["Re-roofing and roof repairs","Slating and tiling","Flat roofing in felt, fibre glass and rubber","Lead flashings and valleys","Fascias and soffits","Brickwork and chimney repairs"])}</div>') + \
 section("c", f'<div class="two"><div><h2>Working on live sites</h2></div><div><p style="color:#cfcec8;margin-bottom:22px">Housing work usually runs to a programme, with residents living next to the job and other trades on site. Tom\'s years on that work shape how he runs every job.</p>{incl(["Own cherry pickers for quick, safe access","Programme-led working",PH("Resident liaison and site tidiness approach to confirm"),PH("Insurance, CSCS and method statements available on request: to confirm")])}</div></div>') + \
 section("s", f'<div class="two"><div><h2>Questions from contractors</h2><p class="ph note">Draft answers. Tom to confirm.</p></div>{faq([("Do you take subcontract work?", PH("Subcontract availability and minimum job size to confirm with Tom.")),("Can you work on a main contractor\'s programme?","Yes, that is the work Tom did for 15 years. Send the details and dates."),("What paperwork can you supply?", PH("Insurance, risk assessments, method statements and certificates to confirm with Tom."))])}</div>') + \
 section("c", f'<h2>Services</h2>{svc_links()}<div style="margin-top:60px">{cta("Have a programme to quote?")}</div>') + "</main>\n" + FOOT

# ---------------- guides ----------------
G = [
 dict(slug="slate-or-tile", title="Slate or tile: how to choose", desc="Plain-English guide to choosing between slate and tiles for a Kent roof: look, weight, pitch, planning and cost.", mins=4, svc=("slating","Slating"), svc2=("tiling","Tiling"),
  intro="Both make a good roof. The right one depends on your house, the roof's pitch and structure, and any planning rules.",
  body=[("Look and local style","Natural slate gives a thin, even, dark finish. Clay tiles give colour and texture, from smooth plain tiles to rough peg tiles. In a conservation area or on an older house, the planning authority may expect you to match what was there."),
        ("Weight and the roof structure","Slate is usually lighter than concrete tiles of similar coverage, and clay tiles vary. A heavier covering can need a stronger roof structure, so the timbers should be checked before you change material."),
        ("Pitch","Every slate and tile has a minimum roof pitch set by its maker. A shallow roof can limit your choice or need a different fixing method. Check the manufacturer's figure for the exact product."),
        ("Cost and lifespan","Natural slate usually costs more to buy and fix than concrete tiles, and good slate and clay can last for many decades. Fibre-cement slate and concrete tiles sit lower on price. A written quote for the exact product is the only reliable comparison."),
        ("Matching an existing roof","If you only need a repair or an extension, matching the existing covering often matters more than the ideal choice. Send photos and we can say what is realistic.")]),
 dict(slug="flat-roof-lifespan", title="How long does a flat roof last?", desc="What affects how long a flat roof lasts, and how felt, fibre glass and rubber systems compare.", mins=4, svc=("flat-roofing","Flat roofing"), svc2=("lead-work","Lead work"),
  intro="There is no single answer. It depends on the system, the quality of the installation and how well the roof drains.",
  body=[("Felt","Felt is a common choice on extensions and garages. Newer high-performance felts last longer than older types. Joints and edges are where it usually fails first."),
        ("Fibre glass","Fibre glass (GRP) forms one seamless layer, so there are no joints to open up. It suits awkward shapes and can be trimmed neatly at edges and upstands."),
        ("Rubber","Rubber membranes come in large sheets with few seams and are known for long service life when laid well."),
        ("What shortens a flat roof's life","Standing water, poor falls, blocked outlets, damage from foot traffic and badly sealed upstands or rooflights. Regular clearing of leaves and a look after storms help."),
        ("Typical lifespans","Manufacturers and trade bodies publish ranges for each system, and installers give guarantees. Ask for the figure and guarantee for the exact system in your quote.")]),
 dict(slug="signs-your-roof-needs-attention", title="Signs your roof needs attention", desc="Common signs of roof problems, what you can safely check from the ground, and when to call a roofer.", mins=3, svc=("tiling","Tiling"), svc2=("slating","Slating"),
  intro="Many roof problems are small when you catch them. Here is what to look for, and what to leave to a roofer.",
  body=[("From the ground and inside","Slipped, cracked or missing tiles or slates; sagging lines on the ridge; damp patches or brown stains on ceilings; daylight in the loft; and water marks around chimneys and roof windows. Binoculars help."),
        ("Around the edges","Gutters overflowing, plants growing from them, and sagging or rotten fascias and soffits. These can let water into the roof edge."),
        ("Lead and flashings","Lifting or cracked lead around chimneys, walls and dormers is a common route for leaks."),
        ("After a storm","Check for debris, displaced tiles and new stains. Take photos if you can do so safely from the ground."),
        ("What not to do","Do not climb onto the roof or lean ladders against fragile edges. A roofer should inspect it. Moss on its own is rarely an emergency, but a lot of it can hold moisture."),
        ("When to call","Any active leak, missing tiles or storm damage is worth a call. Send photos and your postcode on WhatsApp and we will tell you what we see.")]),
]
def guide_page(g):
    secs = "".join(f"<h2>{h}</h2><p>{p}</p>" for h, p in g["body"])
    others = "".join(f'<a href="guide-{o["slug"]}.html">{o["title"]}{ARROW}</a>' for o in G if o is not g)
    return head(g["title"], g["desc"]) + f'''<main id="top">
<section class="page-head">
  <div class="wrap">
    {crumb(("Guides","guides.html"),(g["title"],None))}
    <h1><span class="l" style="--i:0"><span>{g["title"]}</span></span></h1>
    <p class="lead rise" style="--i:0">{g["intro"]}</p>
    <p class="ph note rise" style="--i:1">Draft guide. Tom to check it for accuracy before publishing.</p>
  </div>
</section>
<section class="pitch c" style="margin-top:0;clip-path:none;padding-top:clamp(20px,3vw,40px)">
  <div class="wrap"><div class="prose">
    <p class="meta">{g["mins"]} minute read</p>
    {secs}
    <p>Related: <a href="service-{g["svc"][0]}.html">{g["svc"][1]}</a> and <a href="service-{g["svc2"][0]}.html">{g["svc2"][1]}</a>.</p>
  </div></div>
</section>
<section class="pitch g"><div class="wrap">
  <h2>More guides</h2><div class="more" style="margin:30px 0 60px">{others}</div>
  {cta("Not sure what your roof needs?","Send photos on WhatsApp")}
</div></section>
</main>
''' + FOOT
for g in G: pages["guide-" + g["slug"]] = guide_page(g)
cards = "".join(f'<a class="gcard" href="guide-{g["slug"]}.html"><b>{g["title"]}</b><span>{g["intro"]}</span><em>{g["mins"]} minute read{ARROW}</em></a>' for g in G)
pages["guides"] = head("Roofing guides", "Plain-English roofing guides from Kent Roofs Limited: slate or tile, flat roof lifespan and signs your roof needs attention.") + \
 top("Roofing guides", "Short, plain-English answers to the questions homeowners ask before a roof job.", [("Guides", None)], '<p class="ph note rise" style="--i:1">Drafts. Tom to check each guide for accuracy before they go live.</p>') + \
 f'<section class="pitch c" style="margin-top:0;clip-path:none;padding-top:clamp(20px,3vw,40px)"><div class="wrap"><div class="gcards">{cards}</div></div></section>\n</main>\n' + FOOT

# ---------------- 404 ----------------
pages["404"] = head("Page not found", "That page does not exist. Go to the Kent Roofs Limited homepage or call 07961 994 386.") + \
 top("Page not found", "That page has moved or never existed. Try the homepage, or call us on 07961 994 386.", [("Page not found", None)]) + \
 f'<section class="pitch c" style="margin-top:0;clip-path:none;padding-top:20px"><div class="wrap"><div class="cta" style="display:flex;gap:26px;flex-wrap:wrap"><a class="btn" href="index.html">Go to the homepage {ARROW}</a><a class="link" href="tel:+447961994386">{PHONE}Call 07961 994 386</a></div></div></section>\n</main>\n' + FOOT

only = sys.argv[2:]
for n, t in pages.items():
    if only and n not in only: continue
    open(f"{out}/{n}.html", "w", encoding="utf-8").write(t)
print("wrote", ", ".join(sorted(pages)))
