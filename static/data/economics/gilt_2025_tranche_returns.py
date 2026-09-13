import pandas as pd
from datetime import date

path = "/root/.claude/uploads/613ddfee-fe83-5cd6-bcc0-dc2a2da26884/1de96fd0-1789288343605_20260913_-_Gilt_Issuance_History.xls"
df = pd.read_excel(path, header=4)
mask = df.apply(lambda row: row.astype(str).str.contains("GB00BPCJD880").any(), axis=1)
sub = df[mask].copy()
sub.columns = [c.strip() for c in sub.columns]
print(sub)

MATURITY = date(2025,10,22)
COUPON = 3.5/2  # per 100 nominal, semi-annual

def coupons_between(issue_dt, maturity=MATURITY):
    # coupon dates 22 Apr / 22 Oct; count coupons strictly after issue_dt up to and incl maturity
    d = issue_dt
    # find first coupon date > issue_dt
    dates = []
    y = d.year
    for cand_year in range(y, maturity.year+1):
        for md in [(4,22),(10,22)]:
            cd = date(cand_year, md[0], md[1])
            if cd > issue_dt and cd <= maturity:
                dates.append(cd)
    return sorted(set(dates))

# CPI index (all items, 2015=100), ONS, month of issue -> maturity (Oct 2025 = 139.8)
CPI = {
    (2023,1): 126.4,
    (2023,3): 128.9,
    (2023,5): 131.3,
    (2023,6): 131.5,
    (2023,7): 130.9,
    (2023,8): 131.3,
    (2023,10): 132.0,
    (2023,11): 131.7,
    (2024,7): 133.8,
}
CPI_MATURITY = 139.8  # Oct 2025

rows = []
for _, r in sub.iterrows():
    issue_dt = r['Issue Date'].date() if hasattr(r['Issue Date'],'date') else r['Issue Date']
    price = r['Clean Price \nat Issue \n(£)']
    yld = r['Yield at Issue (%)']
    nominal = r['Nominal Amount Issued (£ million)']
    if pd.isna(price):
        continue
    cdates = coupons_between(issue_dt)
    n_coupons = len(cdates)
    interest = n_coupons * COUPON
    capital = 100 - price
    capital_pct = capital/price*100
    interest_pct = interest/price*100
    total_pct = capital_pct + interest_pct
    key = (issue_dt.year, issue_dt.month)
    cpi0 = CPI.get(key)
    real_pct = None
    if cpi0:
        real_pct = ((1+total_pct/100) / (CPI_MATURITY/cpi0) - 1) * 100
    hold_years = (MATURITY - issue_dt).days/365.0
    rows.append(dict(issue_date=issue_dt, price=price, yield_at_issue=yld, nominal_m=nominal,
                      n_coupons=n_coupons, capital_pct=capital_pct, interest_pct=interest_pct,
                      total_pct=total_pct, cpi0=cpi0, real_pct=real_pct, hold_years=hold_years))

res = pd.DataFrame(rows)
pd.set_option('display.width', 200)
print(res.to_string(index=False))

# weighted average by nominal amount
w = res['nominal_m']
def wavg(col):
    return (res[col]*w).sum()/w.sum()

print("\nWeighted averages (by nominal issued):")
for c in ['price','yield_at_issue','capital_pct','interest_pct','total_pct','real_pct','hold_years']:
    print(c, round(wavg(c),3))

res['ann_nominal_pct'] = ((1+res['total_pct']/100)**(1/res['hold_years']) - 1) * 100
res['ann_real_pct'] = ((1+res['real_pct']/100)**(1/res['hold_years']) - 1) * 100
print("\nWith annualized:")
print(res[['issue_date','yield_at_issue','price','hold_years','total_pct','ann_nominal_pct','real_pct','ann_real_pct']].to_string(index=False))
res.to_csv('/tmp/claude-0/-home-claude/613ddfee-fe83-5cd6-bcc0-dc2a2da26884/scratchpad/gilt/tranche_res.csv', index=False)
