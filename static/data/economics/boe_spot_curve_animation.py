"""
Update BoE master spot-curve CSV and rebuild the yield curve animation.

Inputs : BoE_Spot_Curve_Master.csv (existing master)
         new_rows.csv  (Excel-serial date, 80 spot yields 0.5y..40y) extracted from
         'GLC Nominal month end data_2025 to present.xlsx', sheet '4. spot curve'
         (https://www.bankofengland.co.uk/statistics/yield-curves)
Outputs: BoE_Spot_Curve_Master.csv (updated), 10_spot_curve_animation.gif,
         yield_curve_player.html (frames re-embedded)
"""
import base64, io, re, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image

MASTER, NEW, OLD_PLAYER, OUT = sys.argv[1:5]

DARK_BG, DARK_AXES, GRID_COL, TEXT_COL = '#0d1117', '#161b22', '#30363d', '#e6edf3'
GREEN, RED, GOLD = '#3fb950', '#f78166', '#FFD700'
SOURCE_NOTE = 'Source: Bank of England yield curve data (GLC nominal, month end)'
plt.rcParams.update({
    'figure.facecolor': DARK_BG, 'axes.facecolor': DARK_AXES, 'axes.edgecolor': GRID_COL,
    'axes.labelcolor': TEXT_COL, 'axes.titlecolor': TEXT_COL, 'xtick.color': TEXT_COL,
    'ytick.color': TEXT_COL, 'text.color': TEXT_COL, 'grid.color': GRID_COL,
    'grid.linestyle': '--', 'grid.alpha': 0.5, 'font.family': 'DejaVu Sans', 'font.size': 10,
})

# ── 1. Merge new month-end rows into master ─────────────────────────────────
spot = pd.read_csv(MASTER, index_col=0, parse_dates=True)
mats = [c for c in spot.columns if c != 'Steepness']
new = pd.read_csv(NEW, header=None)
new.index = pd.to_datetime('1899-12-30') + pd.to_timedelta(new.pop(0), unit='D')
new.columns = mats
new['Steepness'] = new['5.0'] - new['0.5']
spot = pd.concat([spot, new])
spot = spot[~spot.index.duplicated(keep='last')].sort_index()
spot.index.name = 'Date'
spot.to_csv(f'{OUT}/BoE_Spot_Curve_Master.csv')
print(f'Master: {len(spot)} rows, {spot.index[0].date()} -> {spot.index[-1].date()}')

# ── 2. Frames: last month-end observation in each quarter ───────────────────
x = np.array([float(m) for m in mats])
q = spot.groupby(spot.index.to_period('Q')).tail(1)
steep = spot['Steepness'].dropna()

vals = spot[mats].values.flatten()
ymin, ymax = np.nanpercentile(vals, 0.5) - 0.5, np.nanpercentile(vals, 99.5) + 0.5

fig = plt.figure(figsize=(12, 8), dpi=100)
gs = fig.add_gridspec(2, 1, height_ratios=[2.3, 1], hspace=0.28,
                      left=0.08, right=0.97, top=0.93, bottom=0.1)
ax, ax2 = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])

ax.set_xlim(x.min(), x.max()); ax.set_ylim(ymin, ymax)
ax.set_xlabel('Maturity (years)', fontsize=10); ax.set_ylabel('Yield (%)', fontsize=11)
ax.grid(alpha=0.4); ax.axhline(0, color=GRID_COL, linewidth=0.8)
ax.set_title('UK Nominal Spot Yield Curve — Historical Evolution', fontsize=13, fontweight='bold')
ghost, = ax.plot([], [], linewidth=1.2, color=GOLD, alpha=0.18)   # curve one year earlier
line, = ax.plot([], [], linewidth=2.5, color=GOLD)
date_txt = ax.text(0.02, 0.92, '', transform=ax.transAxes, fontsize=13, fontweight='bold')
info_txt = ax.text(0.98, 0.92, '', transform=ax.transAxes, fontsize=10, ha='right', color='#8b949e')

ax2.fill_between(steep.index, steep.values, 0, where=steep.values >= 0, color=GREEN, alpha=0.35, linewidth=0)
ax2.fill_between(steep.index, steep.values, 0, where=steep.values < 0, color=RED, alpha=0.35, linewidth=0)
ax2.plot(steep.index, steep.values, linewidth=0.6, color='#8b949e', alpha=0.8)
ax2.axhline(0, color='#8b949e', linewidth=0.8, linestyle='--')
ax2.set_xlim(steep.index[0], steep.index[-1] + pd.Timedelta(days=120))
ax2.set_ylabel('Steepness\n(5yr−0.5yr %)', fontsize=8); ax2.set_xlabel('Date', fontsize=10)
ax2.grid(alpha=0.3)
cursor = ax2.axvline(steep.index[0], color=TEXT_COL, linewidth=1.5)
fig.text(0.01, 0.005, SOURCE_NOTE, fontsize=7, color='#8b949e')

frames = []
for i, (d, row) in enumerate(q.iterrows()):
    r = row[mats].astype(float); ok = r.notna().values
    line.set_data(x[ok], r.values[ok])
    if i >= 4:
        p = q.iloc[i - 4][mats].astype(float); pk = p.notna().values
        ghost.set_data(x[pk], p.values[pk])
    date_txt.set_text(d.strftime('%b %Y'))
    info_txt.set_text(f"10yr {r['10.0']:.2f}%   |   5yr−0.5yr {row['Steepness']:+.2f}%"
                      if pd.notna(row['Steepness']) else f"10yr {r['10.0']:.2f}%")
    cursor.set_xdata([d, d])
    fig.canvas.draw()
    frames.append(Image.frombuffer('RGBA', fig.canvas.get_width_height(),
                                   fig.canvas.buffer_rgba()).convert('RGB'))
plt.close(fig)
print(f'Frames: {len(frames)} ({q.index[0]} -> {q.index[-1]})')

# ── 3. GIF (80 ms/frame, 3 s hold on latest) ────────────────────────────────
pal = frames[-1].quantize(colors=128, method=Image.MEDIANCUT)
gif = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
dur = [80] * len(gif); dur[-1] = 3000
gif[0].save(f'{OUT}/10_spot_curve_animation.gif', save_all=True, append_images=gif[1:],
            duration=dur, loop=0, optimize=True)

# ── 4. Interactive player: re-embed frames as 900x600 JPEG ──────────────────
b64 = []
for f in frames:
    buf = io.BytesIO(); f.resize((900, 600), Image.LANCZOS).save(buf, 'JPEG', quality=75)
    b64.append(base64.b64encode(buf.getvalue()).decode())
html = open(OLD_PLAYER).read()
i = html.find('const frames = ['); j = html.find('];', i)
html = html[:i] + 'const frames = [' + ','.join(f'"{s}"' for s in b64) + html[j:]
n = len(b64)
html = re.sub(r'(id="scrubber" min="0" max=")\d+(")', rf'\g<1>{n-1}\2', html)
html = re.sub(r'Frame 1 / \d+', f'Frame 1 / {n}', html)
html = html.replace('Source: Bank of England Archive yield curve data', SOURCE_NOTE)
open(f'{OUT}/yield_curve_player.html', 'w').write(html)
print('Done')
