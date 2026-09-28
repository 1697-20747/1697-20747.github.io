# Changelog

## 2026-09-28
- `content/blog/economics/interest-rates-are-interesting.md`: added "Update — 28 Sep 2026" commentary (Mar→Aug 2026 curve moves); data as-at note updated.
- `static/data/economics/BoE_Spot_Curve_Master.csv`: appended BoE GLC nominal spot month ends Apr–Aug 2026; restored missing Jan 2025 row (original loader skipped first data row of 2025 file). 680 rows, 1970-01 → 2026-08, no gaps.
- `static/images/economics/10_spot_curve_animation.gif`: rebuilt, 227 quarterly frames to Aug 2026, maturity axis labelled, 1yr-earlier ghost curve, 10yr/steepness readout, 3s hold on last frame.
- `static/tools/yield_curve_player.html`: frames re-embedded (227); scrubber max / frame counter updated.
- New: `static/data/economics/boe_spot_curve_animation.py` (update + animation script), `BoE_spot_new_rows_2026-09.csv` (raw rows extracted from BoE 2025-to-present workbook, sheet "4. spot curve").
- Previous versions of the three data/image files in `_to_delete/boe_2026-04_backup/`.
