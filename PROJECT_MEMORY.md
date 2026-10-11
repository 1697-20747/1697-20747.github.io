# Project Memory

## BoE yield curve post (interest-rates-are-interesting)
- Source: https://www.bankofengland.co.uk/statistics/yield-curves → "Monthly government liability curve (nominal): archive data" (glcnominalmonthedata.zip); use "GLC Nominal month end data_2025 to present.xlsx", sheet "4. spot curve".
- Update: extract new rows (Excel serial date + 80 maturities 0.5–40y) to CSV, then
  `python3 static/data/economics/boe_spot_curve_animation.py <master.csv> <new_rows.csv> <old player.html> <outdir>`
  → writes master CSV, GIF, player HTML to outdir.
- Gotcha: 2025+ workbook has no blank row after the "years:" header; original loader (`boe_yield_curve_analysis.py`, `mat_row + 2`) dropped Jan 2025.
- 30yr series only starts 2016. GIF is commented out in the post; the iframe player is what renders.
- Last update: 2026-09-28, data to 2026-08-28.

## LLM Credit series (content/blog/comp-science/)
- Main LLM Credit series (anchored on llm-credit-paper-generator): not-a-specification (1) → … → audit-the-neighbor-too (10) → no-two-banks-say-it-the-same-way (11, latest, 2026-09-28). Separate operational series: expensive-on-purpose (1, only post; cross-linked via see-also).
- Each post ends with Previous/Next + "Full Series" list; adding a post means updating the prior post's Next + the Full Series list in EVERY series post.
- Source material: `~/Documents/projects/llm_credit_paper/processed/claude_code_audits/*.json` (per-bank agent audit logs), `processed/verified_metrics.sqlite` (`architecture_feedback`, `metrics.superseded_by`), llm_credit_paper CHANGELOG.md.
- Token data: agent audit logs don't record tokens (token_or_cost_usage always 'not available'). Only measured anchors: UBS ~486K/199 cells, MUFG ~483K/339 cells. Per-bank figures in no-two-banks post are derived estimates (1.4–2.4K tokens/cell + ~84K bootstrap/session).

## Inflation / BoE letters post (twenty-letters, economics, draft)
- Data: ONS CPI via `https://www.ons.gov.uk/generator?format=csv&uri=/economy/inflationandpriceindices/timeseries/{d7bt,d7g7}/mm23`; M4 via BoE IADB `_iadb-fromshowcolumns.asp?csv.x=yes&...&SeriesCodes=LPMAUYN,LPMVQJW&CSVF=TN&UsingCodes=Y` (CSVF=TT adds series titles). Both hosts blocked from Cowork sandbox/bridge; fetched via in-app browser JS `fetch()` on same origin.
- Update: append rows to `uk_cpi_m4_monthly_1999-2026.csv`, run `python3 static/data/economics/inflation_since_2019_charts.py` (prints stats, writes both PNGs). Add new letter dates to `LETTERS` list.
- Letters list: BoE `/sitemap/letters`. 2023 Mar/Jun governor PDFs robots-blocked on BoE; gov.uk asset copies used.
- BoE calculator 3.83% ≈ 33% annualised over ~7.67yrs (from Jan 2019); Dec 2019 base gives 4.29%.
- Last update: 2026-10-03, data to Aug 2026; MPC Sep 2026 (next decision 5 Nov 2026).
