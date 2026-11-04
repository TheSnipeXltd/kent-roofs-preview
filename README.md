# Kent Roofs Limited website

Static site: plain HTML, one stylesheet (`site.css`), one script (`site.js`), self-hosted fonts and WebP images. No build step, no dependencies. Open `index.html` or serve the folder.

```bash
python -m http.server 5190        # then open http://localhost:5190
```

## Folder
- `*.html` pages (home, 6 services, projects, about, contact, pubs, housing, guides + 3 guides, 3 legal pages, 404)
- `img/` photos (`pNNNN-640.webp`, `pNNNN-1200.webp`), logo crops, `clients/` (Wetherspoon and Greene King logos, as supplied)
- `fonts/` Bricolage Grotesque and Hanken Grotesk (latin subset, SIL Open Font License)
- `data/business.json` the one file to fill with Tom's details; `data/images.json` image sizes
- `tools/` scripts (below), `vercel.json` and `_headers` security and cache headers

## Scripts (Python 3, no packages)
| Command | What it does |
|---|---|
| `python tools/check.py .` | Broken links, anchors, images, alt text, titles, descriptions, h1s, external requests, unused files, placeholder count |
| `python tools/check.py . --launch` | Same, and fails while any placeholder remains |
| `python tools/placeholders.py .` | Lists every unconfirmed placeholder, grouped |
| `python tools/apply_business.py .` | Fills placeholders from `data/business.json` (email, address, company number, insurance, hours, guarantee, areas, project towns/titles) |
| `python tools/seo.py .` | Needs `domain` in `data/business.json`. Writes `sitemap.xml`, `robots.txt`, canonical and share tags, structured data, and removes the pre-launch `noindex` |
| `python tools/analytics.py .` | Needs `analytics.plausible_domain` in `data/business.json`. Adds cookieless Plausible analytics to every page, counts Call and WhatsApp clicks, allows plausible.io in the security headers, updates the privacy and cookie notices |
| `python tools/finalize.py .` | Re-applies the production pass (fonts, favicons, skip link, call button, responsive images). Safe to re-run |

## Launch order
1. Fill `data/business.json` (leave unknown fields empty).
2. `python tools/apply_business.py .`
3. Tom reads every draft page. Set `"copy_approved": true` and `"legal_reviewed_date"` once signed off, then run step 2 again.
4. `python tools/check.py . --launch` must say `RESULT: OK`.
5. Set `"domain"`, run `python tools/seo.py .`
5b. Create the site in Plausible, set `analytics.plausible_domain`, run `python tools/analytics.py .`
6. Deploy the folder to a static host. `vercel.json` (Vercel) or `_headers` (Netlify, Cloudflare Pages) adds the security headers.
7. Submit `sitemap.xml` in Google Search Console and claim the Google Business Profile.

## Notes
- All pages carry `noindex` until `seo.py` runs, so a draft cannot be indexed by mistake.
- The opening animation (home page only) plays on first visit and on refresh; it is skipped when arriving from another page of the site or with back/forward, and for people with reduced motion.
- `tools/build_extra.py` was a one-off generator for the pubs, housing, guides and 404 pages. Edit the HTML directly from now on; do not re-run it.
- Legal pages are drafts and need a solicitor's review.

## Decisions made
- Enquiries are WhatsApp only (no email form, no stored leads).
- Analytics: yes, cookieless (Plausible). Switched on by `tools/analytics.py` once an account exists.
- Accessibility: axe-core 4.9.1 scan of all 20 pages, 0 violations (4 November 2026).
