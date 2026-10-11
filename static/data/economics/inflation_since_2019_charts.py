"""
Charts + stats for content/blog/economics/twenty-letters.md
Data: uk_cpi_m4_monthly_1999-2026.csv (ONS D7BT/D7G7, BoE LPMAUYN/LPMVQJW).
Outputs (static/images/economics/):
  inflation-since-2019-cpi-vs-target.png
  inflation-m4-vs-cpi-2000-2026.png
Run: python3 static/data/economics/inflation_since_2019_charts.py
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_IMG = os.path.normpath(os.path.join(HERE, "../../images/economics"))
OUT = _REPO_IMG if os.path.isdir(_REPO_IMG) else HERE   # standalone copy: write PNGs next to the script
BG, AX, GRID, TXT, MUTED = "#0d1117", "#161b22", "#30363d", "#e6edf3", "#8b949e"
BLUE, ORANGE, GREEN, PURPLE, AMBER, PINK = "#58a6ff", "#f78166", "#3fb950", "#d2a8ff", "#ffa657", "#ff79c6"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": TXT, "axes.labelcolor": TXT,
                     "xtick.color": TXT, "ytick.color": TXT, "axes.edgecolor": GRID})

df = pd.read_csv(os.path.join(HERE, "uk_cpi_m4_monthly_1999-2026.csv"), comment="#")
df["date"] = pd.to_datetime(df["month"]) + pd.offsets.MonthEnd(0)
df = df.set_index("date")

# Governor -> Chancellor open letters (CPI >1pp from target), publication dates
LETTERS = pd.to_datetime([
    "2020-06-18", "2020-09-17", "2020-12-17", "2021-05-06", "2021-09-23", "2021-12-16",
    "2022-03-17", "2022-06-16", "2022-09-22", "2022-12-15", "2023-03-23", "2023-06-22",
    "2023-09-21", "2023-12-14", "2024-03-21", "2025-06-19", "2025-09-18", "2025-12-18",
    "2026-04-30", "2026-09-17"])

# ---------------- stats ----------------
s = df.loc["2019-12":"2026-08"]
base, end = s["cpi_index_d7bt"].iloc[0], s["cpi_index_d7bt"].iloc[-1]
months = len(s) - 1
yrs = months / 12
cum = end / base - 1
cagr = (end / base) ** (1 / yrs) - 1
path2 = base * 1.02 ** (np.arange(len(s)) / 12)
gap = end / path2[-1] - 1
avg2019 = df.loc["2019", "cpi_index_d7bt"].mean()
boe_cum = end / avg2019 - 1
yoy = s["cpi_12m_rate_d7g7"].iloc[1:]
pre = df.loc["2000-01":"2019-12", "cpi_12m_rate_d7g7"]
m = df.loc["2000-01":, ["m4_12m_growth_lpmvqjw", "cpi_12m_rate_d7g7"]]
lags = {L: round(m["m4_12m_growth_lpmvqjw"].shift(L).corr(m["cpi_12m_rate_d7g7"]), 3) for L in range(0, 37, 3)}
m4c = df.loc["2019-12":"2026-08", "m4_level_gbp_m_lpmauyn"]
m4g = df.loc["2020":, "m4_12m_growth_lpmvqjw"]
stats = {
    "months": months, "years": round(yrs, 3),
    "cum_dec19_aug26_pct": round(cum * 100, 2), "cagr_pct": round(cagr * 100, 2),
    "two_pct_path_cum_pct": round((path2[-1] / base - 1) * 100, 2),
    "price_level_gap_vs_2pct_pct": round(gap * 100, 2),
    "boe_style_2019avg_base": round(avg2019, 2), "boe_style_cum_pct": round(boe_cum * 100, 2),
    "boe_style_cagr_7y": round(((1 + boe_cum) ** (1 / 7) - 1) * 100, 2),
    "boe_style_cagr_7_67y": round(((1 + boe_cum) ** (1 / (7 + 8 / 12)) - 1) * 100, 2),
    "months_within_1_3": int(((yoy >= 1) & (yoy <= 3)).sum()),
    "months_above_3": int((yoy > 3).sum()), "months_below_1": int((yoy < 1).sum()),
    "months_at_or_below_2": int((yoy <= 2).sum()),
    "months_total": int(len(yoy)), "peak": (yoy.idxmax().strftime("%Y-%m"), yoy.max()),
    "mean_12m_rate": round(yoy.mean(), 2),
    "pre_2000_2019_mean": round(pre.mean(), 2),
    "pre_cagr_2000_2019": round(((df.loc["2019-12", "cpi_index_d7bt"].iloc[0] /
                                  df.loc["1999-12", "cpi_index_d7bt"].iloc[0]) ** (1 / 20) - 1) * 100, 2),
    "m4_lead_corr_by_months": lags,
    "m4_level_cum_dec19_aug26_pct": round((m4c.iloc[-1] / m4c.iloc[0] - 1) * 100, 2),
    "m4_peak_growth_since_2020": (m4g.idxmax().strftime("%Y-%m"), m4g.max()),
    "m4_trough_growth_since_2020": (m4g.idxmin().strftime("%Y-%m"), m4g.min()),
}
for k, v in stats.items():
    print(f"{k}: {v}")


def style(ax):
    ax.set_facecolor(AX)
    ax.grid(True, color=GRID, lw=0.6, alpha=0.8)
    for sp in ax.spines.values():
        sp.set_color(GRID)


# ---------------- chart 1: CPI vs target + compound path ----------------
fig, (a1, a2) = plt.subplots(2, 1, figsize=(12, 9), sharex=True, gridspec_kw={"height_ratios": [1, 1.1]})
fig.patch.set_facecolor(BG)
for a in (a1, a2):
    style(a)
a1.axhspan(1, 3, color=GREEN, alpha=0.10, lw=0, label="1–3% (no-letter band)")
a1.axhline(2, color=GREEN, lw=1.4, ls="--", label="2% target")
a1.plot(s.index, s["cpi_12m_rate_d7g7"], color=ORANGE, lw=2.2, label="CPI, 12-month rate (ONS D7G7)")
for i, d in enumerate(LETTERS):
    a1.axvline(d, color=PURPLE, lw=0.8, alpha=0.55, label="Governor's open letter (20)" if i == 0 else None)
pk = yoy.idxmax()
a1.annotate(f"Peak {yoy.max():.1f}%\nOct 2022", xy=(pk, yoy.max()), xytext=(pk + pd.Timedelta(days=200), 10.3),
            color=TXT, fontsize=9, arrowprops=dict(arrowstyle="->", color=MUTED))
a1.set_ylabel("% year on year")
a1.set_ylim(-0.5, 12)
a1.set_title("UK CPI inflation vs the 2% target, Dec 2019 – Aug 2026", color=TXT, fontsize=13, loc="left")
a1.legend(loc="upper left", fontsize=8.5, facecolor=AX, edgecolor=GRID, labelcolor=TXT)

lvl = s["cpi_index_d7bt"] / base * 100
p2 = path2 / base * 100
a2.plot(s.index, lvl, color=ORANGE, lw=2.2, label="Actual CPI price level (Dec 2019 = 100)")
a2.plot(s.index, p2, color=GREEN, lw=1.8, ls="--", label="Price level at 2% compound")
a2.fill_between(s.index, p2, lvl, where=lvl.values >= p2, color=ORANGE, alpha=0.15, lw=0)
a2.annotate(f"{lvl.iloc[-1]:.1f}", xy=(s.index[-1], lvl.iloc[-1]), xytext=(6, 0), textcoords="offset points",
            color=ORANGE, va="center", fontsize=9)
a2.annotate(f"{p2[-1]:.1f}", xy=(s.index[-1], p2[-1]), xytext=(6, 0), textcoords="offset points",
            color=GREEN, va="center", fontsize=9)
a2.set_ylabel("Index, Dec 2019 = 100")
r = a2.twinx()
run = np.array([(lvl.iloc[i] / 100) ** (12 / i) - 1 if i >= 12 else np.nan for i in range(len(lvl))]) * 100
r.plot(s.index, run, color=BLUE, lw=1.4, label="Annualised compound rate since Dec 2019 (rhs)")
r.axhline(2, color=GREEN, lw=0.8, ls=":")
r.set_ylabel("% a year, compounded", color=BLUE)
r.tick_params(axis="y", colors=BLUE)
r.set_ylim(0, 7)
for sp in r.spines.values():
    sp.set_color(GRID)
h1, l1 = a2.get_legend_handles_labels()
h2, l2 = r.get_legend_handles_labels()
a2.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8.5, facecolor=AX, edgecolor=GRID, labelcolor=TXT)
note = (f"Dec 2019 → Aug 2026 ({months} months): prices +{cum*100:.1f}%, {cagr*100:.2f}% a year compounded.\n"
        f"A 2% path implies +{(p2[-1]/100-1)*100:.1f}%. Price level now {gap*100:.1f}% above that path.\n"
        f"12-month rate inside 1–3% in {stats['months_within_1_3']} of {stats['months_total']} months.")
a2.text(0.985, 0.04, note, transform=a2.transAxes, ha="right", va="bottom", fontsize=8.5, color=MUTED,
        bbox=dict(facecolor=AX, edgecolor=GRID, boxstyle="round,pad=0.5"))
a2.xaxis.set_major_locator(mdates.YearLocator())
a2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
fig.text(0.01, 0.005, "Source: ONS CPI (D7BT, D7G7, MM23); Bank of England open letters. Chart: own calculation.",
         color=MUTED, fontsize=8)
fig.tight_layout(rect=(0, 0.02, 1, 1))
fig.savefig(os.path.join(OUT, "inflation-since-2019-cpi-vs-target.png"), dpi=150, facecolor=BG)

# ---------------- chart 2: M4 growth vs CPI, dual axis ----------------
d2 = df.loc["2000-01":]
fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor(BG)
style(ax)
ax.axhline(0, color=GRID, lw=1)
ax.plot(d2.index, d2["m4_12m_growth_lpmvqjw"], color=BLUE, lw=1.8,
        label="M4 broad money, 12-month growth (lhs, BoE LPMVQJW)")
ax.set_ylabel("M4 growth, % y/y", color=BLUE)
ax.tick_params(axis="y", colors=BLUE)
ax.set_ylim(-8, 22)
r = ax.twinx()
r.plot(d2.index, d2["cpi_12m_rate_d7g7"], color=ORANGE, lw=1.8, label="CPI inflation, 12-month rate (rhs, ONS D7G7)")
r.axhline(2, color=GREEN, lw=1.1, ls="--", label="2% CPI target (rhs)")
r.set_ylabel("CPI, % y/y", color=ORANGE)
r.tick_params(axis="y", colors=ORANGE)
r.set_ylim(-4, 12)
for sp in r.spines.values():
    sp.set_color(GRID)
for lbl, x0, x1 in [("GFC", "2008-09", "2009-06"), ("Covid QE", "2020-03", "2021-12")]:
    ax.axvspan(pd.Timestamp(x0), pd.Timestamp(x1), color=PURPLE, alpha=0.10, lw=0)
    ax.text(pd.Timestamp(x0), -7.4, " " + lbl, color=PURPLE, fontsize=8.5)
h1, l1 = ax.get_legend_handles_labels()
h2, l2 = r.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8.5, facecolor=AX, edgecolor=GRID, labelcolor=TXT)
ax.set_title("UK M4 broad money growth vs CPI inflation, Jan 2000 – Aug 2026", color=TXT, fontsize=13, loc="left")
best = max(lags, key=lags.get)
fig.text(0.99, 0.005,
         f"Corr(CPI, M4 growth {best} months earlier) = {lags[best]:.2f}; same-month = {lags[0]:.2f}. "
         "Full-sample correlation, not causation.", ha="right", color=MUTED, fontsize=8)
ax.xaxis.set_major_locator(mdates.YearLocator(2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
fig.text(0.01, 0.005, "Source: Bank of England IADB (LPMVQJW, M4 12-month growth, SA); ONS CPI D7G7.",
         color=MUTED, fontsize=8)
fig.tight_layout(rect=(0, 0.02, 1, 1))
fig.savefig(os.path.join(OUT, "inflation-m4-vs-cpi-2000-2026.png"), dpi=150, facecolor=BG)
print("saved to", OUT)
