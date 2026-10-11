# Changelog

## 2026-10-03 (Economics: Twenty Letters)
- New (draft): `content/blog/economics/twenty-letters.md` — UK CPI Dec 2019→Aug 2026 vs 2% target (+32.4%, 4.29%/yr compound vs 2%; price level 16.0% above 2% path; 26/80 months inside 1–3%); reconciliation with BoE inflation calculator (£1,330.14 / 33.0% / 3.83% — 2019 annual-avg base, ~7.7yr annualisation); table + phase summary of all 20 Governor→Chancellor CPI open letters (Jun 2020–Sep 2026); critique (exogenous-cause framing, forecast-miss table, asymmetry, accountability, counter-arguments); M4 vs CPI 2000–2026 section; Sept 2026 MPC 6–3 split (hold 3.75%: Bailey, Breeden, Dhingra, Lombardelli, Ramsden, Taylor; hike to 4%: Greene, Mann, Pill) + unanimous QT-to-zero-by-2034 decision.
- New: `static/data/economics/uk_cpi_m4_monthly_1999-2026.csv` (ONS D7BT, D7G7; BoE IADB LPMAUYN, LPMVQJW; fetched 2026-10-03), `static/data/economics/inflation_since_2019_charts.py`.
- New: `static/images/economics/inflation-since-2019-cpi-vs-target.png`, `static/images/economics/inflation-m4-vs-cpi-2000-2026.png`.

## 2026-09-28 (LLM Credit series #11)
- New: `content/blog/comp-science/no-two-banks-say-it-the-same-way.md` — 11th post in the LLM Credit series. Agents vs pre-coded Python scraping; data-challenge examples from the audit logs of the last 10 banks (Webster, UniCredit, U.S. Bancorp, TD, Synchrony, State Street, SocGen, SMFG, Scotiabank, Santander); peer-comparison argument. Stats from `verified_metrics.sqlite` as at 2026-09-28.
- Series made sequential: `11.` entry added to the Full Series list in all 10 prior posts; `audit-the-neighbor-too.md` Next → new post.
- `expensive-on-purpose.md` (separate ops series): see-also line now links the new post; its own nav unchanged.
- `no-two-banks-say-it-the-same-way.md`: added sections "What It Costs to Get a Bank Through the Gate" (measured UBS/MUFG token anchors + indicative per-bank token table for last 10 banks, derived at 1.4–2.4K tokens/cell + ~84K bootstrap/session; active minutes from audit logs), "Three Options, One Viable Path" (coded vs manual ~2,750h/pass at assumed 5 min/cell over 33,102 cells vs agentic), "The Agent Gets Better Without Retraining" (checklist A1–C8, 2,015 location hints, 174 architecture_feedback, bootstrap skill + LESSONS.md). Description + Key Takeaways updated.
- `no-two-banks-say-it-the-same-way.md`: added "Ten more, from the rest of the corpus" (from `architecture_feedback`: #44/#18/#71 wrong company + resync re-ingest; #10/#136/#137 regulatory floor as actual; #59 Advanced vs Standardized; #106 APRA internationally-comparable row; #133/#117 parent vs group; #35/#115/#27 filename vs period; #116/#37/#55 units/scale; #90 SEC Item 301; #95/#93 IRRBB measurement; #94/#56 genuine outlier + self-contradicting source). Peer-comparison list +2 bullets (CBA, BNY).

## 2026-09-28
- `content/blog/economics/interest-rates-are-interesting.md`: added "Update — 28 Sep 2026" commentary (Mar→Aug 2026 curve moves); data as-at note updated.
- `static/data/economics/BoE_Spot_Curve_Master.csv`: appended BoE GLC nominal spot month ends Apr–Aug 2026; restored missing Jan 2025 row (original loader skipped first data row of 2025 file). 680 rows, 1970-01 → 2026-08, no gaps.
- `static/images/economics/10_spot_curve_animation.gif`: rebuilt, 227 quarterly frames to Aug 2026, maturity axis labelled, 1yr-earlier ghost curve, 10yr/steepness readout, 3s hold on last frame.
- `static/tools/yield_curve_player.html`: frames re-embedded (227); scrubber max / frame counter updated.
- New: `static/data/economics/boe_spot_curve_animation.py` (update + animation script), `BoE_spot_new_rows_2026-09.csv` (raw rows extracted from BoE 2025-to-present workbook, sheet "4. spot curve").
- Previous versions of the three data/image files in `_to_delete/boe_2026-04_backup/`.
