---
title: "Two Numbers, Same Page"
date: 2026-07-12T15:30:00Z
draft: true
categories: ["comp-science"]
tags: [credit-risk, LLM, banks, claude-code, data-architecture]
description: "How the credit-paper pipeline's Claude Code extraction agent actually works, and a bug it caught that a pattern-matcher never would have."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

*Fourth post in a series about building a local, offline credit-analysis
pipeline. Start with [Not a Specification](/blog/comp-science/not-a-specification/),
or see the full series list at the bottom of this post. This one's about
the extraction agent itself, following on from [One Metric, Three
Rulebooks](/blog/comp-science/one-metric-three-rulebooks/) on the
IFRS9/CECL split.*

## The problem with a regex

Early on, metric extraction was regex against PDF text: find "CET1", find a nearby percentage, write it down. It worked until it didn't, and when it didn't, it failed silently — the wrong number, matched with total confidence, no way to tell from the output alone that anything had gone wrong.

The fix wasn't a smarter pattern. It was giving up on pattern-matching as the *final* decision-maker at all. A regex is still allowed to find candidates — grepping a 300-page filing for every place a term appears beats reading it cover to cover — but something has to actually look at each candidate and decide if it's real. That something is Claude Code, and the discipline around it is the actual subject of this post: not the extraction, but the mechanism that keeps an agent doing hundreds of these calls a day from drifting into exactly the shortcuts that made the regex unreliable in the first place.

## Read yourself, don't build a decider

The one rule that everything else hangs off: a helper script is allowed to *dump* a document's text so there's something to read. It is never allowed to *decide* where the value is — no keyword scoring, no "take the first match," no auto-selected candidate page. That was tried once, early, as a way to save time. It failed the same way the regex did: confident, wrong, and invisible until someone checked. Search is a fast index into the document; judgment about what the number actually means still has to be a read, every time.

That's expensive if it happens fresh for every bank, every year. It doesn't have to. Report templates are stable — a given bank's Pillar 3 disclosure puts the same ratios on roughly the same pages, filing after filing. Once a location's confirmed, it's cached: page, a short heading clue, a confidence level. The next year checks the hint first — read the expected page, confirm the number's still there and still makes sense next to last year's — and only falls back to a full search if the hint misses. Most years, for most metrics, that's a fast confirm, not a fresh investigation. The judgment discipline stays; the *repetition* of it doesn't.

## Not every mistake needs the same amount of ceremony

A found error used to mean one thing: stop, list it, wait for a human to approve the fix before anything gets written. That's still true for anything that touches a value someone already trusted, or where two sources genuinely disagree. It stopped being true for the boring case — a first-time value, cleanly sourced, sitting inside the expected range, nothing else claiming to be the real number. That gets written immediately and logged for visibility, not held up for a decision that was never really in question. The review gate moved to where the actual judgment calls live, instead of sitting in front of every single write regardless of how obvious it was.

Same logic runs at the level of which bank starts next. A name given once no longer needs to be given again after every bank finishes clean — but a bank that comes back flagged still stops everything until someone looks, on purpose, every time. Cheap steps get automatic; anything that could be wrong in a way that matters still gets a human in the loop.

## The bug a pattern-matcher would never have caught

Here's what all of that discipline is actually for. A Pillar 3 liquidity disclosure states two different HQLA figures on the same page: one "as of" the reporting date, one averaged over the trailing twelve months. Both real. Both correctly labeled, if you read the surrounding sentence. A pattern that just grabs "the number near HQLA" has no way to know which one it landed on — and it turned out one extraction pass had grabbed the spot figure from the annual report while another had grabbed the average from the regulatory filing, for the *same bank, same year*. Two real numbers, both accurate, flagged as a data conflict because nothing had ever recorded which one was supposed to be canonical.

Fixing the one case was easy once someone actually read the page. Fixing the *shape* of the bug meant asking the more useful question: what's this true of generally? Every metric in the schema now carries an explicit basis — a point-in-time snapshot, or a period average, and if the latter, whether that period is a fiscal year or a rolling twelve months. Not a guess applied after the fact — checked against the DB, since the label already living there for this exact case said "year-end" and it was wrong, which is a good demonstration of the actual failure mode: a plausible-looking classification nobody had gone back and verified.

None of this is exotic. It's the same lesson twice, at two different scales: a script that decides instead of reads will eventually be confidently wrong, and a label that was never checked against reality will eventually just be wrong, sitting there looking fine.

## Key Takeaways

- Let a script find candidates. Don't let it decide between them.
- Caching *where something is* is safe. Caching *what something means* needs re-checking the first time it actually matters.
- Review gates belong at the judgment calls, not at every write regardless of how obvious it was.
- Two numbers can both be true and still be the wrong one to compare — that's not a data conflict, it's a missing definition.

---

**Previous in the series:** [One Metric, Three Rulebooks](/blog/comp-science/one-metric-three-rulebooks/)
**Next in the series:** [Adding the 61st Bank](/blog/comp-science/adding-the-61st-bank/)

---

## Full Series

1. [Not a Specification](/blog/comp-science/not-a-specification/)
2. [LLM Credit Paper Generator](/blog/comp-science/llm-credit-paper-generator/)
3. [One Metric, Three Rulebooks](/blog/comp-science/one-metric-three-rulebooks/)
4. **Two Numbers, Same Page** (this post) *(draft, unpublished)*
5. [Adding the 61st Bank](/blog/comp-science/adding-the-61st-bank/)
6. [Antidote for Large Liar Model](/blog/comp-science/antidote-for-large-liar-model/)
7. [Post PDF](/blog/comp-science/post-pdf/)
8. [Whose Bank Is This?](/blog/comp-science/whose-bank-is-this/)
9. [Confirmed, Not Claimed](/blog/comp-science/confirmed-not-claimed/)
10. [Audit the Neighbor Too](/blog/comp-science/audit-the-neighbor-too/)
