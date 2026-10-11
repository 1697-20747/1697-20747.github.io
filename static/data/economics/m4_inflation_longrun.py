"""
Long-run M4 vs inflation analysis for content/blog/economics/twenty-letters.md
Data: uk_m4_cpi_gdp_quarterly_1963-2026.csv (BoE LPQAUYN/LPQVQJW; ONS D7G7, ABMI, YBHA).
RPI deliberately excluded. Pre-1989 inflation uses the implied GDP deflator (YBHA/ABMI).
Outputs (static/images/economics/):
  m4-longrun-growth-1964-2026.png
  m4-inflation-correlation-panel.png
Run: python3 static/data/economics/m4_inflation_longrun.py   (needs pandas, matplotlib, statsmodels)
"""
import os, io, contextlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import grangercausalitytests

HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_IMG = os.path.normpath(os.path.join(HERE, "../../images/economics"))
OUT = _REPO_IMG if os.path.isdir(_REPO_IMG) else HERE   # standalone copy: write PNGs next to the script
BG, AX, GRID, TXT, MUTED = "#0d1117", "#161b22", "#30363d", "#e6edf3", "#8b949e"
BLUE, ORANGE, GREEN, PURPLE, AMBER, PINK = "#58a6ff", "#f78166", "#3fb950", "#d2a8ff", "#ffa657", "#ff79c6"
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": TXT, "axes.labelcolor": TXT,
                     "xtick.color": TXT, "ytick.color": TXT, "axes.edgecolor": GRID})

d = pd.read_csv(os.path.join(HERE, "uk_m4_cpi_gdp_quarterly_1963-2026.csv"), comment="#", index_col=0)
d.index = pd.PeriodIndex(d.index, freq="Q")
d["defl"] = d.nominal_gdp_gbp_m / d.real_gdp_gbp_m
pct4 = lambda s: (s / s.shift(4) - 1) * 100
d["defl_yoy"] = pct4(d.defl)
d["rgdp_yoy"] = pct4(d.real_gdp_gbp_m)
d["ngdp_yoy"] = pct4(d.nominal_gdp_gbp_m)
d["excess"] = d.m4_yoy - d.rgdp_yoy          # money growth in excess of real output growth
d["vel_yoy"] = d.ngdp_yoy - d.m4_yoy         # implied velocity growth (identity)
d["yr"] = d.index.year
P = lambda a, b: d.loc[pd.Period(a, "Q"):pd.Period(b, "Q")]

# ---------------- stats ----------------
S = {}
w = P("1976Q3", "2026Q2")
S["50y_means_1976Q3_2026Q2"] = w[["m4_yoy", "rgdp_yoy", "defl_yoy", "ngdp_yoy", "vel_yoy"]].mean().round(2).to_dict()
ann = d.loc[[pd.Period(f"{y}Q2", "Q") for y in range(1977, 2027)], "m4_yoy"]
S["50y_m4_compound"] = round(((np.prod(1 + ann / 100)) ** (1 / len(ann)) - 1) * 100, 2)
S["neg_quarters_share_50y"] = f"{(w.m4_yoy < 0).sum()} of {len(w)}"
S["m4_mean_since_1992Q4"] = round(P("1992Q4", "2026Q2").m4_yoy.mean(), 2)
S["cpi_mean_since_1992Q4"] = round(P("1992Q4", "2026Q2").cpi_yoy.mean(), 2)

DEC = [("1960s*", 1964, 1969), ("1970s", 1970, 1979), ("1980s", 1980, 1989), ("1990s", 1990, 1999),
       ("2000s", 2000, 2009), ("2010s", 2010, 2019), ("2020–26", 2020, 2026)]
dec = pd.DataFrame({lab: d[(d.yr >= a) & (d.yr <= b)][["m4_yoy", "rgdp_yoy", "defl_yoy", "cpi_yoy", "vel_yoy"]].mean()
                    for lab, a, b in DEC}).T.round(1)
S["decade_means"] = dec.to_dict("index")


def xcorr(y, x, a, b, lags):
    s = P(a, b)
    return {k: s[y].corr(d[x].shift(k).loc[s.index]) for k in lags}


LAGS = range(-8, 17)
XC = {
    "CPI, 1989–2026": xcorr("cpi_yoy", "m4_yoy", "1989Q1", "2026Q2", LAGS),
    "CPI, 1989–2019 (pre-Covid)": xcorr("cpi_yoy", "m4_yoy", "1989Q1", "2019Q4", LAGS),
    "CPI, 1992–2007 (inflation targeting, pre-GFC)": xcorr("cpi_yoy", "m4_yoy", "1992Q4", "2007Q4", LAGS),
    "GDP deflator, 1966–2026": xcorr("defl_yoy", "m4_yoy", "1966Q1", "2026Q2", LAGS),
}
S["xcorr_peak"] = {k: (max(v, key=v.get), round(max(v.values()), 2), "lag0", round(v[0], 2)) for k, v in XC.items()}

# five-year non-overlapping blocks (complete blocks only)
d["blk"] = (d.yr - 1966) // 5
blk = d[(d.yr >= 1966) & (d.yr <= 2025)].groupby("blk").agg(
    start=("yr", "min"), m4=("m4_yoy", "mean"), ex=("excess", "mean"), defl=("defl_yoy", "mean"), cpi=("cpi_yoy", "mean"))
fit = sm.OLS(blk.defl, sm.add_constant(blk.ex)).fit()
S["5y_blocks"] = {"corr_m4_defl": round(blk.m4.corr(blk.defl), 2), "corr_excess_defl": round(blk.ex.corr(blk.defl), 2),
                  "slope": round(fit.params["ex"], 2), "r2": round(fit.rsquared, 2), "n": len(blk)}

# HAC regression: CPI on M4 growth 8 quarters earlier, 1989-2026
s = P("1989Q1", "2026Q2").copy()
s["m4_l8"] = d.m4_yoy.shift(8).loc[s.index]
reg = sm.OLS(s.cpi_yoy, sm.add_constant(s.m4_l8), missing="drop").fit(cov_type="HAC", cov_kwds={"maxlags": 8})
S["hac_cpi_on_m4_l8"] = {"beta": round(reg.params["m4_l8"], 3), "t": round(reg.tvalues["m4_l8"], 2), "r2": round(reg.rsquared, 2)}


def granger(cols, a, b, lags=(4, 8, 12)):
    with contextlib.redirect_stdout(io.StringIO()):
        r = grangercausalitytests(P(a, b)[cols].dropna(), maxlag=list(lags))
    return {k: round(v[0]["ssr_ftest"][1], 3) for k, v in r.items()}


S["granger_p_M4_to_CPI_1989_2026"] = granger(["cpi_yoy", "m4_yoy"], "1989Q1", "2026Q2")
S["granger_p_CPI_to_M4_1989_2026"] = granger(["m4_yoy", "cpi_yoy"], "1989Q1", "2026Q2")
S["granger_p_M4_to_deflator_1966_2026"] = granger(["defl_yoy", "m4_yoy"], "1966Q1", "2026Q2")
roll = d.cpi_yoy.rolling(40).corr(d.m4_yoy.shift(8))
S["rolling10y_corr_l8_min_max"] = (round(roll.min(), 2), str(roll.idxmin()), round(roll.max(), 2), str(roll.idxmax()))
for k, v in S.items():
    print(f"{k}: {v}")


def style(ax):
    ax.set_facecolor(AX)
    ax.grid(True, color=GRID, lw=0.6, alpha=0.8)
    for sp in ax.spines.values():
        sp.set_color(GRID)


def leg(ax, **kw):
    ax.legend(fontsize=8, facecolor=AX, edgecolor=GRID, labelcolor=TXT, **kw)


t = d.index.to_timestamp(how="end")

# ---------------- chart 1: long-run growth ----------------
fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor(BG)
style(ax)
m = d.yr >= 1964
ax.axhline(0, color=GRID, lw=1)
ax.plot(t[m], d.m4_yoy[m], color=BLUE, lw=1.9, label="M4 broad money, 12-month growth")
ax.plot(t[m], d.ngdp_yoy[m].clip(-12, 30), color=PURPLE, lw=1.1, alpha=0.8, label="Nominal GDP growth (2020–21 clipped)")
ax.plot(t[m], d.defl_yoy[m], color=AMBER, lw=1.2, alpha=0.9, label="GDP deflator inflation")
ax.plot(t[m], d.cpi_yoy[m], color=ORANGE, lw=1.8, label="CPI inflation (from 1989)")
avg = S["50y_means_1976Q3_2026Q2"]["m4_yoy"]
ax.axhline(avg, color=BLUE, lw=1, ls="--", alpha=0.8)
ax.text(pd.Timestamp("2010-06-30"), avg + 0.6, f"M4 50-year mean {avg:.1f}%", color=BLUE, fontsize=8.5)
ax.axhline(2, color=GREEN, lw=1, ls=":")
ax.text(t[m][0], 0.7, "2% target", color=GREEN, fontsize=8.5)
ax.set_ylim(-8, 30)
ax.set_ylabel("% year on year")
ax.set_title("UK M4 growth vs nominal GDP and inflation, 1964–2026", color=TXT, fontsize=13, loc="left")
leg(ax, loc="upper right")
note = (f"1976–2026 averages: M4 {avg:.1f}% = real GDP {S['50y_means_1976Q3_2026Q2']['rgdp_yoy']:.1f}% "
        f"+ deflator {S['50y_means_1976Q3_2026Q2']['defl_yoy']:.1f}% + falling velocity {-S['50y_means_1976Q3_2026Q2']['vel_yoy']:.1f}%.\n"
        f"M4 growth was negative in {S['neg_quarters_share_50y']} quarters, all in 2010–15 or 2023.")
ax.text(0.01, 0.03, note, transform=ax.transAxes, fontsize=8.5, color=MUTED,
        bbox=dict(facecolor=AX, edgecolor=GRID, boxstyle="round,pad=0.5"))
fig.text(0.01, 0.005, "Source: Bank of England IADB (LPQVQJW); ONS (D7G7, ABMI, YBHA). Deflator = YBHA/ABMI. Own calculation.",
         color=MUTED, fontsize=8)
fig.tight_layout(rect=(0, 0.02, 1, 1))
fig.savefig(os.path.join(OUT, "m4-longrun-growth-1964-2026.png"), dpi=150, facecolor=BG)

# ---------------- chart 2: 2x2 correlation panel ----------------
fig, axs = plt.subplots(2, 2, figsize=(13, 10))
fig.patch.set_facecolor(BG)
for a in axs.flat:
    style(a)

# (a) 5y blocks
a = axs[0, 0]
a.scatter(blk.ex, blk.defl, color=BLUE, s=40, zorder=3)
for _, r in blk.iterrows():
    off = {2001: (4, -11), 1996: (4, -11), 2016: (-46, 5)}.get(int(r.start), (4, 4))
    a.annotate(f"{int(r.start)}–{str(int(r.start) + 4)[2:]}", (r.ex, r.defl), xytext=off,
               textcoords="offset points", fontsize=7.5, color=TXT)
xx = np.linspace(blk.ex.min() - 1, blk.ex.max() + 1, 50)
a.plot(xx, fit.params["const"] + fit.params["ex"] * xx, color=ORANGE, lw=1.2,
       label=f"OLS: slope {fit.params['ex']:.2f}, R² {fit.rsquared:.2f}")
a.plot(xx, xx, color=MUTED, lw=0.8, ls=":", label="1:1 (strict quantity theory)")
a.set_xlabel("Excess money growth (M4 − real GDP), 5-yr avg, %")
a.set_ylabel("GDP deflator inflation, 5-yr avg, %")
a.set_title("(a) Five-year averages, 1966–2025", color=TXT, fontsize=11, loc="left")
leg(a, loc="upper left")

# (b) cross-correlation
a = axs[0, 1]
cols = [ORANGE, GREEN, PURPLE, AMBER]
for (lab, v), c in zip(XC.items(), cols):
    a.plot(list(v.keys()), list(v.values()), color=c, lw=1.6, marker="o", ms=3, label=lab)
a.axhline(0, color=GRID, lw=1)
a.axvline(0, color=MUTED, lw=0.8, ls=":")
a.set_xlabel("Quarters M4 growth leads inflation (negative = inflation leads M4)")
a.set_ylabel("Correlation")
a.set_title("(b) Cross-correlation by lead/lag", color=TXT, fontsize=11, loc="left")
a.set_ylim(-0.6, 1)
leg(a, loc="lower right")

# (c) rolling correlation
a = axs[1, 0]
rr = roll.dropna()
a.plot(rr.index.to_timestamp(how="end"), rr.values, color=BLUE, lw=1.6)
a.axhline(0, color=GRID, lw=1)
a.set_ylim(-1, 1)
a.set_ylabel("Correlation")
a.set_title("(c) Rolling 10-yr correlation: CPI vs M4 growth 8 quarters earlier", color=TXT, fontsize=11, loc="left")

# (d) decade decomposition, grouped bars (no stacking: velocity is negative)
a = axs[1, 1]
x = np.arange(len(dec))
wdt = 0.2
for i, (col, lab, c) in enumerate([("m4_yoy", "M4 growth", BLUE), ("rgdp_yoy", "Real GDP growth", GREEN),
                                   ("defl_yoy", "GDP deflator inflation", AMBER), ("vel_yoy", "Velocity change", PINK)]):
    a.bar(x + (i - 1.5) * wdt, dec[col], width=wdt, color=c, label=lab)
a.scatter(x + 0.5 * wdt, dec.cpi_yoy, marker="D", color=ORANGE, zorder=4, s=22, label="CPI inflation (from 1989)")
a.axhline(0, color=GRID, lw=1)
a.set_xticks(x)
a.set_xticklabels(dec.index, fontsize=8.5)
a.set_ylabel("% a year, decade average")
a.set_title("(d) M4 ≈ real growth + inflation − velocity change", color=TXT, fontsize=11, loc="left")
leg(a, loc="upper right")

fig.suptitle("Does M4 growth predict UK inflation?", color=TXT, fontsize=14, x=0.01, ha="left")
fig.text(0.01, 0.005, "Source: Bank of England IADB (LPQAUYN, LPQVQJW); ONS (D7G7, ABMI, YBHA). Quarterly data. "
         "*1960s = 1964–69. Own calculation.", color=MUTED, fontsize=8)
fig.tight_layout(rect=(0, 0.02, 1, 0.97))
fig.savefig(os.path.join(OUT, "m4-inflation-correlation-panel.png"), dpi=150, facecolor=BG)
print("saved to", OUT)
