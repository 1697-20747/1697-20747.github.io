# Project Memory

## BoE yield curve post (interest-rates-are-interesting)
- Source: https://www.bankofengland.co.uk/statistics/yield-curves → "Monthly government liability curve (nominal): archive data" (glcnominalmonthedata.zip); use "GLC Nominal month end data_2025 to present.xlsx", sheet "4. spot curve".
- Update: extract new rows (Excel serial date + 80 maturities 0.5–40y) to CSV, then
  `python3 static/data/economics/boe_spot_curve_animation.py <master.csv> <new_rows.csv> <old player.html> <outdir>`
  → writes master CSV, GIF, player HTML to outdir.
- Gotcha: 2025+ workbook has no blank row after the "years:" header; original loader (`boe_yield_curve_analysis.py`, `mat_row + 2`) dropped Jan 2025.
- 30yr series only starts 2016. GIF is commented out in the post; the iframe player is what renders.
- Last update: 2026-09-28, data to 2026-08-28.
