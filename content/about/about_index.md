---
title: "About"
layout: "single"
ShowReadingTime: false
ShowBreadCrumbs: false
hidemeta: true
---

This is a personal site. The writing here covers economics, data analytics, computer science, credit risk, philosophy, and whatever else earns a place. The posts are notes made public — working through ideas, not finished arguments.

## The day job

Finance. Primarily credit — analysis, structure, the forensics of how things fail. If you have spent time reading financial statements with genuine scepticism rather than confirmation bias, you will find some common ground here.

## The rest of the time

Low-level programming on small devices. Embedded systems, constrained hardware, the kind of work where every byte is a negotiation. This requires a working understanding of machine learning, which means most of the comp science writing here sits at that intersection — the plumbing beneath the tools everyone else uses without thinking about. Currently trying to build navigation from optical feed using 3d object tracking, and vector path determination. Its done in 3D, but working on 2D in the main. This is part of a wider project. Right now trying to run it all on a Luckfox Pico Ultra W, with a few bits and bobs added (position, camera, etc, etc).

None of the comp science is the day job. It is personal time, chosen freely. That distinction matters.

## On writing style

The text is not AI generated. The informal phrasing is deliberate — clarity does not require formality, and pretension is its own form of obscurity. If a sentence is clumsy it is because the thought behind it was still being worked out, not because a language model hallucinated it into existence.

## On social media

No. This is it. There is a very small number of WhatsApp groups, and that is the full extent of it. If you want to get in touch, LinkedIn is in the footer.

## The name

`[1697, 20747]`

A tokenizer output. Run the name through a BPE tokenizer — GPT-family, if you are curious — and those are the token IDs you get back. If that means something to you, you are probably in the right place. If it does not, the writing should still be readable without it.

## Why?

As stated elsewhere, don't do anything without a problem statement that has been developed. There are a couple of reasons why for this site. One is a repository to use, much later, to post train a smaller LLM. It requires structured text, so by default I can scrape this site to use for curated training data. Second, a reminder for myself. Third, the discipline of writing things down. Clear writing requires clear thinking. I generally suck at writing. Fourth, it serves a practical purpose. With a varied background, I have always struggled with have a CV that actually covers my skill set. This site acts as a very expanded skill set description. You can infer what I am good at, or not, from the contents, in a manner impossible in a short form CV. Lastly, in some manner for my kids. Hopefully some life lessons buried in here somewhere. They have heard them all, but it might be a reminder one day. Books, as much as I love them, are not for everyone. This is in essence a book, split across a few subjects. But easier to contain.

I hope the traditional CV dies, and gets replaced with actual skills framework. I have a lot of respect for those who can do the doing.

I hope something here is useful to someone.

## Site structure

<div style="overflow-x: auto; margin: 1.5rem 0;">
<svg width="100%" viewBox="0 0 680 480" xmlns="http://www.w3.org/2000/svg" style="font-family: inherit;">
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M2 1L8 5L2 9" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </marker>
</defs>

<rect x="250" y="20" width="180" height="40" rx="8" fill="#f1efe8" stroke="#5f5e5a" stroke-width="0.5"/>
<text x="340" y="35" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="500" fill="#2c2c2a">Hugo site (root)</text>
<text x="340" y="52" text-anchor="middle" dominant-baseline="central" font-size="11" fill="#5f5e5a">config.toml · profileMode</text>

<line x1="280" y1="60" x2="90" y2="130" stroke="#888780" stroke-width="0.5" marker-end="url(#arrow)"/>
<line x1="310" y1="60" x2="240" y2="130" stroke="#888780" stroke-width="0.5" marker-end="url(#arrow)"/>
<line x1="340" y1="60" x2="340" y2="130" stroke="#888780" stroke-width="0.5" marker-end="url(#arrow)"/>
<line x1="370" y1="60" x2="470" y2="130" stroke="#888780" stroke-width="0.5" marker-end="url(#arrow)"/>
<line x1="400" y1="60" x2="600" y2="130" stroke="#888780" stroke-width="0.5" marker-end="url(#arrow)"/>

<rect x="20" y="130" width="140" height="40" rx="8" fill="#e1f5ee" stroke="#0f6e56" stroke-width="0.5"/>
<text x="90" y="145" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="500" fill="#085041">content/</text>
<text x="90" y="161" text-anchor="middle" dominant-baseline="central" font-size="11" fill="#0f6e56">All source markdown</text>

<rect x="170" y="130" width="120" height="40" rx="8" fill="#e6f1fb" stroke="#185fa5" stroke-width="0.5"/>
<text x="230" y="145" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="500" fill="#0c447c">static/</text>
<text x="230" y="161" text-anchor="middle" dominant-baseline="central" font-size="11" fill="#185fa5">avatar · images · data</text>

<rect x="300" y="130" width="80" height="40" rx="8" fill="#eeedfe" stroke="#534ab7" stroke-width="0.5"/>
<text x="340" y="145" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="500" fill="#3c3489">themes/</text>
<text x="340" y="161" text-anchor="middle" dominant-baseline="central" font-size="11" fill="#534ab7">PaperMod</text>

<rect x="400" y="130" width="120" height="40" rx="8" fill="#faeeda" stroke="#854f0b" stroke-width="0.5"/>
<text x="460" y="145" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="500" fill="#633806">public/</text>
<text x="460" y="161" text-anchor="middle" dominant-baseline="central" font-size="11" fill="#854f0b">Built HTML output</text>

<rect x="535" y="130" width="130" height="40" rx="8" fill="#f1efe8" stroke="#5f5e5a" stroke-width="0.5"/>
<text x="600" y="145" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="500" fill="#2c2c2a">scripts</text>
<text x="600" y="161" text-anchor="middle" dominant-baseline="central" font-size="11" fill="#5f5e5a">new-post · publish · graph</text>

<line x1="60" y1="170" x2="40" y2="230" stroke="#888780" stroke-width="0.5" marker-end="url(#arrow)"/>
<line x1="80" y1="170" x2="120" y2="230" stroke="#888780" stroke-width="0.5" marker-end="url(#arrow)"/>
<line x1="100" y1="170" x2="220" y2="230" stroke="#888780" stroke-width="0.5" marker-end="url(#arrow)"/>
<line x1="115" y1="170" x2="350" y2="230" stroke="#888780" stroke-width="0.5" marker-end="url(#arrow)"/>

<rect x="10" y="230" width="80" height="36" rx="6" fill="#e1f5ee" stroke="#0f6e56" stroke-width="0.5"/>
<text x="50" y="244" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="500" fill="#085041">blog/</text>
<text x="50" y="258" text-anchor="middle" dominant-baseline="central" font-size="11" fill="#0f6e56">8 sections</text>

<rect x="98" y="230" width="80" height="36" rx="6" fill="#e1f5ee" stroke="#0f6e56" stroke-width="0.5"/>
<text x="138" y="244" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="500" fill="#085041">books/</text>
<text x="138" y="258" text-anchor="middle" dominant-baseline="central" font-size="11" fill="#0f6e56">33 entries</text>

<rect x="186" y="230" width="80" height="36" rx="6" fill="#e1f5ee" stroke="#0f6e56" stroke-width="0.5"/>
<text x="226" y="244" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="500" fill="#085041">about/</text>
<text x="226" y="258" text-anchor="middle" dominant-baseline="central" font-size="11" fill="#0f6e56">_index.md</text>

<rect x="274" y="230" width="120" height="36" rx="6" fill="#e1f5ee" stroke="#0f6e56" stroke-width="0.5"/>
<text x="334" y="244" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="500" fill="#085041">_index.md</text>
<text x="334" y="258" text-anchor="middle" dominant-baseline="central" font-size="11" fill="#0f6e56">homepage root</text>

<line x1="50" y1="266" x2="50" y2="306" stroke="#888780" stroke-width="0.5" stroke-dasharray="4 3"/>
<rect x="10" y="306" width="620" height="36" rx="6" fill="none" stroke="#888780" stroke-width="0.5" stroke-dasharray="4 3"/>
<text x="26" y="328" dominant-baseline="central" font-size="11" fill="#5f5e5a">economics · data-analytics · comp-science · credit-risk · philosophy · bjj · unhelpful-advice · other</text>

<rect x="10" y="358" width="620" height="50" rx="6" fill="none" stroke="#888780" stroke-width="0.5" stroke-dasharray="4 3"/>
<text x="26" y="376" dominant-baseline="central" font-size="11" font-weight="500" fill="#444441">Published posts</text>
<text x="26" y="394" dominant-baseline="central" font-size="11" fill="#5f5e5a">credit-risk/enron-a-look-back.md · economics/inflation-measurement.md · unhelpful-advice/define-the-problem.md · definitions-matter.md</text>

<line x1="138" y1="266" x2="138" y2="424" stroke="#888780" stroke-width="0.5" stroke-dasharray="4 3"/>
<rect x="98" y="424" width="80" height="36" rx="6" fill="none" stroke="#888780" stroke-width="0.5" stroke-dasharray="4 3"/>
<text x="138" y="442" text-anchor="middle" dominant-baseline="central" font-size="11" fill="#5f5e5a">33 book md files</text>
<text x="138" y="457" text-anchor="middle" dominant-baseline="central" font-size="11" fill="#5f5e5a">one per book</text>

<rect x="400" y="306" width="240" height="60" rx="8" fill="none" stroke="#888780" stroke-width="0.5" stroke-dasharray="4 3"/>
<text x="416" y="326" dominant-baseline="central" font-size="11" font-weight="500" fill="#444441">config.toml</text>
<text x="416" y="344" dominant-baseline="central" font-size="11" fill="#5f5e5a">+ credit-risk menu entry</text>
<text x="416" y="362" dominant-baseline="central" font-size="11" fill="#5f5e5a">+ profileMode · avatar</text>

</svg>
</div>

---

As for context, this is broadly how I do it. I generate a new post in bash, with the basics, then edit actual content later. Usually in VS Code, but often just in nano. The simpler the better. Its very basic markdown, with some code blocks. I used Hugo re render it, and manually set up the file structure.

## Some Bash I Use

Short description of what this does.
```bash
#!/bin/bash
echo "hello world"
```

Another block if you want multiple examples.
```bash
for f in *.csv; do
    echo "Processing $f"
done
```

Here is actual example for new blank post for a book:

```
cat > "content/books/the-signal-and-the-noise.md" << 'EOF'
---
title: "The Signal and the Noise"
author: "Nate Silver"
date: 2026-03-15
categories: ["Data & Statistics"]
tags: ["statistics", "data-analytics", "probability", "forecasting", "bayesian"]
description: "A tour through prediction across baseball, elections, finance and weather. The core argument is that most forecasters fail not from lack of data but from overconfidence in it."
showToc: false
---

Published in 2012, this is a field-by-field tour of how prediction works and why it so often fails. Silver's central thesis is that the explosion of available data has not made us better forecasters — if anything it has made things worse, because more data means more noise to mistake for signal. Drawing on case studies from weather forecasting, the 2008 financial crisis, earthquake prediction, poker, and elections, he makes the case for Bayesian reasoning as the practical antidote: start with a prior, update it incrementally as evidence arrives, and above all resist the temptation to express more certainty than your model actually supports. The finance and economics chapters are the most directly useful if that is your domain, and the gap between rated and actual risk in mortgage-backed securities is used to devastating effect to illustrate what happens when overconfident models meet correlated reality.

## Observations

Worth reading alongside *Quality of Earnings* — both books are ultimately about the same problem: the difference between what the numbers say and what is actually going on. Silver is readable and the cross-domain framing is genuinely illuminating, though the book is long and some chapters (baseball in particular) overstay their welcome. The Bayesian chapters are the ones to take notes on.
EOF
```

---

## File Structure

Here is the file structure of the page if you are looking to replicate the concept. I find basic web pages run this way are easy to manage, as you can edit file however you like. The site refreshes when you run hugo. There is back up shell script so that it copies (for the last 10 runs) each update. This can help you catch any errors.

```

├── archetypes
│   └── blog.md
├── assets
│   └── css
│       └── extended
│           └── custom-fonts.css
├── content
│   ├── about
│   │   ├── _index.md
│   │   └── about_index.md
│   ├── blog
│   │   ├── bjj
│   │   │   └── _index.md
│   │   ├── comp-science
│   │   │   └── _index.md
│   │   ├── credit-risk
│   │   │   ├── _index.md
│   │   │   └── enron-a-look-back.md
│   │   ├── data-analytics
│   │   │   └── _index.md
│   │   ├── economics
│   │   │   ├── _index.md
│   │   │   └── inflation-measurement.md
│   │   ├── other
│   │   │   └── _index.md
│   │   ├── philosophy
│   │   │   └── _index.md
│   │   ├── unhelpful_obs
│   │   │   └── my-post-title.md
│   │   ├── unhelpful-advice
│   │   │   ├── _index.md
│   │   │   ├── define-the-problem.md
│   │   │   └── definitions-matter.md
│   │   └── _index.md
│   ├── books
│   │   ├── _index.md
│   │   ├── art-of-doing-science-hamming.md
│   │   ├── art-of-statistics-spiegelhalter.md
│   │   ├── behave-sapolsky.md
│   │   ├── books-index.md
│   │   ├── brain-of-the-firm-beer.md
│   │   ├── challenger-higginbotham.md
│   │   ├── concise-history-of-warfare.md
│   │   ├── crashed-tooze.md
│   │   ├── debt-graeber.md
│   │   ├── deep-learning-goodfellow.md
│   │   ├── determined-sapolsky.md
│   │   ├── divine-comedy.md
│   │   ├── euro-stiglitz.md
│   │   ├── financial-shenanigans.md
│   │   ├── fm-22-100-army-leadership.md
│   │   ├── growth-susskind.md
│   │   ├── irrational-exuberance.md
│   │   ├── keeping-at-it-volcker.md
│   │   ├── life-is-simple-mcfadden.md
│   │   ├── lombard-street-bagehot.md
│   │   ├── mind-of-the-strategist-ohmae.md
│   │   ├── money-ferguson.md
│   │   ├── noise-kahneman.md
│   │   ├── on-competition-porter.md
│   │   ├── once-an-eagle.md
│   │   ├── price-of-time-chancellor.md
│   │   ├── quality-of-earnings.md
│   │   ├── radical-uncertainty-king-kay.md
│   │   ├── red-notice-browder.md
│   │   ├── royal-charter-bank-of-england.md
│   │   ├── smartest-guys-in-the-room.md
│   │   ├── spqr-beard.md
│   │   ├── stress-test-geithner.md
│   │   ├── the-signal-and-the-noise.md
│   │   ├── third-pillar-rajan.md
│   │   └── three-body-problem.md
│   └── _index.md
├── static
│   ├── data
│   │   ├── a-millennium-of-macroeconomic-data-for-the-uk.xlsx
│   │   └── Untitled.csv
│   └── images
│       ├── avatar.png
│       └── Figure 1_ Causes of the difference between the RPI and CPIH inflation rates, 2006 to 2018 .png
├── themes
│   └── PaperMod
│       ├── assets
│       │   ├── css
│       │   │   ├── common
│       │   │   │   ├── 404.css
│       │   │   │   ├── archive.css
│       │   │   │   ├── footer.css
│       │   │   │   ├── header.css
│       │   │   │   ├── main.css
│       │   │   │   ├── post-entry.css
│       │   │   │   ├── post-single.css
│       │   │   │   ├── profile-mode.css
│       │   │   │   ├── search.css
│       │   │   │   └── terms.css
│       │   │   ├── core
│       │   │   │   ├── license.css
│       │   │   │   ├── reset.css
│       │   │   │   ├── theme-vars.css
│       │   │   │   └── zmedia.css
│       │   │   ├── extended
│       │   │   │   └── blank.css
│       │   │   └── includes
│       │   │       ├── chroma-mod.css
│       │   │       ├── chroma-styles.css
│       │   │       └── scroll-bar.css
│       │   └── js
│       │       ├── fastsearch.js
│       │       ├── fuse.basic.min.js
│       │       └── license.js
│       ├── i18n
│       │   ├── ar.yaml
│       │   ├── be.yaml
│       │   ├── bg.yaml
│       │   ├── bn.yaml
│       │   ├── ca.yaml
│       │   ├── ckb.yaml
│       │   ├── cs.yaml
│       │   ├── da.yaml
│       │   ├── de.yaml
│       │   ├── el.yaml
│       │   ├── en.yaml
│       │   ├── eo.yaml
│       │   ├── es.yaml
│       │   ├── fa.yaml
│       │   ├── fi.yaml
│       │   ├── fr.yaml
│       │   ├── he.yaml
│       │   ├── hi.yaml
│       │   ├── hr.yaml
│       │   ├── hu.yaml
│       │   ├── id.yaml
│       │   ├── it.yaml
│       │   ├── ja.yaml
│       │   ├── ko.yaml
│       │   ├── ku.yaml
│       │   ├── mn.yaml
│       │   ├── ms.yaml
│       │   ├── nl.yaml
│       │   ├── no.yaml
│       │   ├── oc.yaml
│       │   ├── pa.yaml
│       │   ├── pl.yaml
│       │   ├── pnb.yaml
│       │   ├── pt.yaml
│       │   ├── ro.yaml
│       │   ├── ru.yaml
│       │   ├── sk.yaml
│       │   ├── sv.yaml
│       │   ├── sw.yaml
│       │   ├── th.yaml
│       │   ├── tr.yaml
│       │   ├── uk.yaml
│       │   ├── uz.yaml
│       │   ├── vi.yaml
│       │   ├── zh-tw.yaml
│       │   └── zh.yaml
│       ├── images
│       │   ├── screenshot.png
│       │   └── tn.png
│       ├── layouts
│       │   ├── _default
│       │   │   ├── _markup
│       │   │   │   └── render-image.html
│       │   │   ├── archives.html
│       │   │   ├── baseof.html
│       │   │   ├── index.json
│       │   │   ├── list.html
│       │   │   ├── llms.txt
│       │   │   ├── rss.xml
│       │   │   ├── search.html
│       │   │   ├── single.html
│       │   │   └── terms.html
│       │   ├── partials
│       │   │   ├── templates
│       │   │   │   ├── _funcs
│       │   │   │   │   └── get-page-images.html
│       │   │   │   ├── opengraph.html
│       │   │   │   ├── schema_json.html
│       │   │   │   └── twitter_cards.html
│       │   │   ├── anchored_headings.html
│       │   │   ├── author.html
│       │   │   ├── breadcrumbs.html
│       │   │   ├── comments.html
│       │   │   ├── cover.html
│       │   │   ├── edit_post.html
│       │   │   ├── extend_footer.html
│       │   │   ├── extend_head.html
│       │   │   ├── footer.html
│       │   │   ├── head.html
│       │   │   ├── header.html
│       │   │   ├── home_info.html
│       │   │   ├── index_profile.html
│       │   │   ├── post_canonical.html
│       │   │   ├── post_meta.html
│       │   │   ├── post_nav_links.html
│       │   │   ├── share_icons.html
│       │   │   ├── social_icons.html
│       │   │   ├── svg.html
│       │   │   ├── toc.html
│       │   │   └── translation_list.html
│       │   ├── shortcodes
│       │   │   ├── collapse.html
│       │   │   ├── figure.html
│       │   │   ├── inTextImg.html
│       │   │   ├── ltr.html
│       │   │   ├── rawhtml.html
│       │   │   └── rtl.html
│       │   ├── 404.html
│       │   └── robots.txt
│       ├── go.mod
│       ├── LICENSE
│       ├── README.md
│       └── theme.toml
├── backup.sh
├── bash script new book post.pages
├── blog update bash format.pages
├── config.toml
├── graph_helper.py
├── new-post.sh
├── publish.sh
└── README.md

```
---

The two pages files are just script saved into a Mac pages files as reminder. They don't impact the actual web page generated in html in any way.

---

*The views here are personal. They do not represent any employer, client, or institution.*

© 2026 onwards. All rights reserved.
