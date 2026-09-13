import pandas as pd
import numpy as np
from scipy.interpolate import PchipInterpolator
from datetime import date

# same curve as chart 1
mats = np.array([1/12, 3/12, 6/12, 1, 2, 3, 5, 7, 10, 20, 30])
yld = np.array([3.85, 3.99, 4.24, 4.55, 4.70, 4.86, 4.90, 5.12, 5.35, 5.86, 5.91]) / 100.0
curve = PchipInterpolator(mats, yld, extrapolate=True)
def y(t):
    t = np.clip(t, mats[0], mats[-1])
    return curve(t)
def df(t):
    yt = y(t)
    return (1 + yt/2.0) ** (-2*t)

VALUATION = date(2026, 9, 13)
def yearfrac(d0, d1):
    return (d1 - d0).days / 365.0

MATURITY = date(2038, 1, 29)
COUPON = 3.75/2

# coupon dates from valuation forward to maturity: 29 Jan / 29 Jul
future_coupons = []
d = date(2027, 1, 29) if VALUATION < date(2026,7,29) else None
# find first coupon date after valuation
cands = []
y0 = VALUATION.year
for yy in range(y0, MATURITY.year+1):
    for md in [(1,29),(7,29)]:
        cd = date(yy, md[0], md[1])
        if cd > VALUATION and cd <= MATURITY:
            cands.append(cd)
future_coupons = sorted(set(cands))
print("first few future coupons:", future_coupons[:4], "... last:", future_coupons[-1], "count:", len(future_coupons))

price_today = 0.0
for cd in future_coupons:
    t = yearfrac(VALUATION, cd)
    cf = COUPON + (100 if cd == future_coupons[-1] else 0)
    price_today += cf * df(t)

# accrued interest since last coupon (29 Jul 2026) to valuation (13 Sep 2026)
last_c, next_c = date(2026,7,29), date(2027,1,29)
accrued = COUPON * (VALUATION-last_c).days/(next_c-last_c).days
clean_today = price_today - accrued
print(f"Dirty price today: {price_today:.3f}  Accrued: {accrued:.4f}  Clean: {clean_today:.3f}")
years_to_maturity = yearfrac(VALUATION, MATURITY)
print(f"years to maturity from today: {years_to_maturity:.2f}")

# now tranches
path = "/root/.claude/uploads/613ddfee-fe83-5cd6-bcc0-dc2a2da26884/1de96fd0-1789288343605_20260913_-_Gilt_Issuance_History.xls"
raw = pd.read_excel(path, header=4)
raw.columns = [c.strip() for c in raw.columns]
mask = raw.apply(lambda row: row.astype(str).str.contains("GB00BQC4R999").any(), axis=1)
sub = raw[mask].copy()

CPI = {
    (2022,11): 114.9,  # placeholder, will fetch
    (2023,3): 128.9,
    (2023,6): 131.5,
    (2023,7): 130.9,
    (2023,10): 132.0,
    (2024,1): 133.4,   # placeholder, will fetch
    (2024,6): 134.6,   # placeholder, will fetch
    (2024,8): 134.8,   # placeholder, will fetch
    (2024,11): 134.9,  # placeholder, will fetch
}
CPI_TODAY = 142.5  # Jun 2026, latest published

rows = []
for _, r in sub.iterrows():
    issue_dt = r['Issue Date'].date() if hasattr(r['Issue Date'],'date') else r['Issue Date']
    price = r['Clean Price \nat Issue \n(£)']
    yld_i = r['Yield at Issue (%)']
    nominal = r['Nominal Amount Issued (£ million)']
    if pd.isna(price):
        continue
    # coupons paid from issue to valuation date (already paid, realised interest)
    past = []
    for yy in range(issue_dt.year, VALUATION.year+1):
        for md in [(1,29),(7,29)]:
            cd = date(yy, md[0], md[1])
            if cd > issue_dt and cd <= VALUATION:
                past.append(cd)
    n_past = len(sorted(set(past)))
    interest = n_past * COUPON
    capital = clean_today - price
    capital_pct = capital/price*100
    interest_pct = interest/price*100
    total_pct = capital_pct + interest_pct
    hold_years = yearfrac(issue_dt, VALUATION)
    rows.append(dict(issue_date=issue_dt, price=price, yield_at_issue=yld_i, nominal_m=nominal,
                      n_coupons=n_past, capital_pct=capital_pct, interest_pct=interest_pct,
                      total_pct=total_pct, hold_years=hold_years))

res = pd.DataFrame(rows)
pd.set_option('display.width',200)
print(res.to_string(index=False))
res.to_csv('/tmp/claude-0/-home-claude/613ddfee-fe83-5cd6-bcc0-dc2a2da26884/scratchpad/gilt/tranche_2038_res.csv', index=False)
