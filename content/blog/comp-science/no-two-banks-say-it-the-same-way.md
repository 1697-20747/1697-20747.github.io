---
title: "No Two Banks Say It the Same Way"
date: 2026-09-28T09:00:00Z
draft: false
categories: ["comp-science"]
tags: [credit-risk, LLM, AI, agents, data-architecture, verification, banks, peer-comparison]
description: "The last ten banks through the verification pipeline, read log by log. Why pre-coded Python scraping failed, why checking every cell by hand is not feasible, what it costs in tokens to get a bank through the QA gate, and how the agent's harness evolves session by session. Agents are the only viable path to a curated credit metric database at scale, and without that data a peer credit comparison ranks definitions, not banks."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

*Eleventh post in a series about building a local, offline credit-analysis
pipeline — start with [Not a Specification](/blog/comp-science/not-a-specification/)
for the problem statement. The companion post
[Expensive On Purpose](/blog/comp-science/expensive-on-purpose/) covered what
agentic verification costs. This one covers why nothing cheaper worked.*

---

## Eight Years of a Number That Was Never There

UniCredit's annual reports carried a net interest margin in the project's
database for every year from 2018 to 2025. 1.92%, 1.43%, 0.77%, 0.75%,
4.66%, 0.83%, 0.89%, 0.53%. Each one had been extracted automatically,
passed a sanity-range check, and been promoted to `verified=1`.

None of them is a net interest margin. UniCredit's annual report never
discloses a headline NIM ratio, in any year. What the extractor had found
was the Part H related-party notes table, where Italian reporting
convention labels the net interest income line of the P&L "Net interest
margin", and a percentage column beside it shows how much of that line is
attributable to related parties. The keyword matched. The number sat
next to a `%` sign. It landed in a plausible range. Eight years running.

The FY2022 value (4.66) didn't even match that table. It came from
somewhere else again.

An agent found this on 27 September, not by being cleverer about regular
expressions, but by doing what the extractor never could: open each year's
report, look at the table the number came from, ask whether that table
is the kind of table a NIM lives in, and then search the whole document
to confirm no real NIM ratio exists anywhere. All eight rows were
retracted to an explicit, documented "not disclosed", and the pattern was
logged as a recurring bug (`architecture_feedback` #170) because the same
terminology will turn up in other Italian and EU filers.

That one example contains most of this post's argument. The failure was
not a bad regex. It was a correct regex applied to data that does not
mean what its label says.

## The Last Ten Banks

The project's verification database now covers 60 banks and 814 filings;
57 banks are closed out. Each agentic session writes a machine-readable
audit log. I went back through the logs for the ten most recent banks —
Webster Financial, UniCredit, U.S. Bancorp, TD Bank, Synchrony Financial,
State Street, Société Générale, SMFG, Scotiabank and Santander — looking
for one thing: cases where the difficulty came from the data rather than
the software.

Almost every case fit. They fall into six shapes.

### 1. The label is right, the concept is wrong

**UniCredit NIM**, above. **Société Générale's cost of risk** is a quieter
version. Each year's report states the Group commercial cost of risk
first, then gives the French Retail Banking segment figure in a bullet
directly below. The extractor took the segment figure in three separate
years: stored 56bp against a Group figure of 61bp for FY2014, 36 against
37 for FY2016, 30 against 19 for FY2017. Same words, same paragraph, and
a different perimeter of the bank.

**Santander's NPL coverage** is the case where both numbers are real. The
annual report's "Total coverage ratio" runs 24–32 percentage points above
the coverage ratio derived from the Pillar 3 CR1 template for the same
year: 71% against 38.8% for FY2021. Neither is an extraction error. They
are two distinct concepts sharing a name, and one database key cannot hold
both without a documented decision about which one it means.

### 2. The same bank, two different scopes

**UniCredit's gross loans** show a large, consistent gap between the
annual report and Pillar 3 in several years. Again, both are correctly
transcribed: the annual report gives balance-sheet loans to *customers*,
while Pillar 3's Basel CR1 template gives loans and advances to banks
*and* customers. The loan-to-deposit ratio derived from each inherits the
gap. The same pattern had already appeared at Santander and Royal Bank of
Canada.

**Webster Financial's loan-to-deposit ratio** is disclosed only at the
level of Webster Bank, the insured subsidiary, not the holding company.
For a US bank holding company that's structural, since deposits sit only
in the depository subsidiary, but it has to be recorded as such, because
this project scopes everything to group-consolidated level
([Whose Bank Is This?](/blog/comp-science/whose-bank-is-this/) explains
why).

**TD Bank's NPL coverage** for FY2016–17 was deliberately left empty. A
ratio could have been computed from the allowance-movement table and the
gross-impaired-loans table. One of them includes debt securities
classified as loans and acquired FDIC loans; the other explicitly excludes
both. Dividing them would produce a clean-looking number with no meaning.
The agent recorded a confirmed gap instead.

### 3. The right number, the wrong date

**TD Bank's Domestic Stability Buffer** rose from 3.0% to 3.5% on
1 November 2023. TD's fiscal year ends on 31 October. An earlier session
had applied the new rate to FY2023, with a note admitting it was a
time-budget shortcut. It was one day wrong, and the one day matters: the
FY2023 combined buffer is 6.5%, not 7.0%. The correction was
cross-validated against an already-verified 11.0% regulatory minimum
(4.5 + 6.5), which the wrong figure would have broken.

**Société Générale's FY2021 Pillar 2 requirement** was taken from a
table whose columns are dated 01.03.2022, 01.01.2022 and 01.01.2021.
There is no 31.12.2021 column. The stored value came from the March 2022
column (P2R 1.19%), a level that only took effect after the fiscal year
had closed. The requirement in force during FY2021 was 0.98%, which moves
the CET1 headroom to 468bp. The agent had made the same error on the
annual-report side, noticed it, and fixed it before it was ever reported.
The Pillar 3 side was older, protected data, so it went to human review.

A FY2016 Pillar 3 CET1 ratio at the same bank (11.6 against a correct
11.5) had the same cause: a narrow "update bulletin" document whose
primary column was 31 March 2017, with the year-end figure relegated to a
comparative.

### 4. The number is only in a picture

**Société Générale's LCR** for 2015–2017 appears in its FY2017 Pillar 3
as a small bar chart. Text extraction flattens a chart into a string of
labels and values, in an order that follows the PDF's internal drawing
sequence, not the visual alignment of bars and dates. An earlier agent
pass read that string literally and produced 142 / 124 / 140. That
created an apparent conflict with the FY2018 Pillar 3's comparatives,
which went to review. Re-reading the chart by word *x-coordinates*,
matching each value to the bar it sits over, gave 140% for 2017, 142% for
2016 and 124% for 2015, consistent with both the narrative text and the
following year's table. The same technique found that a FY2018 leverage
ratio (4.3) was actually 2017's bar in a three-year chart. The correct
value was 4.2.

**SMFG's NPL ratio** for FY2021 and FY2022 was recoverable only by
looking at the page, not parsing it: "increasing by 0.30pp to 0.98%",
next to a chart. For FY2020 the extractor had captured the 0.08pp
*year-on-year change* instead of the 0.68% level. For FY2019 it had taken
a number from the adjacent loan-deposit-spread table, which coincidentally
had the same value. Then SMFG discontinued its NPL coverage disclosure
from FY2022 and replaced it with a chart-only graphic. The agent confirmed
that by full-document search rather than assuming it.

### 5. The regulator decides what "the ratio" means

**Scotiabank's LCR and HQLA** are disclosed on OSFI's quarterly-average
convention. The EU default in this project's metric dictionary is the
Pillar 3 LIQ1 twelve-month trailing average. Nine years of Scotiabank rows
had no period type at all, and one had the EU label. Correcting it
required establishing that OSFI's quarterly average is a legitimate,
already-used convention in the corpus (RBC, CIBC, Goldman Sachs, U.S.
Bancorp, UBS and CBA use it too), updating the dictionary, and logging
that RBC and CIBC may carry the same stale metadata.

**Santander's HQLA** for FY2022–23 had been copied from the annual
report's liquidity note (312,042m) into the Pillar 3 row, while that
year's own Pillar 3 disclosed an explicitly weighted twelve-month average
of 303,330m. **UniCredit's** Pillar 3 HQLA for FY2023–24 was stored as
59.9bn and 65.3bn. Those figures appear nowhere in the source template;
the LIQ1 year-end values are 171.6bn and 162.6bn.

**Santander's capital ratios** changed basis in the source itself. The
FY2025 annual report's footnote reads: "2023 and 2024 ratios are fully
loaded, while the 2025 ratio is phased in." The bank disclosed that
methodology break itself, so a model reading ten years of CET1 would see
a smooth series that isn't one.

**TD Bank** has no SREP add-on, because SREP is an EU/UK Pillar 2
concept. A keyword search for "SREP" across its reports does return hits,
though: every one of them is inside the word "misrepresentation". TLAC
only became a binding, disclosed OSFI requirement from Q1 2022, so
FY2016–21 are structural gaps rather than missed data. **U.S. Bancorp and
Synchrony** disclose an LCR but never the underlying HQLA dollar figure,
which is published in a separate quarterly regulatory filing rather than
the 10-K.

### 6. The document isn't what its filename says

This shape predates the last ten banks but still defines them. SMFG's
`pillar3` files turned out to be the wrong document in 8 of 11 years
(`architecture_feedback` #66). MUFG's annual report was an Integrated
Report with no financial statements for eleven straight years. CBA's
risk-weighted assets were comma-truncated in 8 of 10 years: 368,721m
stored as 721. That's the tail of the digits after the thousands
separator, and it happened to land in a plausible range.

### Ten more, from the rest of the corpus

The last ten banks aren't unusual. The project's findings log
(`architecture_feedback`) holds 174 entries across all 60 banks. Here
are ten more cases from it, all confirmed against the source documents.

**1. The file belongs to a different company.** All ten "Truist
Financial" 10-Ks in the corpus, FY2016–2025, were filings by The Southern
Company, an electric utility in Atlanta. Its XBRL tags include
`PublicUtilitiesOtherDepreciablePropertyPlantAndEquipmentPlantInService`.
Six of Citizens Financial Group's ten 10-Ks were Nielsen Holdings'
filings: 500+ mentions of Nielsen, zero of Citizens. The Truist rows (360
of them) were deleted on 18 July. Four days later a routine batch resync
put them all back, because the files were still on disk and the
filename-to-bank mapping still said "Truist". A pipeline keyed on
filenames trusts filenames.

**2. The regulatory floor is stored as the result.** Capital One's
leverage ratio was 4.0% in every year checked. That's the minimum the
10-K says the bank must keep; the actual ratio was 11.1–12.5%. Intesa
Sanpaolo's LCR was stored as exactly 100.0% for FY2022–25, taken from the
phrase "LCR > 100%". The real figures in the same report were 181.9%,
168.1%, 154.8% and 139.6%. Intesa's Pillar 3 Tier 1 ratio for FY2020 was
the SREP requirement, not the ratio achieved. The first percentage next
to a label is very often the rule, not the result.

**3. Two valid ratios, and only one is binding.** US Advanced
Approaches banks calculate capital ratios two ways, and the binding
figure is the lower one. BNY Mellon's 10-K says exactly that. The
database had stored the higher, non-binding Standardized figure: 12.5%
CET1 for FY2019 against a binding 11.5%. The same bug affected 77 rows
across eight US G-SIBs.

**4. A memo row right below the real row.** Every Australian major's
Pillar 3 summary table puts a "Common Equity Tier 1 (Internationally
Comparable)" row directly under the APRA-basis CET1 row. For nine years
the scraper took the memo row for CBA: 19.4% for FY2021 against a real
13.1%. In a peer table that makes an Australian bank look six points
better capitalised than it is.

**5. The same sentence, about a different entity.** Intesa's annual
report has a second full "Report on operations" for the standalone parent
company, using the same wording as the Group section: cost/income 44.2%
for the parent against 45.1% for the Group in FY2023. UBS's FY2017 annual
report has its Swiss capital-requirement table twice, once for UBS Group
AG and once for UBS AG. The requirement percentages are identical in both
tables. Only the capital actually held differs.

**6. The filename's year isn't the document's year.** Intesa's annual
reports for FY2015–18 were rotated by one slot: the "2015" file was the
2018 report, "2016" was 2015, and so on. UBS's "FY2024 Pillar 3" was the
30 September 2024 quarterly report, at 440KB against 3.5MB for the prior
year's. Discover's FY2023 and FY2024 "10-Ks" were 10-K/A amendments
containing only the governance section, with no financial statements at
all. File size was the first clue in both of those cases.

**7. Units and scale.** UBS's NII sensitivity was stored as 7.0 for three
years running. The source says "approximately CHF 0.7 billion", and the
parser dropped the leading "0.". MUFG's total assets are correctly
413,113.5, in yen billions, which fails every range check calibrated for
dollar and euro banks. Across roughly 15 banks, 118 interest-rate-risk
rows with no source quote were all stored as percentages, while every row
that did have a quote turned out to be a currency amount. At Deutsche
Bank the value was also June's mid-year comparative, not the December
figure.

**8. A regulator removed the disclosure.** The SEC dropped the mandatory
five-year Selected Financial Data table (Item 301) around 2021. BNY
Mellon stopped disclosing ROA from FY2021. A full-text search of those
10-Ks finds "return on assets" only as the pension plan's expected return
on assets, an actuarial assumption a scraper would happily take. A
discontinued disclosure looks exactly like a missed one unless someone
checks why.

**9. Same metric name, different measurement.** JPMorgan splits its
NII sensitivity into US-dollar and non-US-dollar tables for FY2018–23.
The database had used the dollar table in some years (6.9bn against a
combined 7.8bn for FY2020) and the non-dollar table in others (0.7bn
against a combined −1.3bn for FY2022, so even the sign was wrong).
Webster's disclosure models a gradual 12-month rate ramp reported as a
percentage, not an instantaneous ±100bp shock in dollars. It isn't the
same metric, so the correct entry is a documented structural gap, not a
number.

**10. True data that looks wrong, and a source that contradicts
itself.** First Citizens' FY2023 ROE of 63.9% and ROA of 5.9% fail every
sanity range. They're genuine: a $9.8bn gain on acquiring Silicon Valley
Bridge Bank from the FDIC roughly equals that year's entire net income.
UBS's FY2018 dividend payout ratio is 605%, verbatim, in its SEC
supplemental table. The same report's shareholder letter gives a total
payout of 76%, which includes buybacks and so should be the larger
figure. That one is still unresolved. A range check rejects the true
number in the first case and has nothing to say about the second.

## Why Pre-Coded Scraping Could Not Get There

The project didn't begin with agents. It began with a sensible,
well-engineered pipeline: `batch_ingest.py` and a regex-based
`extract_pdf()` with keyword tables per metric, rules to skip segment
tables, reject forward-looking targets, and prefer the most frequently
repeated value, plus sanity ranges and an auto-promote step. Every one of
those rules came from a real bug, and every rule is correct.

The database records how that pipeline performed. Of 26,382 superseded
metric rows, 5,671 carry `batch_ingest.py`'s signature in their notes. Of
174 logged architecture findings, 108 are recurring bugs. The six shapes
above explain why the fixes never converged.

**A pattern answers "does this match", never "is this the thing".** Each
failure above is a true match: "Net interest margin" really is on the
page; "SREP" really is inside "misrepresentation"; 721 really does follow
a comma. Prescriptive code has no concept of meaning to check a match
against.

**Every rule is a rule about one bank's layout.** "Skip segment tables"
works until SocGen puts the segment figure in a bullet directly under the
Group figure. "Prefer the year-end column" works until the table has no
year-end column. "Reject forward-looking values" works until the
forward-looking column is labelled with a date rather than the word
"target". Sixty banks across several regulatory regimes and eleven years means
thousands of layouts, and each rule you add to handle one of them is a
new way to misread another.

**Scraping has no memory across documents or years.** Catching TD's
buffer error needed the regulatory minimum from the same year. Catching
the SocGen LCR needed the following year's comparatives. Catching CBA
needed noticing that nine different years' values were all three-digit
numbers when the bank's balance sheet was in the hundreds of billions. A
script processes one page at a time. The evidence that a number is wrong
is almost always on a different page, in a different document, or in a
different year.

**Sanity ranges accept plausible nonsense.** 1.92% is a perfectly
reasonable NIM. 721bn is a plausible RWA for a large bank. Range checks
catch absurd values, and absurd values were never the problem.

**Absence is a claim that needs evidence.** Around 14,000 cells in the
database are explicit, reasoned "not disclosed" entries. A scraper that
finds nothing can't tell "this bank doesn't publish HQLA in its 10-K"
from "my pattern missed it" from "this concept doesn't exist under this
regulator." These are three different facts, and a peer comparison needs
to know which one it's looking at.

## What the Agents Actually Do

The agentic sessions (Claude Code, driven by a long written operating
prompt, `CLAUDE_CODE_METRICS_PROMPT.md`, and a checklist of every known
bug shape) don't replace code. They use it: `pdftotext -layout`,
PyMuPDF for printed page labels, grep across a whole filing, SQL against
the verification database, the `qa_*` scripts. What changes is who decides
what the output means.

From the logs, a typical cell goes like this: search the right document
(confirmed against a separate file register, not trusted from the
filename). Find the candidate. Read the surrounding table, including its
headers, dates, scope, and the units in its footnotes. Check the value
against neighbouring years and related metrics. Then write it with an
exact page and quote, or write an explicit gap with the search that
justified it, or hold it for a human.

Three habits stand out in the last ten logs:

- **Deriving rather than guessing.** Tier 2 ratios were computed as total
  capital minus Tier 1, and pre-provision profit over RWA from each
  year's own income statement. The formula and its input row IDs are
  recorded in the notes. TD's combined buffer was built component by
  component (CCB + D-SIB surcharge + DSB) for each year.
- **Refusing when refusal is correct.** TD's FY2016–17 NPL coverage was
  left empty. So was every cell where the concept doesn't exist in that
  jurisdiction, each with a reason attached.
- **Cross-checking outside the task.** The Synchrony session promoted ten
  years of NIM to `verified=2` so that its genuine card-issuer outlier
  (NIM ranges up to 16%) could legitimately widen a sanity range, rather
  than widening it on trust.

## Agents Get It Wrong Too

It would be dishonest to present agents as the fix on their own. The
same logs show:

- An earlier Société Générale fork misread that LCR bar chart.
- A SocGen pass initially wrote seven gross-loan cells on a broader IFRS 9
  concept than the bank's established series, then caught and corrected
  them itself in the same session.
- Webster Financial's file register had been reported in the changelog as
  "10/10 confirmed" in July. On 28 September it was verified to be 0/10:
  the confirmation step had never actually been persisted
  (`architecture_feedback` #173).
- An approved SMFG instruction assumed a FY2017 anchor value was already
  written. It wasn't. The agent found the gap and filled it from the
  source quote rather than following the approval to the letter.

What made each of these recoverable is the harness described in
[Confirmed, Not Claimed](/blog/comp-science/confirmed-not-claimed/):
verified values are immutable (insert and supersede, never overwrite);
anything that disagrees with protected data goes to human review; a
register of which document is which is kept separately from the metrics;
and a closing gate of QA checks has to pass before a bank can be
marked done. Agents bring judgment to every cell. The harness makes sure
a bad judgment can't quietly win.

## What It Costs to Get a Bank Through the Gate

A bank is "done" only when it passes the closing QA gate. Every
not-found cell has to be classified with evidence, every verified value
needs a page and a quote, every filing must be confirmed in the file
register, and cross-document and consistency checks must come back
clean.

**What was actually measured.** Agent sessions here can't report their
own token usage (every audit log says so rather than guessing), so there
are only two hard measurements, both recorded in
[Expensive On Purpose](/blog/comp-science/expensive-on-purpose/):

| Run | Cells worked | Tokens | Tool calls | Tokens per cell |
|---|---|---|---|---|
| UBS gap closure | 199 | ~486,000 | 251 | ~2,400 |
| MUFG gap closure + file re-confirmation | 339 | ~483,000 | 238 | ~1,400 |

On top of that, each session pays a fixed cost to read the project's
operating documents before it starts. That's now about 84,000 tokens,
down from more than 300,000 (see below).

**Indicative cost of the last ten banks' final passes.** These figures
use the measured range of 1,400–2,400 tokens per cell, plus the bootstrap
cost for each session. They're derived estimates, not metered figures.
Active minutes are taken from the audit logs where the session recorded
them.

| Bank | Final-pass work | Sessions | Logged active time | Indicative tokens |
|---|---|---|---|---|
| State Street | Gate re-run only, nothing to extract | 1 | 10 min | ~0.1M |
| U.S. Bancorp | 60 unclassified cells | 1 | 40 min | 0.17–0.23M |
| TD Bank | 82 cells + 1 wrong-period correction | 1 | 52 min | 0.2–0.28M |
| Synchrony | 90 cells + 33 re-verifications | 1 | 25 min | 0.25–0.38M |
| Webster | 10 filings re-confirmed + 57 citation gaps | 1 | not logged | 0.18–0.25M |
| Scotiabank | 5 approved items, 50 rows + dictionary fix | 2 | 28 min+ | 0.24–0.29M |
| SMFG | 5 approved items, ~50 rows + NPL re-verify | 2 | 79 min | 0.24–0.29M |
| Santander | 185-row citation backlog (final pass only) | 1 | — | 0.35–0.53M |
| UniCredit | ~300 cells + 8-year NIM retraction | 4 | 270 min | 0.75–1.05M |
| Société Générale | ~390 cells + ~260-row citation backlog, 4 review items | ~9 over 4 days | — | 1.7–2.3M |

The spread is the point. A US 10-K filer with one document type and
clean prior work closes in under an hour and a few hundred thousand
tokens. A European bank with an annual report and a Pillar 3 filing for
every year, chart-only disclosures, and a decade of wrong-column and
wrong-perimeter legacy values takes days and millions of tokens. The cost
follows how messy the bank's data is, not how big the bank is.

## Three Options, One Viable Path

There are only three ways to build a curated, cited, comparable credit
metric database. The logs rule out two of them.

**1. Pre-coded extraction.** This is cheap, fast and repeatable, and
wrong in ways it can't detect. The evidence is above: 5,671 superseded
rows carry the batch scraper's signature, and 108 recurring bug patterns
were logged. None of the six problem shapes could be fixed by writing
more rules.

**2. A person checking every cell.** This is accurate but can't be done at
this scale. The active database holds 33,102 bank × year × metric ×
document cells. At an assumed five minutes per cell to open the filing,
find the table, check scope and date, and record page and quote, one pass
is about 2,750 hours, or roughly a year and a half of full-time analyst
work. And one pass is never enough. Each time a new bug shape surfaces
(174 so far, spread over three months) the affected cells across every
bank have to be checked again. By then the next year's filings have
arrived. TD Bank's final pass alone is 82 cells, which is a working day
for a person against 52 minutes for the agent.

**3. Agents inside a harness.** This takes judgment on every cell at
hundreds of thousands of tokens per bank, with a human only on the items
the harness escalates: a disagreement with protected data, or a basis
decision. That's the only one of the three that is both accurate and
achievable. It's why 57 of 60 banks are closed out, with 13,958 values at
`verified=2` and about 14,000 cells carrying an explicit reason why the
figure isn't disclosed.

The human role doesn't disappear. It moves up a level: approving held
corrections, deciding which of two genuine bases a metric key should
mean, and spotting when a claimed result, like Webster's "10/10
confirmed", hasn't actually been done.

## The Agent Gets Better Without Retraining

The model's weights never changed during any of this. The
[original post](/blog/comp-science/llm-credit-paper-generator/) explains
why fine-tuning was abandoned. What improved was everything around the
model, and the agents did most of that improving themselves, one session
at a time:

- **Every bug becomes a written rule.** The ingestion checklist now has
  26 numbered rules: pre-flight (A1–A8), during extraction (B1–B10) and
  before write (C1–C8). Each one was added after a real failure. TD's
  one-day buffer error is a B6 wrong-period case. SocGen's cost of risk
  is a B2 segment-versus-Group case. The next agent reads the rule before
  it opens the document.
- **Every session leaves directions for the next.** The database holds
  2,015 location hints, recording where a metric lives for a given bank
  and document type. 851 of them record that a metric is confirmed
  absent, so no future session spends tokens searching for it again.
- **Every finding is queryable.** The 174 `architecture_feedback`
  entries (101 logged in July, 25 in August, 48 in September) are a bug
  backlog the agent both writes to and reads from. UniCredit's NIM finding
  was logged specifically because Italian and EU filers will repeat it.
- **The gate grows when something slips through.** A file-register
  completeness check was added in July after a wiring gap. Webster's
  false "10/10 confirmed", caught in September, is exactly the failure it
  exists to catch.
- **The agent tunes its own start-up.** A session-bootstrap skill,
  written from the project's own experience, cut the mandatory reading at
  session start from more than 300,000 tokens to about 84,000. It has a
  `LESSONS.md` file the agent updates itself. The most recent entry, from
  the 27 September UniCredit session, notices that the changelog has
  outgrown the token figure the skill quotes for it. It tells the next
  session to check the file size first and search by bank name rather
  than read the whole file.
- **Method changes carry forward.** Switching from printing whole PDF
  pages into the transcript to extracting text once and searching it
  added roughly 40% more work per token. The chart-reading fix
  (x-coordinates rather than text order) is now part of the method, not a
  one-off.

That is what "adaptive" means here. The agent doesn't get smarter. The
environment it works in accumulates the corpus's quirks faster than any
rulebook written up front could, and each bank costs less judgment than
it would have without the previous ones. A pre-coded pipeline has to
anticipate the data. An agentic one learns it from the data, and a
reviewer can read everything it has learned.

## The Point: Peer Comparison Is a Data Problem

The generator exists to write credit papers, and a credit paper is
comparative. A bank's CET1 headroom, liquidity coverage or NPL coverage
means little in isolation. It's the position against a peer group that
carries the analysis. [Not a Specification](/blog/comp-science/not-a-specification/)
made that the core of the problem statement, and
[One Metric, Three Rulebooks](/blog/comp-science/one-metric-three-rulebooks/)
showed why a Stage 3 ratio cannot exist on a US balance sheet.

The last ten banks make the consequence concrete. Put the raw
disclosures side by side and you get:

- Santander's NPL coverage at 71% against a peer's CR1-derived 39%: a
  32-point "outperformance" that is entirely definitional.
- Scotiabank's LCR on a quarterly average against an EU bank's
  twelve-month trailing average.
- Santander's FY2025 capital ratios on a phased-in basis against prior
  years and peers that are fully loaded.
- CBA's CET1 on APRA's "internationally comparable" memo basis (19.4%)
  against peers' actual regulatory CET1: six points of strength that
  aren't there.
- BNY Mellon's non-binding Standardized ratio against peers' binding
  ones.
- SocGen's cost of risk swinging between Group and French retail
  perimeters from one year to the next.
- UniCredit showing a NIM that is actually a related-party share, and
  HQLA at a third of its true value.
- A US bank with an empty SREP cell and a European bank with a populated
  one, where the difference is a regulatory regime, not a weakness.

A model given that table will write fluent, confident, cited prose about
differences that don't exist. That is the failure
[Antidote for Large Liar Model](/blog/comp-science/antidote-for-large-liar-model/)
was designed against, and it happens without the model inventing a
single number. Every input would have been faithfully extracted. The
comparison would still be wrong.

This is why the project spends its effort where it does. The generator
itself reached 96% on its evaluation benchmark with prompting and
deterministic post-processing
([LLM Credit Paper Generator](/blog/comp-science/llm-credit-paper-generator/)).
The hard, expensive, still-ongoing work is upstream. Every number needs a
single defined concept, scope, basis and date, a real citation, and an
explicit, reasoned entry wherever the bank doesn't disclose it. Banks
don't publish data in a form that allows peer comparison. Someone has to
make it comparable, and that work needs reading and judgment on each
cell, not pattern matching.

## Key Takeaways

- Pre-coded scraping didn't fail because it was badly written. It failed
  because bank disclosures differ in layout, terminology, scope, basis
  and timing, and a pattern can confirm that text matches but not what
  it means.
- The evidence that a number is wrong usually sits in another year,
  another document or another metric. Verification has to reason across
  all three.
- Agents made extraction tractable by applying judgment to each cell,
  and made it safe only because a separate harness assumes they will
  sometimes be wrong.
- Coded extraction can't be trusted, and checking every cell by hand
  (roughly 2,750 hours per pass, repeated every time a new bug shape
  appears) can't be done in the time available. Agents inside a harness
  are the only viable way to build a curated credit metric database at
  scale, at roughly 0.1–2.3M tokens per bank depending on how messy its
  disclosures are.
- The agent improves without retraining: checklist rules, location
  hints, a queryable bug backlog and a self-editing skill carry what
  each session learns into the next.
- Without harmonised, cited, scope-consistent data, a peer credit
  comparison ranks disclosure conventions, not banks.

---

**Previous in the series:** [Audit the Neighbor Too](/blog/comp-science/audit-the-neighbor-too/)
**Next in the series:** — this is the latest post

---

## Full Series

1. [Not a Specification](/blog/comp-science/not-a-specification/)
2. [LLM Credit Paper Generator](/blog/comp-science/llm-credit-paper-generator/)
3. [One Metric, Three Rulebooks](/blog/comp-science/one-metric-three-rulebooks/)
4. [Two Numbers, Same Page](/blog/comp-science/two-numbers-same-page/) *(draft, unpublished)*
5. [Adding the 61st Bank](/blog/comp-science/adding-the-61st-bank/)
6. [Antidote for Large Liar Model](/blog/comp-science/antidote-for-large-liar-model/)
7. [Post PDF](/blog/comp-science/post-pdf/)
8. [Whose Bank Is This?](/blog/comp-science/whose-bank-is-this/)
9. [Confirmed, Not Claimed](/blog/comp-science/confirmed-not-claimed/)
10. [Audit the Neighbor Too](/blog/comp-science/audit-the-neighbor-too/)
11. **No Two Banks Say It the Same Way** (this post)

---

*See also, from the operational series:* [Expensive On Purpose](/blog/comp-science/expensive-on-purpose/) —
what the agentic verification work described here costs in tokens, and why.
