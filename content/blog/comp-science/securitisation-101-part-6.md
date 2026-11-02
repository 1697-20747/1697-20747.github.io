---
title: "Securitisation 101 — Part 6: The Bank of England Data Tape"
date: 2026-11-01T10:00:00Z
lastmod: 2026-11-01
draft: false
categories: ["comp-science"]
tags: ["RMBS", "securitisation", "data quality", "Bank of England", "python"]
series: ["Securitisation 101"]
description: "How the model generates the Bank of England loan-level data tape, the testing regime that runs before and after the file is written, and why every rule is data, so the software can follow the Bank's template when it changes."
summary: "Part 6 of 6: the BoE loan-level tape, step by step, and the data quality regime that tests it at generation, in memory and again after it is written."
ShowToc: true
TocOpen: false
cover:
  image: "images/comp-science/boe_tape_process.svg"
  alt: "BoE loan-level data tape: generation and testing, seven steps from loan data to release"
  caption: "The data tape: generated, validated, written, read back and tested"
---
<!--more-->

Part 1 said the data comes first. This part is about the data that leaves: the **Bank of England loan-level data tape**, one row per mortgage in the Bank's template, which a lender submits for a pool of mortgages or an RMBS used as collateral with the Bank.

It looks like the dullest output in the build. It is also the one with the least room for error: the Bank receives it as a file, reads it by machine, and rejects what does not match the template. A tape that is close is a tape that is wrong.

---

## The template

The Bank publishes the template as a workbook ("Loan Level Data: Reporting Template for Residential Mortgage Pools", updated April 2024). It has two parts:
- **the fields**: 233 AR codes (AR1 the run date, AR3 the loan id, AR67 the current balance, AR129 the postcode, and so on), each with a priority (mandatory or optional), a format, a maximum length and, for coded fields, a list of allowed codes;
- **the instructions**: sixteen numbered rules for the files themselves. No file over 150MB; CSV, tab-delimited TXT or a one-sheet XLSX only; AR codes alone in the header row; no password; blanks where data was not collected; redeemed loans for one period after redemption, defaulted loans for as long as they last.

Neither part is hard-coded in the model. The fields are read from the Bank's workbook into a field dictionary. The instructions, and the model's own extra checks, sit in a **tape rules data set**: each rule with an id, what it requires, whether it is the Bank's rule or the model's, and where it comes from (for example, "Template and instructions, instruction 3").

---

## Generation and testing

![BoE data tape: generation and testing](/images/comp-science/boe_tape_process.svg)

### 1. Loan data in template coding

The loans are held in the template's own coding from the start, in Parquet. Each loan is one row with AR fields, so the tape is a selection of what is already there, not a translation. Data not collected stays blank; "ND" (no data) appears only where a field's code list offers it.

### 2. Pool data quality, at generation

Before a pool is used at all, three layers of checks run:
- **template rules**, the same validator the tape uses;
- **integrity**: row counts, unique loan ids, key fields populated, no negative balances, interest-only loans holding their balance;
- **plausibility**: the pool's profile against Bank of England / FCA lending statistics (LTV, income multiples, buy-to-let and arrears shares, the regional mix).

The third layer exists because a pool can pass every format rule and still be economically wrong. One early generated pool had a 35% average LTV: perfectly formatted, completely unrealistic.

### 3. Currency integrity

When the cash-flow engine loads a pool, it decodes every loan's currency field (AR65) through the template's code list and checks it against the deal currency. A pool mixing currencies is refused: the engine has no FX conversion, so it would add pounds to euros. The design allows other currencies, but each needs its own rate index, curve and conventions, so for now the model works only in GBP. The same rule is tested again on the tape and its cover sheet.

### 4. Build the tape, validate in memory

The tape takes the template's fields, in the template's order, and nothing else. AR1 is the run date, the date the data were produced, as the template asks; AR2 is the pool id. For an RMBS, origination and maturity dates become quarter dates. Nothing is recoded or rescaled.

The whole tape is then validated in memory: every field present, codes on their lists, dates and numbers in their formats, percentages in decimal form, and the cross-field rules (maturity after origination, arrears and status agreeing, fixed-rate loans with a revision date). **A bad value stops the tape.** It is a defect in the data chain, to fix at source, never something to repair quietly on the way out.

### 5. Write the file

CSV, TXT or a one-sheet XLSX, header row of AR codes only, no password. Anything over 150MB is split into numbered parts, each with its own header row. Internal columns (pricing, approximate geolocation) go to a separate file that is never submitted.

### 6. Post-generation tests: read it back

Validating the data in memory is not the same as testing the file. So the files are **read back exactly as written**, as the Bank would receive them, and tested again:
- **the files**: accepted format, under 150MB, one Excel sheet, opens without a password, UTF-8 text, every row the same width (an unquoted comma in a borrower id would break that), header exact, parts numbered in order;
- **the content**: every loan in the pool there once and nothing else, every value equal to the pool it came from (no silent change), the loan count and total balance equal to the pool's to the penny, blanks that are blank rather than the word "nan";
- **the template, again**: the full validation re-run on what was read back;
- **the cover sheet**: run date, pool id, loan count, balance and currency all agree with the tape.

Each check carries its rule id, and **every rule must have at least one check**. A rule added to the data set without a check fails the run, so a requirement cannot be listed and then quietly never tested.

On the sample deal, all 27 rules pass: 29 checks over 5,366 loans.

### 7. Release, or stop

Only a tape that passes is released, with its cover sheet, a test report and the run's provenance (the code version, the configuration and data hashes, and each file's SHA-256). The report lists every rule, its source, its checks and the result, so a reviewer can see what was tested and against what.

A tape that fails is not released. The report stays beside it and names each failed rule.

The monthly reporting refreshes the tape at each payment date and puts each refresh through steps 4 to 7.

---

## What the tests have already caught

Writing the read-back tests turned up a real defect. The cover sheet had coded the pool's currency as **AR65 = 1**. On the template's list, 1 is the euro; sterling is 2. The tape itself was right, the cover sheet beside it was wrong, and the in-memory validation could never see it, because it only checks the tape. The cover sheet now takes the code from the tape, and the post-generation tests compare the two: a cover sheet coded 1 fails two rules.

That is the case for testing the output, not just the data: the defects that matter are often in the joins between pieces that each look right on their own.

---

## When the Bank changes the rules

The template has been revised before, and will be again. The architecture assumes it will:
- **Fields** come from the Bank's workbook. A new template means rebuilding the field dictionary from the new workbook; the generator, validator and tape writer all read it.
- **Instructions and thresholds** live in the tape rules data set, which is dated. A new template gets a new version from its effective date; the old version is archived, so a tape for an earlier date is still tested against the rules in force then.
- **Each rule is labelled** as the Bank's or the model's own. The model's checks are stricter in places (core fields never blank, plausible percentage ranges, the round trip), and can be relaxed without breaching a Bank rule.
- **Every rule needs a check**, and the tests enforce it in both directions, so a new rule cannot sit in the data set untested.

So when the Bank moves the goalposts, the change is to data, with a source and a date, and the tests say at once whether the software still meets it.

---

## Limits

- **Excel output** needs two libraries this build does not have installed, so the XLSX path is tested only where they are present. CSV and TXT are tested every time.
- **The reporting glossary** the template asks for (to explain blank mandatory fields and any added codes) is not generated. The tests list the fields that need one.
- **Submission timing** (raw pools monthly within ten working days of the run date; RMBS at least quarterly) is outside the file, so it is recorded, not tested.
- **Synthetic data.** The pool is made up. The rules are the Bank's; the loans are not.

---

### Securitisation 101 series

**Previous:** [Part 5: Credit Enhancement, Mechanism and Design](/blog/comp-science/securitisation-101-part-5/)

**Full series**
1. [Part 1: What It Is, and Why the Data Comes First](/blog/comp-science/securitisation-101/)
2. [Part 2: The Parties and the Waterfall](/blog/comp-science/securitisation-101-part-2/)
3. [Part 3: Building the Deal](/blog/comp-science/securitisation-101-part-3/)
4. [Part 4: Outputs, Assumptions and Limits](/blog/comp-science/securitisation-101-part-4/)
5. [Part 5: Credit Enhancement, Mechanism and Design](/blog/comp-science/securitisation-101-part-5/)
6. Part 6: The Bank of England Data Tape (this post)
