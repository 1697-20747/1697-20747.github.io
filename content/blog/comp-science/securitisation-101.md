---
title: "Securitisation 101"
date: 2026-05-17T07:13:28Z
draft: true
categories: ["comp-science"]
tags: [securitisation, tranching, RMBS]
description: "A start to finish guide to securitisation"
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

## Overview

This is about the dark art of securitisation (securitization?!), what it is, how it works, the concepts behind it and how it works IRL.

A few notes before we proceed.
- This is based on real processes, actual credit concepts, and done at scale.
- The data set is made up of course, but the loans are all realistic in nature.
- Data tape standards as per BoE have been adopted.
- The code does a few things:
    - creates random portfolio of loans.
    - creates loan level cash flows for P&I.
    - creates pool level aggregation of cash flows (all loans together into monthly schedules).
    - this incorporates recent real world transaction and prospectus. See references.
    - full reporting is properly generated from data using stand alone scripts, output onto log files.
    - I baked in API call methods to deploy reporting properly. Note pithy comment on excel!!
    - this approach is based on stand alone bash scripts, so you can run from CLI and don't need any IDE. It is stable and lean, but to change best you know how to read code. Code on github.
    - from this applies stress and credit methodologies to tranche the loans. This is the key functional task here.
    - the tranching model is stand alone, can be applied at scale to any pool of mortgages.
    - reporting dashboard and summary statistics for the mortgage pool, and the tranches.
    - key assumptions are in stand alone files and read in as needed. This means you can change them and model still works.
    - these are big data sets, csv is poor choice. For key tables apache parquet is used for good reason, computational efficiency on the monte carlo runs in the main.


⚠️ Warning The tranching model is complex, but is highly realistic. it is based on open source data sets, and features all of the key aspects required. The monte carlo process is set for n runs, 10,000 is good enough. Test. The variance and correlation assumptions are based on real world data, historical interest rates, HRI data, etc, etc. It adopts rating agency concepts based on public domain methodologies. It is about 90% complete, you can definitely use this for tranching purposes when assessing mortgage pools to give you realistic results. But it is not 100%. Do not use in production environment. The last 10% needs use of brain cells, if you don't know what you are doing, do not use this in production. The 100% version is not going on my git hub for lots of reasons. The last parts are not so easy. There is enough here you should be able to tweak this to your own choices, which is part of the last 10%, your assumptions and mine not the same.

A few other notes on this post. I usually write, or re write a lot of the code. This one features the heaviest use of AI yet. I sketched out the processes that I knew I needed, I segregated them, designed the basic path that I wanted, reviewed external market standards, docs and credit processes. From here, I used AI to build this like lego, one stand alone piece at a time. I made sure integration was built in. Tranching model used lots of public domain inputs, actual securitisation prospectuses and periodic reporting, credit processes from many rating agencies (all public domain). I am confident I could have slogged this out without AI, but it would have taken several hundred of hours to get it right.

> Don't use excel for things like this if this is your day job. It does not scale, its time as an industry we all moved on from that. It was nice, and you can do a lot in excel. But you shouldn't any more. Its time to let go.....rip off the band aid and learn to code properly.


---

## Securitisation - what is is?

A mortgage is just that, a mortgage from a bank of building society. You can't really sell it or transfer, it is not a security. 

1. So if we take a lot of mortgages, pool them (aggregate), put them into a legal entity, we have aggregated all the cash flows. If a loan defaults and does not pay, then the pool experiences the same impacts.
2. Now we can allocate the cash flows from the pool in an ordered manner of priority. This is called tranching. This *does not* create more cash flow, it only allocated. What this means, for example is the all of the cash from the pool will first pay the first ranking tranche investors, as AAA. If and only if they get paid in full, then left over cash can be allocated to the next tranche, AA, and so on.
3. If I get paid from all mortgages, not just one, presumable the probability of many loans defaulting at same time is less than that of one loan. Diversification, or imperfect correlations. The lower the correlation the betters.
4. If I take less risk on cash flows from *all* mortgages, then in an efficient market this should result in lower yield, as the security is lower risk. You must ponder this until you understand the concept. If mortgages have credit spreads (risk premium over time value of money) of say 200bps, you cannot create a securitisation if the AAA spreads are 200bps. This would be mathematically impossible. This is a bit abstract, so we will cover in sources and uses later by shocking yields and breaking the securitisation from day one.
5. There are no other sources of funds, what pays in gets paid out. There is no more funds coming in for any reason.



❗ Important Securitisation is a zero sum game. It cannot create cash flow. Much like 2nd law of thermodynamics (the total entropy of an isolated system can never decrease over time.), the process only allocates existing cash flow from the system (the SPV). Total sources and uses *must* reconcile, in total and for every period, other than small liquidity amounts.

---

## The formal process

Here is a logical step by step process for creating an RMBS (or any ABS) from scratch:

# RMBS Creation Process

1. **Acquire Mortgage Pool**  
   Gather a portfolio of residential mortgages with standardized loan-level data including balances, rates, borrower characteristics, and payment history.

2. **Perform Due Diligence**  
   Review the mortgage pool for credit quality, underwriting standards, geographic concentration, delinquency status, and data integrity.

3. **Model Loan Cash Flows**  
   Generate projected monthly mortgage cash flows including scheduled principal, interest, prepayments, defaults, and recoveries.

4. **Analyze Credit Risk**  
   Estimate expected losses and stress performance using historical data, macroeconomic scenarios, and statistical or machine learning models.

5. **Create Special Purpose Vehicle (SPV)**  
   Transfer the mortgage pool into a bankruptcy-remote legal entity that will issue the RMBS securities.

6. **Structure the RMBS Tranches**  
   Divide the securitization into tranches (AAA, AA, A, BBB, residual) with different levels of seniority and credit protection.

7. **Build the Waterfall Mechanism**  
   Define how monthly mortgage cash flows and losses are allocated among tranches according to priority rules.

8. **Apply Credit Enhancement**  
   Add protections such as subordination, excess spread, reserve accounts, or overcollateralization to improve tranche credit quality.

9. **Run Stress Scenarios**  
   Simulate severe economic conditions such as house price declines, unemployment shocks, and elevated defaults to test tranche resilience.

10. **Size the Tranches**  
    Adjust tranche balances iteratively until each tranche satisfies target expected loss and rating criteria under stress conditions.

11. **Obtain Credit Ratings**  
    Submit the transaction to rating agencies for independent analysis and assignment of tranche credit ratings.

12. **Issue RMBS Securities**  
    Sell the structured securities to investors, with proceeds used to fund the mortgage acquisition.

13. **Service the Mortgage Pool**  
    Collect borrower payments, manage delinquencies and foreclosures, and distribute monthly cash flows through the waterfall.

14. **Monitor Ongoing Performance**  
    Continuously track collateral performance, tranche losses, prepayments, and trigger events throughout the life of the securitization.
---



---
## Key Takeaways

- 2nd law of thermodynamics applies (well, the conservation concept for cash does).
- There *must* be yeild advantage at the A notes, or you cannot economically issue.
- There is a ceiling at BBB and first loss tranches where it won't work.
- Remeber if you sell $100 for $80, its the same thing as getting higher yields. This is how first loss tranches earn risk adjsuted yields. But it comes from thinner A note yields. No money is created here!
- There is huge scope for reporting automation if you let go of excel from incpetion. Design in your reporting process from day one. You can fully automate, and log all reporting and acess across all investors.
- Secrutisation process works, but its not a magic cure. CMSB, a lot sketchier for credit performance that resi still worked, losses got up to the J notes, but in general the A's worked as intended.

---

## References

- As individually noted.
