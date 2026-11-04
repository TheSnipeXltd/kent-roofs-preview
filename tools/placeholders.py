"""List every unconfirmed placeholder, grouped by what is needed. python tools/placeholders.py ."""
import sys, re, glob, os, collections
root = sys.argv[1].rstrip("/\\")
seen = collections.OrderedDict()
for f in sorted(glob.glob(f"{root}/*.html")):
    h = open(f, encoding="utf-8").read()
    for m in re.finditer(r'<(span|p)[^>]*class="ph[^"]*"[^>]*>(.*?)</\1>', h, re.S):
        t = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        seen.setdefault(t, []).append(os.path.basename(f))
for t, ps in sorted(seen.items(), key=lambda x: -len(x[1])):
    print(f"{len(ps):>3}x  {t}\n       {', '.join(sorted(set(ps)))}")
print(f"\n{sum(len(v) for v in seen.values())} placeholders, {len(seen)} different")
