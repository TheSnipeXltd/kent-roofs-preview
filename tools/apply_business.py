"""Fill the dashed placeholders from data/business.json. Safe to re-run; empty values are skipped.
python tools/apply_business.py .
Set "copy_approved": true once Tom has signed off every draft page: removes the 'Draft / to confirm' banners (not the unfilled placeholders)."""
import sys, re, glob, json, os, html
root = sys.argv[1].rstrip("/\\")
d = json.load(open(f"{root}/data/business.json", encoding="utf-8-sig"))
E = html.escape
def span(txt): return f'<span class="ph">{txt}</span>'
reps = []
if d.get("email"): reps.append((span("hello@domain.co.uk"), f'<a href="mailto:{E(d["email"])}">{E(d["email"])}</a>'))
if d.get("address"): reps.append((span("Registered address"), E(d["address"])))
if d.get("company_number"): reps.append((span("XXXXXXXX"), E(d["company_number"])))
if d.get("insurance_footer"): reps.append((span("Insurance details"), E(d["insurance_footer"])))
if d.get("hours"): reps.append((span("Opening hours to confirm"), E(d["hours"])))
if d.get("insurance_cover"): reps.append((span("Cover amount and insurer to confirm"), E(d["insurance_cover"])))
if d.get("cscs"): reps.append((span("Card type to confirm"), E(d["cscs"])))
if d.get("guarantee"):
    reps.append((span("Terms to confirm"), E(d["guarantee"])))
    reps.append((span("Guarantee terms to confirm with Tom."), E(d["guarantee"])))
if d.get("materials"): reps.append((span("Materials and colours to confirm with Tom."), E(d["materials"])))
if d.get("pub_hours"): reps.append((span("Working hours and out-of-hours options to confirm with Tom."), E(d["pub_hours"])))
if d.get("pub_paperwork"): reps.append((span("Insurance, risk assessments and method statements to confirm with Tom."), E(d["pub_paperwork"])))
if d.get("travel_range"): reps.append((span("Travel range to confirm with Tom."), E(d["travel_range"])))
if d.get("subcontract"): reps.append((span("Subcontract availability and minimum job size to confirm with Tom."), E(d["subcontract"])))
if d.get("housing_paperwork"): reps.append((span("Insurance, risk assessments, method statements and certificates to confirm with Tom."), E(d["housing_paperwork"])))
areas = d.get("areas") or []
projects = d.get("projects") or {}
today = d.get("legal_reviewed_date", "")
n_changes = 0
for path in glob.glob(f"{root}/*.html"):
    n = os.path.basename(path)
    h0 = h = open(path, encoding="utf-8").read()
    for a, b in reps: h = h.replace(a, b)
    if areas:
        chips = "".join(f"<span>{E(t)}</span>" for t in areas)
        h = re.sub(r'(<div class="areas">).*?(</div>)', lambda m: m.group(1) + chips + m.group(2), h, flags=re.S)
        h = re.sub(r'<p class="ph[^"]*"[^>]*>Example towns\. Tom to confirm\.</p>', '', h)
    # project towns / titles by photo id
    def block(m):
        b = m.group(0)
        pid = re.search(r'img/(p\d+)-', b)
        if not pid or pid.group(1) not in projects: return b
        pr = projects[pid.group(1)]
        if pr.get("town"): b = b.replace('<span class="ph">Town, Kent</span>', f'<span>{E(pr["town"])}</span>')
        if pr.get("title"): b = re.sub(r'(<b>)[^<]*(</b>)', lambda x: x.group(1) + E(pr["title"]) + x.group(2), b, count=1)
        return b
    if projects: h = re.sub(r'<figure>.*?</figure>|<button class="tile".*?</button>', block, h, flags=re.S)
    if d.get("copy_approved"):
        h = re.sub(r'\s*<p class="ph note[^"]*"[^>]*>.*?</p>', '', h, flags=re.S)
        h = re.sub(r'\s*<p class="ph" style="border:0;border-bottom:1px dashed var\(--gold\)">[^<]*</p>', '', h)
    if today and n in ("privacy.html", "cookies.html", "terms.html"):
        h = re.sub(r'<p class="meta">Draft 1[^<]*</p>', f'<p class="meta">Last updated {E(today)}</p>', h)
        h = re.sub(r'\s*<p class="ph note[^"]*"[^>]*>Draft written to match[^<]*</p>', '', h)
    if h != h0: open(path, "w", encoding="utf-8").write(h); n_changes += 1
print(f"updated {n_changes} pages")
