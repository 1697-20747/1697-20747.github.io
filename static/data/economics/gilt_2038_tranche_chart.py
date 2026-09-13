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

res = pd.read_csv('/tmp/claude-0/-home-claude/613ddfee-fe83-5cd6-bcc0-dc2a2da26884/scratchpad/gilt/tranche_2038_res.csv', parse_dates=['issue_date'])
res = res.sort_values('issue_date').reset_index(drop=True)

labels = [f"{d.strftime('%-d %b %y')}\n{y:.2f}%" for d, y in zip(res['issue_date'], res['yield_at_issue'])]
x = np.arange(len(res))
w = 0.36

fig, ax = plt.subplots(figsize=(14, 8.5))

b1 = ax.bar(x - w/2, res['capital_pct'], width=w, color=ACCENT2, zorder=3,
            label='Capital return (issue price → today’s market price)')
b2 = ax.bar(x + w/2, res['interest_pct'], width=w, color=ACCENT5, zorder=3,
            label='Interest received (coupons to date)')

for xi, cap in zip(x, res['capital_pct']):
    ax.annotate(f'{cap:+.1f}%', (xi - w/2, cap), textcoords="offset points",
                xytext=(0, 4 if cap >= 0 else -13), ha='center', fontsize=8.3, color=ACCENT2, fontweight='bold')
for xi, itr in zip(x, res['interest_pct']):
    ax.annotate(f'{itr:+.1f}%', (xi + w/2, itr), textcoords="offset points",
                xytext=(0, 4), ha='center', fontsize=8.3, color=ACCENT5, fontweight='bold')

tot = ax.scatter(x, res['total_pct'], color=TEXT_COL, s=64, zorder=6, marker='_', linewidths=3,
                  label='Total nominal return (capital + interest)')
d = ax.scatter(x, res['real_pct'], color=ACCENT4, s=90, zorder=6, edgecolor=DARK_BG, linewidth=1.0,
               marker='D', label='Real total return (CPI-deflated from issue month)')
for xi, r, t in zip(x, res['real_pct'], res['total_pct']):
    ax.annotate(f'{r:+.1f}%', (xi, r), textcoords="offset points", xytext=(16, -3),
                ha='left', fontsize=8.3, color=ACCENT4, fontweight='bold')
    ax.annotate(f'{t:+.1f}%', (xi, t), textcoords="offset points", xytext=(16, 3),
                ha='left', fontsize=8.3, color=TEXT_COL, fontweight='bold')

ax.axhline(0, color=TEXT_COL, linewidth=1.1, zorder=4)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=8.8)
ax.set_xlabel('Entry point: date and yield of each issuance tranche (1 syndication + 8 outright auctions)', fontsize=10.5)
ax.set_ylabel('Cumulative return if sold today, per £100 nominal (%)', fontsize=11)
ax.set_title('One Gilt, Nine Entry Points — 3¾% Treasury Gilt 2038 (GB00BQC4R999)\nSold today (13 Sep 2026) off the current curve, not held to maturity: capital vs. interest vs. CPI-real',
             fontsize=12.1, fontweight='bold', pad=14)
ax.legend(loc='upper right', fontsize=8.6, framealpha=0.95)
ax.grid(axis='y', alpha=0.35)
ax.set_xlim(-0.6, len(res) - 0.3)
ax.set_ylim(-17.5, 19)

note = ("Note: each labelled point is one \"entry point\" — a separate auction/syndication at which this gilt was issued (1 syndication\n"
        "+ 8 outright auctions, 9 Nov 2022–20 Nov 2024), each at its own price/yield. Still outstanding today (matures 29 Jan 2038,\n"
        "~11.4 yrs left) — unlike this post's earlier reference bond, which had already matured. “Sold today” means marked to\n"
        "market off the same curve as the chart above: £86.27 clean (5.37% flat-yield equivalent), down from issue prices of\n"
        "£88.56–£96.63. Capital return = (today's clean price − issue price)/issue price — negative for every tranche, since every\n"
        "one was issued at a lower yield than today's curve implies. Interest = coupons actually paid from issue to today, summed\n"
        "(no reinvestment). Real return deflates nominal total return by ONS CPI (all items, 2015=100) from the tranche's own\n"
        "issue month to Jun 2026 (142.5, latest published).")
ax.text(0.012, 0.015, note, transform=ax.transAxes, fontsize=7.3, color=MUTED,
        va='bottom', ha='left', bbox=dict(boxstyle='round,pad=0.45', facecolor=DARK_AXES, edgecolor=GRID_COL, alpha=0.92))

add_source(fig, 'Source: UK DMO Gilt Issuance History (report D2.1E); current curve as in the discount-curve chart above; ONS CPI index (series D7BT).')
fig.tight_layout(rect=[0, 0.02, 1, 1])
fig.savefig(f'{OUT}/fiscal-outlook-2038-gilt-tranche-returns.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
plt.close(fig)
print("saved 2038 tranche returns chart (grouped bars)")
