"""
Bank of England Archive Yield Curve Data - Full Statistical Analysis
Source: Bank of England Archive yield curve data
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ── Dark mode theme ────────────────────────────────────────────────────────────
DARK_BG   = '#0d1117'
DARK_AXES = '#161b22'
GRID_COL  = '#30363d'
TEXT_COL  = '#e6edf3'
ACCENT    = '#58a6ff'
ACCENT2   = '#f78166'
ACCENT3   = '#3fb950'
ACCENT4   = '#d2a8ff'
ACCENT5   = '#ffa657'

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

SOURCE_NOTE = 'Source: Bank of England Archive yield curve data'

FILES = [
    '/mnt/user-data/uploads/GLC_Nominal_month_end_data_1970_to_2015.xlsx',
    '/mnt/user-data/uploads/GLC_Nominal_month_end_data_2016_to_2024.xlsx',
    '/mnt/user-data/uploads/GLC_Nominal_month_end_data_2025_to_present.xlsx',
]

OUT = '/mnt/user-data/outputs'


# ── 1. Load & merge spot curve data ───────────────────────────────────────────
def load_spot_curve(path):
    raw = pd.read_excel(path, sheet_name='4. spot curve', header=None)
    mat_row = raw[raw.iloc[:, 0] == 'years:'].index[0]
    maturities = raw.iloc[mat_row, 1:].dropna().astype(float).tolist()
    data_start = mat_row + 2          # skip blank row after header
    df = raw.iloc[data_start:, :len(maturities)+1].copy()
    df.columns = ['Date'] + maturities
    df = df.dropna(subset=['Date'])
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    df = df.apply(pd.to_numeric, errors='coerce')
    return df

frames = [load_spot_curve(f) for f in FILES]
# Align columns – use union then sort
all_mats = sorted(set().union(*[set(f.columns) for f in frames]))
spot = pd.concat([f.reindex(columns=all_mats) for f in frames])
spot = spot.sort_index()
spot = spot[~spot.index.duplicated(keep='last')]

# Rename columns to year labels
spot.columns = [float(c) for c in spot.columns]

print(f"Spot curve shape: {spot.shape}  |  {spot.index[0].date()} → {spot.index[-1].date()}")

# ── 2. Steepness (5yr − 0.5yr) ────────────────────────────────────────────────
spot['Steepness'] = spot[5.0] - spot[0.5]

# ── 3. Save master CSV ────────────────────────────────────────────────────────
csv_path = f'{OUT}/BoE_Spot_Curve_Master.csv'
spot.index.name = 'Date'
spot.to_csv(csv_path)
print(f"CSV saved: {csv_path}")

# ── Helper ────────────────────────────────────────────────────────────────────
def add_source(ax, note=SOURCE_NOTE):
    ax.figure.text(0.01, 0.005, note, fontsize=7, color='#8b949e', ha='left', va='bottom')

def stat_table(series, name):
    s = series.dropna()
    return {
        'Series': name,
        'Count': len(s),
        'Mean': s.mean(),
        'Median': s.median(),
        'Std Dev': s.std(),
        'Min': s.min(),
        '5th Pct': s.quantile(0.05),
        '25th Pct': s.quantile(0.25),
        '75th Pct': s.quantile(0.75),
        '95th Pct': s.quantile(0.95),
        'Max': s.max(),
        'Skewness': s.skew(),
        'Kurtosis': s.kurt(),
    }

# Series of interest
KEY_MATS = [0.5, 1.0, 5.0, 10.0, 30.0]
SERIES_COLORS = {0.5: ACCENT, 1.0: ACCENT3, 5.0: ACCENT5, 10.0: ACCENT2, 30.0: ACCENT4, 'Steepness': '#ff79c6'}

# ── 4. Box-plots (key maturities + steepness) ─────────────────────────────────
def make_boxplots():
    series_keys = KEY_MATS + ['Steepness']
    labels = ['0.5yr', '1yr', '5yr', '10yr', '30yr', 'Steepness\n(5yr−0.5yr)']
    data = [spot[k].dropna().values for k in series_keys]
    colors = [SERIES_COLORS[k] for k in series_keys]

    fig, ax = plt.subplots(figsize=(13, 7))
    bp = ax.boxplot(data, patch_artist=True, widths=0.55,
                    medianprops=dict(color='white', linewidth=2),
                    whiskerprops=dict(color=GRID_COL, linewidth=1.5),
                    capprops=dict(color=GRID_COL, linewidth=1.5),
                    flierprops=dict(marker='.', markersize=2, alpha=0.3))
    for patch, c in zip(bp['boxes'], colors):
        patch.set_facecolor(c)
        patch.set_alpha(0.7)
        patch.set_edgecolor(c)

    ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylabel('Yield / Spread (%)', fontsize=11)
    ax.set_title('UK Nominal Spot Curve — Box Plots\n(0.5yr, 1yr, 5yr, 10yr, 30yr + Steepness)',
                 fontsize=13, fontweight='bold', pad=15)
    ax.axhline(0, color=GRID_COL, linewidth=1, linestyle='--')
    ax.grid(axis='y', alpha=0.4)
    add_source(ax)
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    fig.savefig(f'{OUT}/01_boxplots.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close(fig)
    print("Saved: 01_boxplots.png")

make_boxplots()


# ── 5. Histograms per key series ──────────────────────────────────────────────
def make_histograms():
    series_keys = KEY_MATS + ['Steepness']
    labels = ['0.5yr', '1yr', '5yr', '10yr', '30yr', 'Steepness (5yr−0.5yr)']

    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    axes = axes.flatten()

    for i, (k, lbl) in enumerate(zip(series_keys, labels)):
        ax = axes[i]
        s = spot[k].dropna()
        c = SERIES_COLORS[k]
        ax.hist(s, bins=60, color=c, alpha=0.75, edgecolor='none')
        ax.axvline(s.mean(), color='white', linewidth=1.5, linestyle='--', label=f'Mean: {s.mean():.2f}%')
        ax.axvline(s.median(), color=ACCENT3, linewidth=1.5, linestyle=':', label=f'Median: {s.median():.2f}%')
        ax.set_title(lbl, fontsize=11, fontweight='bold')
        ax.set_xlabel('Yield (%)', fontsize=9)
        ax.set_ylabel('Frequency', fontsize=9)
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)
        add_source(ax)

    fig.suptitle('UK Nominal Spot Curve — Histograms', fontsize=14, fontweight='bold', y=1.01)
    fig.tight_layout()
    fig.savefig(f'{OUT}/02_histograms.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close(fig)
    print("Saved: 02_histograms.png")

make_histograms()


# ── 5b. Standalone Steepness histogram ────────────────────────────────────────
def make_steepness_histogram():
    s = spot['Steepness'].dropna()
    fig, ax = plt.subplots(figsize=(10, 6))
    n, bins, patches = ax.hist(s, bins=70, color='#ff79c6', alpha=0.75, edgecolor='none')
    # colour bars by sign
    for patch, left in zip(patches, bins[:-1]):
        patch.set_facecolor(ACCENT3 if left >= 0 else ACCENT2)
        patch.set_alpha(0.75)
    ax.axvline(0, color='white', linewidth=1.5, linestyle='-', label='Zero')
    ax.axvline(s.mean(), color=ACCENT, linewidth=2, linestyle='--', label=f'Mean: {s.mean():.2f}%')
    ax.axvline(s.median(), color=ACCENT5, linewidth=2, linestyle=':', label=f'Median: {s.median():.2f}%')
    ax.set_title('Steepness Histogram (5yr − 0.5yr Spot Yield)\nGreen = Normal / Upward Sloping   |   Red = Inverted',
                 fontsize=12, fontweight='bold', pad=12)
    ax.set_xlabel('Spread (%)', fontsize=11)
    ax.set_ylabel('Frequency', fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    add_source(ax)
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    fig.savefig(f'{OUT}/03_steepness_histogram.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close(fig)
    print("Saved: 03_steepness_histogram.png")

make_steepness_histogram()


# ── 6. Time series for key maturities ────────────────────────────────────────
def make_time_series():
    fig, ax = plt.subplots(figsize=(16, 7))
    for k in KEY_MATS:
        if k in spot.columns:
            s = spot[k].dropna()
            ax.plot(s.index, s.values, linewidth=1, color=SERIES_COLORS[k], label=f'{k}yr', alpha=0.85)
    ax.set_title('UK Nominal Spot Yields — Key Maturities (Time Series)', fontsize=13, fontweight='bold')
    ax.set_xlabel('Date', fontsize=11)
    ax.set_ylabel('Yield (%)', fontsize=11)
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(alpha=0.4)
    add_source(ax)
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    fig.savefig(f'{OUT}/04_time_series.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close(fig)
    print("Saved: 04_time_series.png")

make_time_series()


# ── 7. Steepness time series ──────────────────────────────────────────────────
def make_steepness_ts():
    s = spot['Steepness'].dropna()
    fig, ax = plt.subplots(figsize=(16, 5))
    ax.fill_between(s.index, s.values, 0,
                    where=(s.values >= 0), color=ACCENT3, alpha=0.35, label='Normal (5yr > 0.5yr)')
    ax.fill_between(s.index, s.values, 0,
                    where=(s.values < 0), color=ACCENT2, alpha=0.35, label='Inverted (0.5yr > 5yr)')
    ax.plot(s.index, s.values, linewidth=0.8, color='#ff79c6', alpha=0.9)
    ax.axhline(0, color='white', linewidth=1, linestyle='--')
    ax.set_title('Yield Curve Steepness Over Time (5yr − 0.5yr Spot Yield)', fontsize=13, fontweight='bold')
    ax.set_xlabel('Date', fontsize=11)
    ax.set_ylabel('Spread (%)', fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.4)
    add_source(ax)
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    fig.savefig(f'{OUT}/05_steepness_time_series.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close(fig)
    print("Saved: 05_steepness_time_series.png")

make_steepness_ts()


# ── 8. Correlation heatmap ────────────────────────────────────────────────────
def make_heatmap():
    cols = [c for c in KEY_MATS if c in spot.columns] + ['Steepness']
    corr = spot[cols].corr()
    labels = [f'{c}yr' if c != 'Steepness' else 'Steep.' for c in cols]

    fig, ax = plt.subplots(figsize=(8, 7))
    cmap = plt.cm.RdYlGn
    im = ax.imshow(corr.values, cmap=cmap, vmin=-1, vmax=1, aspect='auto')
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=10)
    ax.set_yticklabels(labels, fontsize=10)
    for i in range(len(cols)):
        for j in range(len(cols)):
            ax.text(j, i, f'{corr.values[i,j]:.2f}', ha='center', va='center',
                    fontsize=9, color='black' if abs(corr.values[i,j]) > 0.5 else TEXT_COL)
    plt.colorbar(im, ax=ax, label='Correlation')
    ax.set_title('Correlation Matrix — Spot Yields & Steepness', fontsize=12, fontweight='bold', pad=12)
    add_source(ax)
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    fig.savefig(f'{OUT}/06_correlation_heatmap.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close(fig)
    print("Saved: 06_correlation_heatmap.png")

make_heatmap()


# ── 9. Rolling 12m std dev (volatility) ──────────────────────────────────────
def make_rolling_vol():
    fig, ax = plt.subplots(figsize=(16, 6))
    for k in KEY_MATS:
        if k in spot.columns:
            rv = spot[k].dropna().rolling(12).std()
            ax.plot(rv.index, rv.values, linewidth=1.2, color=SERIES_COLORS[k], label=f'{k}yr', alpha=0.85)
    ax.set_title('Rolling 12-Month Yield Volatility (Std Dev)', fontsize=13, fontweight='bold')
    ax.set_xlabel('Date', fontsize=11)
    ax.set_ylabel('Std Dev (%)', fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.4)
    add_source(ax)
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    fig.savefig(f'{OUT}/07_rolling_volatility.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close(fig)
    print("Saved: 07_rolling_volatility.png")

make_rolling_vol()


# ── 10. Percentile fan chart ──────────────────────────────────────────────────
def make_fan_chart():
    mat_cols = [c for c in spot.columns if c != 'Steepness' and pd.notna(c)]
    mat_cols_sorted = sorted(mat_cols)
    desc = spot[mat_cols_sorted].describe(percentiles=[.05, .25, .5, .75, .95])

    fig, ax = plt.subplots(figsize=(14, 7))
    xs = mat_cols_sorted
    ax.fill_between(xs, desc.loc['5%'], desc.loc['95%'], color=ACCENT, alpha=0.15, label='5th–95th pct')
    ax.fill_between(xs, desc.loc['25%'], desc.loc['75%'], color=ACCENT, alpha=0.3, label='25th–75th pct')
    ax.plot(xs, desc.loc['50%'], color=ACCENT, linewidth=2.5, label='Median', zorder=5)
    ax.plot(xs, desc.loc['mean'], color=ACCENT5, linewidth=2, linestyle='--', label='Mean', zorder=5)

    # Overlay selected snapshots
    snap_dates = ['1990-01-31', '2000-01-31', '2008-12-31', '2020-03-31']
    snap_colors = ['#ff79c6', '#f78166', '#ffa657', '#3fb950']
    for sd, sc in zip(snap_dates, snap_colors):
        try:
            row = spot[mat_cols_sorted].loc[spot.index.asof(pd.Timestamp(sd))].dropna()
            ax.plot(row.index, row.values, color=sc, linewidth=1.5, alpha=0.8, label=sd)
        except Exception:
            pass

    ax.set_title('UK Nominal Spot Curve — Percentile Fan Chart\n(with historical snapshots)', fontsize=13, fontweight='bold')
    ax.set_xlabel('Maturity (years)', fontsize=11)
    ax.set_ylabel('Yield (%)', fontsize=11)
    ax.legend(fontsize=9, loc='lower right')
    ax.grid(alpha=0.4)
    add_source(ax)
    fig.tight_layout(rect=[0, 0.02, 1, 1])
    fig.savefig(f'{OUT}/08_fan_chart.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close(fig)
    print("Saved: 08_fan_chart.png")

make_fan_chart()


# ── 11. Statistical summary table as figure ──────────────────────────────────
def make_stats_table():
    rows = [stat_table(spot[k], f'{k}yr' if k != 'Steepness' else 'Steepness') for k in KEY_MATS + ['Steepness'] if k in spot.columns]
    tdf = pd.DataFrame(rows).set_index('Series')
    num_cols = [c for c in tdf.columns if c != 'Count']
    tdf[num_cols] = tdf[num_cols].round(4)

    fig, ax = plt.subplots(figsize=(18, 4))
    ax.axis('off')
    cols = list(tdf.reset_index().columns)
    vals = tdf.reset_index().values.tolist()
    tbl = ax.table(cellText=vals, colLabels=cols, cellLoc='center', loc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8.5)
    tbl.scale(1, 2)
    for (r, c), cell in tbl.get_celld().items():
        if r == 0:
            cell.set_facecolor('#1f6feb')
            cell.set_text_props(color='white', fontweight='bold')
        elif r % 2 == 0:
            cell.set_facecolor('#21262d')
        else:
            cell.set_facecolor(DARK_AXES)
        cell.set_edgecolor(GRID_COL)
        cell.set_text_props(color=TEXT_COL)
    ax.set_title('Statistical Summary — UK Nominal Spot Yields', fontsize=12, fontweight='bold', pad=15, color=TEXT_COL)
    fig.text(0.01, 0.01, SOURCE_NOTE, fontsize=7, color='#8b949e')
    fig.tight_layout()
    fig.savefig(f'{OUT}/09_stats_table.png', dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close(fig)
    # Also save as CSV
    tdf.to_csv(f'{OUT}/BoE_Statistical_Summary.csv')
    print("Saved: 09_stats_table.png + BoE_Statistical_Summary.csv")

make_stats_table()


# ── 12. Yield curve snapshot animation ───────────────────────────────────────
def make_animation():
    mat_cols = sorted([c for c in spot.columns if c != 'Steepness' and pd.notna(c)])
    # sample every 3 months to keep file manageable
    quarterly = spot[mat_cols].resample('QS').last()
    quarterly = quarterly.dropna(how='all')
    dates = quarterly.index.tolist()

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_AXES)
    ax.set_xlim(min(mat_cols), max(mat_cols))

    all_vals = spot[mat_cols].values.flatten()
    ymin = np.nanpercentile(all_vals, 0.5) - 0.5
    ymax = np.nanpercentile(all_vals, 99.5) + 0.5
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel('Maturity (years)', fontsize=11)
    ax.set_ylabel('Yield (%)', fontsize=11)
    ax.grid(alpha=0.4)
    ax.axhline(0, color=GRID_COL, linewidth=0.8)

    year_min = dates[0].year
    year_max = dates[-1].year

    line, = ax.plot([], [], linewidth=2.5, color='#FFD700')
    fill = ax.fill_between([], [], [], alpha=0)
    date_txt = ax.text(0.02, 0.94, '', transform=ax.transAxes,
                       fontsize=13, color=TEXT_COL, fontweight='bold')
    ax.set_title('UK Nominal Spot Yield Curve — Historical Evolution', fontsize=13, fontweight='bold')
    fig.text(0.01, 0.005, SOURCE_NOTE, fontsize=7, color='#8b949e')

    def init():
        line.set_data([], [])
        date_txt.set_text('')
        return line, date_txt

    def update(frame_idx):
        d = dates[frame_idx]
        row = quarterly.loc[d, mat_cols].dropna()
        if len(row) < 3:
            return line, date_txt
        line.set_data(row.index, row.values)
        date_txt.set_text(d.strftime('%b %Y'))
        return line, date_txt

    ani = FuncAnimation(fig, update, frames=len(dates), init_func=init,
                        interval=80, blit=False)
    ani.save(f'{OUT}/10_spot_curve_animation.gif', writer=PillowWriter(fps=12),
             savefig_kwargs={'facecolor': DARK_BG})
    plt.close(fig)
    print("Saved: 10_spot_curve_animation.gif")

make_animation()

print("\n✅ All outputs saved to /mnt/user-data/outputs/")
