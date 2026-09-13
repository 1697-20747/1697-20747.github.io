import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq
from datetime import date

OUT = "/tmp/claude-0/-home-claude/613ddfee-fe83-5cd6-bcc0-dc2a2da26884/scratchpad/gilt/out"

# ── Dark mode theme, matching site convention (boe_yield_curve_analysis.py) ──
DARK_BG   = '#0d1117'
DARK_AXES = '#161b22'
GRID_COL  = '#30363d'
TEXT_COL  = '#e6edf3'
ACCENT    = '#58a6ff'   # blue
ACCENT2   = '#f78166'   # orange
ACCENT3   = '#3fb950'   # green
ACCENT4   = '#d2a8ff'   # purple
ACCENT5   = '#ffa657'   # amber
PINK      = '#ff79c6'
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

SOURCE_CURVE = 'Source: Trading Economics, UK benchmark gilt yields, 11 Sep 2026'
SOURCE_GILT  = 'Source: DMO auction/prospectus records (3¼% Treasury Gilt 2044); curve as above. Par-curve valuation is illustrative, not a trading price.'

# ── Curve data ────────────────────────────────────────────────────────────────
mats = np.array([1/12, 3/12, 6/12, 1, 2, 3, 5, 7, 10, 20, 30])
mat_labels = ['1M','3M','6M','1Y','2Y','3Y','5Y','7Y','10Y','20Y','30Y']
yld = np.array([3.85, 3.99, 4.24, 4.55, 4.70, 4.86, 4.90, 5.12, 5.35, 5.86, 5.91]) / 100.0

curve = PchipInterpolator(mats, yld, extrapolate=True)
def y(t):
    t = np.clip(t, mats[0], mats[-1])
    return curve(t)
def df(t):
    yt = y(t)
    return (1 + yt/2.0) ** (-2*t)

# ── Chart 1: current par yield curve + discount factor curve (two panels, one metric each) ──
def make_discount_curve():
    fine = np.linspace(1/12, 30, 400)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9), sharex=True,
                                    gridspec_kw={'height_ratios': [1.1, 1]})

    ax1.plot(fine, y(fine)*100, color=ACCENT, linewidth=2.2, zorder=5)
    ax1.scatter(mats, yld*100, color=ACCENT5, s=36, zorder=6, edgecolor=DARK_BG, linewidth=0.6,
                label='Benchmark gilt yields')
    for m, lbl, v in zip(mats, mat_labels, yld):
        if lbl in ('1Y','5Y','10Y','30Y'):
            ax1.annotate(f'{lbl}\n{v*100:.2f}%', (m, v*100), textcoords="offset points",
                         xytext=(0, 10), ha='center', fontsize=8.5, color=TEXT_COL)
    ax1.set_ylabel('Par yield (%)', fontsize=11)
    ax1.set_title('UK Gilt Curve, 11 September 2026 — Par Yields and Implied Discount Factors',
                   fontsize=13, fontweight='bold', pad=12)
    ax1.legend(loc='lower right', fontsize=9)
    ax1.grid(alpha=0.4)

    ax2.plot(fine, df(fine), color=ACCENT3, linewidth=2.2)
    ax2.fill_between(fine, df(fine), 0, color=ACCENT3, alpha=0.12)
    for m, lbl in zip(mats, mat_labels):
        if lbl in ('1Y','5Y','10Y','20Y','30Y'):
            ax2.annotate(f'{df(m):.3f}', (m, df(m)), textcoords="offset points",
                         xytext=(0, 8), ha='center', fontsize=8.5, color=TEXT_COL)
    ax2.set_ylabel('Discount factor', fontsize=11)
    ax2.set_xlabel('Maturity (years)', fontsize=11)
    ax2.set_ylim(0, 1.02)
    ax2.grid(alpha=0.4)

    add_source(fig, SOURCE_CURVE + ' — curve fitted by monotone (PCHIP) interpolation of benchmark par yields; treated as a proxy zero curve, a simplification flagged in the text.')
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    fig.savefig(f'{OUT}/fiscal-outlook-discount-curve.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close(fig)
    print("saved discount curve")

make_discount_curve()

# ── Gilt cash flows: 3.25% Treasury Gilt 2044 ──────────────────────────────────
valuation = date(2026, 9, 13)
def yearfrac(d0, d1):
    return (d1 - d0).days / 365.0

coupon_dates = []
d = date(2027, 1, 22)
while d <= date(2044, 1, 22):
    coupon_dates.append(d)
    m = d.month + 6
    yrr = d.year + (m-1)//12
    m = (m-1) % 12 + 1
    d = date(yrr, m, 22)

coupon = 3.25/2

def price_at_flat_yield(flat_y):
    p = 0.0
    for cd in coupon_dates:
        t = yearfrac(valuation, cd)
        cf = coupon + (100 if cd == coupon_dates[-1] else 0)
        p += cf * (1+flat_y/2)**(-2*t)
    return p

def curve_price():
    p = 0.0
    for cd in coupon_dates:
        t = yearfrac(valuation, cd)
        cf = coupon + (100 if cd == coupon_dates[-1] else 0)
        p += cf * df(t)
    return p

dirty_curve_price = curve_price()
last_coupon, next_coupon = date(2026,7,22), date(2027,1,22)
accrued = coupon * (valuation-last_coupon).days / (next_coupon-last_coupon).days
clean_curve_price = dirty_curve_price - accrued

ytm_curve = brentq(lambda yy: price_at_flat_yield(yy) - dirty_curve_price, 0.001, 0.20)
issue_yield = 0.03293
issue_price = 99.18

print(f"dirty curve price {dirty_curve_price:.2f} clean {clean_curve_price:.2f} flat-yield-equiv {ytm_curve*100:.3f}%")

# ── Chart 2: price/yield zoom 3%-7% for the 2044 gilt ─────────────────────────
def make_price_zoom():
    ys = np.linspace(0.03, 0.07, 200)
    prices = np.array([price_at_flat_yield(yy) for yy in ys])

    fig, ax = plt.subplots(figsize=(12, 7.5))
    ax.plot(ys*100, prices, color=ACCENT4, linewidth=2.4, zorder=5,
            label='3¼% Treasury Gilt 2044 — price vs. flat yield')

    # par reference
    ax.axhline(100, color=GRID_COL, linewidth=1, linestyle=':')
    ax.text(7.0, 100, ' par', color=MUTED, fontsize=8, va='center', ha='left')

    # issuance point
    ax.scatter([issue_yield*100], [issue_price], color=ACCENT3, s=70, zorder=6, edgecolor=DARK_BG, linewidth=0.8)
    ax.annotate(f'2013 issue: {issue_yield*100:.2f}% yield\n£{issue_price:.2f}',
                (issue_yield*100, issue_price), textcoords="offset points", xytext=(10, 12),
                fontsize=9, color=ACCENT3, fontweight='bold')

    # current point
    ax.scatter([ytm_curve*100], [dirty_curve_price], color=ACCENT2, s=70, zorder=6, edgecolor=DARK_BG, linewidth=0.8)
    ax.annotate(f'Sep 2026, off current curve:\n{ytm_curve*100:.2f}% equiv. yield, £{clean_curve_price:.2f} clean',
                (ytm_curve*100, dirty_curve_price), textcoords="offset points", xytext=(-190, -40),
                fontsize=9, color=ACCENT2, fontweight='bold')

    ax.annotate('', xy=(ytm_curve*100, dirty_curve_price), xytext=(issue_yield*100, issue_price),
                arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.2, linestyle='--'))

    ax.set_xlim(3, 7)
    ax.set_xlabel('Flat yield (%)', fontsize=11)
    ax.set_ylabel('Price (per £100 nominal)', fontsize=11)
    ax.set_title('Price Impact of Rising Yields — 3¼% Treasury Gilt 2044 (17.4 yrs to maturity)\nZoomed to the 3.00%–7.00% yield range',
                 fontsize=13, fontweight='bold', pad=12)
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(alpha=0.4)

    add_source(fig, 'Source: author calculation — DMO auction record (2013 issue) and Trading Economics curve (2026), full cash-flow discounting, flat-yield price/yield curve for illustration.')
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    fig.savefig(f'{OUT}/fiscal-outlook-2044-gilt-repricing.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close(fig)
    print("saved price zoom")

make_price_zoom()

# ── Total return from a 2013 hold-to-today-then-sell, across the same yield range ──
issue_date = date(2013, 5, 16)

past_coupons = []
d = date(2013, 7, 22)
while d <= valuation:
    past_coupons.append(d)
    m = d.month + 6
    yrr = d.year + (m-1)//12
    m = (m-1) % 12 + 1
    d = date(yrr, m, 22)

total_coupons_received = coupon * len(past_coupons)
holding_years = (valuation - issue_date).days / 365.0
print(f"past coupons: {len(past_coupons)}, total coupon cash: {total_coupons_received:.3f}, holding years: {holding_years:.2f}")

def total_return_pct(sale_price_dirty):
    return (sale_price_dirty - issue_price + total_coupons_received) / issue_price * 100

def make_price_zoom_v2():
    ys = np.linspace(0.03, 0.07, 200)
    prices = np.array([price_at_flat_yield(yy) for yy in ys])
    tr = total_return_pct(prices)

    fig, ax = plt.subplots(figsize=(12, 7.8))
    ax2 = ax.twinx()

    l1, = ax.plot(ys*100, prices, color=ACCENT4, linewidth=2.4, zorder=5,
            label='Price (LH axis)')
    l2, = ax2.plot(ys*100, tr, color=ACCENT5, linewidth=2.0, linestyle='-.', zorder=4,
             label='Total return since 2013 purchase, incl. coupons (RH axis)')

    ax.axhline(100, color=GRID_COL, linewidth=1, linestyle=':')
    ax.text(6.97, 100.6, 'par', color=MUTED, fontsize=8, va='bottom', ha='right')

    ax.scatter([issue_yield*100], [issue_price], color=ACCENT3, s=70, zorder=6, edgecolor=DARK_BG, linewidth=0.8)
    ax.annotate(f'Issued 16 May 2013: {issue_yield*100:.2f}% yield\n£{issue_price:.2f}',
                (issue_yield*100, issue_price), textcoords="offset points", xytext=(10, 14),
                fontsize=9, color=ACCENT3, fontweight='bold')

    ax.scatter([ytm_curve*100], [dirty_curve_price], color=ACCENT2, s=70, zorder=6, edgecolor=DARK_BG, linewidth=0.8)
    ax.annotate(f'Sep 2026, off current curve:\n{ytm_curve*100:.2f}% equiv. yield, £{clean_curve_price:.2f} clean',
                (ytm_curve*100, dirty_curve_price), textcoords="offset points", xytext=(-195, -55),
                fontsize=9, color=ACCENT2, fontweight='bold')

    ax.annotate('', xy=(ytm_curve*100, dirty_curve_price), xytext=(issue_yield*100, issue_price),
                arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.2, linestyle='--'))

    cur_tr = total_return_pct(dirty_curve_price)
    ax2.scatter([ytm_curve*100], [cur_tr], color=ACCENT5, s=55, zorder=6, edgecolor=DARK_BG, linewidth=0.8, marker='D')
    ax2.annotate(f'{cur_tr:.0f}% total return\nif sold today', (ytm_curve*100, cur_tr),
                 textcoords="offset points", xytext=(14, -6), fontsize=8.7, color=ACCENT5, fontweight='bold')

    ax2.axhline(0, color=ACCENT5, linewidth=0.8, linestyle=':', alpha=0.5)

    ax.set_xlim(3, 7)
    ax.set_xlabel('Flat yield at sale (%)', fontsize=11)
    ax.set_ylabel('Price (per £100 nominal)', fontsize=11, color=ACCENT4)
    ax2.set_ylabel('Cumulative total return since 2013 purchase (%)', fontsize=11, color=ACCENT5)
    ax.tick_params(axis='y', colors=ACCENT4)
    ax2.tick_params(axis='y', colors=ACCENT5)
    ax2.spines['right'].set_color(ACCENT5)
    ax2.spines['left'].set_color(ACCENT4)
    ax.set_title('Price Impact of Rising Yields — 3¼% Treasury Gilt 2044, issued 16 May 2013 (17.4 yrs left to maturity)\nZoomed to the 3.00%–7.00% yield range, with total return if bought at issue and sold today',
                 fontsize=12.5, fontweight='bold', pad=12)

    lines = [l1, l2]
    ax.legend(lines, [ln.get_label() for ln in lines], loc='upper right', fontsize=8.8)
    ax.grid(alpha=0.3)

    note = ("Note: total return = (sale price − £99.18 purchase price + all coupons received 2013–26) / £99.18.\n"
            f"Assumes {len(past_coupons)} semi-annual coupons of £1.625 actually paid ({holding_years:.1f}-yr hold), simply summed —\n"
            "not reinvested, not compounded, no accrued-interest adjustment at purchase/sale. Sale price is\n"
            "this gilt's own price/flat-yield line above, i.e. this is one bond's realised return, not the curve.")
    ax.text(0.02, 0.03, note, transform=ax.transAxes, fontsize=7.6, color=MUTED,
            va='bottom', ha='left', bbox=dict(boxstyle='round,pad=0.4', facecolor=DARK_AXES, edgecolor=GRID_COL, alpha=0.9))

    add_source(fig, 'Source: author calculation — DMO auction record (2013 issue) and Trading Economics curve (2026), full cash-flow discounting.')
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    fig.savefig(f'{OUT}/fiscal-outlook-2044-gilt-repricing.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close(fig)
    print("saved price zoom v2 with total return")
    print(f"total return at current curve point: {cur_tr:.2f}%  annualized: {((1+cur_tr/100)**(1/holding_years)-1)*100:.2f}%")
    print(f"total return at 3.00% sale: {total_return_pct(price_at_flat_yield(0.03)):.2f}%")
    print(f"total return at 7.00% sale: {total_return_pct(price_at_flat_yield(0.07)):.2f}%")

make_price_zoom_v2()

# ── Add a note box to chart 1 as well ──
def make_discount_curve_v2():
    fine = np.linspace(1/12, 30, 400)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9.3), sharex=True,
                                    gridspec_kw={'height_ratios': [1.1, 1]})

    ax1.plot(fine, y(fine)*100, color=ACCENT, linewidth=2.2, zorder=5)
    ax1.scatter(mats, yld*100, color=ACCENT5, s=36, zorder=6, edgecolor=DARK_BG, linewidth=0.6,
                label='Benchmark gilt yields')
    for m, lbl, v in zip(mats, mat_labels, yld):
        if lbl in ('1Y','5Y','10Y','30Y'):
            ax1.annotate(f'{lbl}\n{v*100:.2f}%', (m, v*100), textcoords="offset points",
                         xytext=(0, 10), ha='center', fontsize=8.5, color=TEXT_COL)
    ax1.set_ylabel('Par yield (%)', fontsize=11)
    ax1.set_title('UK Gilt Curve, 11 September 2026 — Par Yields and Implied Discount Factors',
                   fontsize=13, fontweight='bold', pad=12)
    ax1.legend(loc='lower right', fontsize=9)
    ax1.grid(alpha=0.4)

    note1 = ("Note: par yields interpolated (monotone PCHIP) between the 11 benchmark points\n"
             "marked; used here as a proxy zero/discount curve (semi-annual compounding),\n"
             "not a bootstrapped zero curve — a simplification, see post text.")
    ax1.text(0.015, 0.97, note1, transform=ax1.transAxes, fontsize=7.6, color=MUTED,
             va='top', ha='left', bbox=dict(boxstyle='round,pad=0.4', facecolor=DARK_AXES, edgecolor=GRID_COL, alpha=0.9))

    ax2.plot(fine, df(fine), color=ACCENT3, linewidth=2.2)
    ax2.fill_between(fine, df(fine), 0, color=ACCENT3, alpha=0.12)
    for m, lbl in zip(mats, mat_labels):
        if lbl in ('1Y','5Y','10Y','20Y','30Y'):
            ax2.annotate(f'{df(m):.3f}', (m, df(m)), textcoords="offset points",
                         xytext=(0, 8), ha='center', fontsize=8.5, color=TEXT_COL)
    ax2.set_ylabel('Discount factor', fontsize=11)
    ax2.set_xlabel('Maturity (years)', fontsize=11)
    ax2.set_ylim(0, 1.02)
    ax2.grid(alpha=0.4)

    note2 = "Discount factor = price today of £1 received at that maturity = (1 + y/2)^(−2t)."
    ax2.text(0.015, 0.06, note2, transform=ax2.transAxes, fontsize=7.6, color=MUTED,
             va='bottom', ha='left', bbox=dict(boxstyle='round,pad=0.4', facecolor=DARK_AXES, edgecolor=GRID_COL, alpha=0.9))

    add_source(fig, SOURCE_CURVE + ' — curve fitted by monotone (PCHIP) interpolation of benchmark par yields; treated as a proxy zero curve, a simplification flagged in the text.')
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    fig.savefig(f'{OUT}/fiscal-outlook-discount-curve.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close(fig)
    print("saved discount curve v2 with notes")

make_discount_curve_v2()
