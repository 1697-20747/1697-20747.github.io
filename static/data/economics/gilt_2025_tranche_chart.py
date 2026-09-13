import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = "/tmp/claude-0/-home-claude/613ddfee-fe83-5cd6-bcc0-dc2a2da26884/scratchpad/gilt/out"

DARK_BG   = '#0d1117'
DARK_AXES = '#161b22'
GRID_COL  = '#30363d'
TEXT_COL  = '#e6edf3'
ACCENT    = '#58a6ff'
ACCENT2   = '#f78166'
ACCENT3   = '#3fb950'
ACCENT4   = '#d2a8ff'
ACCENT5   = '#ffa657'
MUTED     = '#8b949e'

plt.rcParams.update({
    'figure.facecolor':  DARK_BG,
    'axes.facecolor':    DARK_AXES,
    'axes.edgecolor':    GRID_COL,
    'axes.labelcolor':   TEXT_COL,
    'axes.titlecolor':   TEXT_COL,
    'xtick.color':       TEXT_COL,
    'ytick.color':       TEXT_COL,
    'text.color':        TEXT_COL,
    'grid.color':        GRID_COL,
    'grid.linestyle':    '--',
    'grid.alpha':        0.5,
    'legend.facecolor':  DARK_AXES,
    'legend.edgecolor':  GRID_COL,
    'legend.labelcolor': TEXT_COL,
    'font.family':       'DejaVu Sans',
    'font.size':         10,
})

def add_source(fig, note):
    fig.text(0.01, 0.005, note, fontsize=7, color=MUTED, ha='left', va='bottom')

res = pd.read_csv('/tmp/claude-0/-home-claude/613ddfee-fe83-5cd6-bcc0-dc2a2da26884/scratchpad/gilt/tranche_res.csv', parse_dates=['issue_date'])
res = res.sort_values('issue_date').reset_index(drop=True)

labels = [f"{d.strftime('%-d %b %y')}\n{y:.2f}%" for d, y in zip(res['issue_date'], res['yield_at_issue'])]
x = np.arange(len(res))

fig, ax = plt.subplots(figsize=(13, 8))

b1 = ax.bar(x, res['capital_pct'], color=ACCENT, width=0.55, label='Capital return (price → par)', zorder=3)
b2 = ax.bar(x, res['interest_pct'], bottom=res['capital_pct'], color=ACCENT5, width=0.55, label='Interest received (coupons)', zorder=3)

for xi, tot in zip(x, res['total_pct']):
    ax.annotate(f'{tot:.1f}%', (xi, tot), textcoords="offset points", xytext=(0, 5),
                ha='center', fontsize=9.5, fontweight='bold', color=TEXT_COL)

d = ax.scatter(x, res['real_pct'], color=ACCENT4, s=90, zorder=6, edgecolor=DARK_BG, linewidth=1.0,
               marker='D', label='Real total return (CPI-deflated from issue month)')
for xi, r in zip(x, res['real_pct']):
    ax.annotate(f'{r:.1f}%', (xi, r), textcoords="offset points", xytext=(0, -16),
                ha='center', fontsize=8.7, color=ACCENT4, fontweight='bold')

ax.axhline(0, color=GRID_COL, linewidth=1)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=9)
ax.set_xlabel('Tranche issue date and yield at issue', fontsize=11)
ax.set_ylabel('Cumulative return to redemption, per £100 nominal (%)', fontsize=11)
ax.set_title('One Gilt, Eight Entry Points — 3½% Treasury Gilt 2025 (GB00BPCJD880)\nRealised nominal return (capital + interest) vs. CPI-real return, by issuance tranche, to redemption at par 22 Oct 2025',
             fontsize=12.3, fontweight='bold', pad=14)
ax.legend(loc='upper right', fontsize=9)
ax.grid(axis='y', alpha=0.35)
ax.set_ylim(-1, 17)

note = ("Note: every tranche of this gilt redeemed at the same £100 par on the same date (22 Oct 2025) and paid the same\n"
        "3.50% coupon — the only thing that varied was the price/yield at issue during 2023's rate volatility. Capital\n"
        "return = (100 − issue price)/issue price; interest = coupons actually paid from issue to redemption, simply\n"
        "summed (no reinvestment); real return deflates nominal total return by ONS CPI (all items, 2015=100) from the\n"
        "tranche's own issue month to Oct 2025 (139.8). Final £365m Jul-2024 tap (no separately published price) excluded.")
ax.text(0.012, 0.985, note, transform=ax.transAxes, fontsize=7.4, color=MUTED,
        va='top', ha='left', bbox=dict(boxstyle='round,pad=0.45', facecolor=DARK_AXES, edgecolor=GRID_COL, alpha=0.92))

add_source(fig, 'Source: UK DMO Gilt Issuance History (report D2.1E), data as of 13 Sep 2026; ONS CPI index (series D7BT).')
fig.tight_layout(rect=[0, 0.02, 1, 1])
fig.savefig(f'{OUT}/fiscal-outlook-2025-gilt-tranche-returns.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
plt.close(fig)
print("saved tranche returns chart")
