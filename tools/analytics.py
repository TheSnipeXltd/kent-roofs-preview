"""Switch on cookieless analytics (Plausible). Safe to re-run.
1. Create a Plausible site for your domain, then put the bare domain (for example kentroofs.co.uk) in
   data/business.json -> analytics.plausible_domain
2. python tools/analytics.py .
Adds the script to every page, counts Call and WhatsApp clicks as events, allows plausible.io in the
security headers, and updates the privacy and cookie notices. Plausible uses no cookies, so no banner."""
import sys, re, glob, json, os
root = sys.argv[1].rstrip("/\\")
d = json.load(open(f"{root}/data/business.json", encoding="utf-8-sig"))
a = d.get("analytics") or {}
dom = (a.get("plausible_domain") or "").strip().lower()
if not dom: sys.exit('Set analytics.plausible_domain in data/business.json first (for example "kentroofs.co.uk").')
TAG = f'<!--analytics-->\n<script defer data-domain="{dom}" src="https://plausible.io/js/script.tagged-events.js"></script>\n<!--/analytics-->\n'

def tag_links(h):
    def add(m):
        attrs = m.group(0)
        name = "Call+click" if 'href="tel:' in attrs else "WhatsApp+click"
        cls = f"plausible-event-name={name}"
        if cls in attrs: return attrs
        if 'class="' in attrs: return attrs.replace('class="', f'class="{cls} ', 1)
        return attrs.replace("<a ", f'<a class="{cls}" ', 1)
    return re.sub(r'<a [^>]*href="(?:tel:[^"]*|https://wa\.me/[^"]*)"[^>]*>', add, h)

for p in glob.glob(f"{root}/*.html"):
    n = os.path.basename(p); h = open(p, encoding="utf-8").read()
    h = re.sub(r'<!--analytics-->.*?<!--/analytics-->\s*', '', h, flags=re.S)
    h = h.replace("</head>", TAG + "</head>", 1)
    h = tag_links(h)
    if n == "privacy.html":
        h = h.replace("The website has no account area and no analytics at present. It does not collect your details itself:",
                      "The website has no account area. It uses Plausible Analytics to count visits, which does not use cookies, does not store anything on your device and does not follow you across other sites. The website does not collect your details itself:")
    if n == "cookies.html":
        h = h.replace("There are no advertising cookies, no analytics and no social media trackers on this site, so there is no cookie banner.",
                      "We use Plausible Analytics to count visits. It does not use cookies, does not store anything on your device and does not follow you across other sites. There are no advertising cookies and no social media trackers, so there is no cookie banner.")
        h = re.sub(r'\s*<span class="ph">Tom to tell us if he wants analytics[^<]*</span>', '', h)
        h = h.replace("If we add analytics or any cookie that is not strictly necessary,", "If we add any cookie that is not strictly necessary,")
    open(p, "w", encoding="utf-8").write(h)

for f in ("vercel.json", "_headers"):
    path = f"{root}/{f}"
    if not os.path.exists(path): continue
    t = open(path, encoding="utf-8").read()
    if "plausible.io" not in t:
        t = t.replace("script-src 'self'", "script-src 'self' https://plausible.io").replace("connect-src 'self'", "connect-src 'self' https://plausible.io")
        open(path, "w", encoding="utf-8").write(t)
print(f"analytics on for {dom}; script added to {len(glob.glob(root + '/*.html'))} pages")
