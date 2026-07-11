---
title: "About"
layout: "single"
ShowReadingTime: false
ShowBreadCrumbs: false
hidemeta: true
---

This is a personal site. The writing here covers economics, data analytics, computer science, credit risk, philosophy, and whatever else earns a place. The posts are notes made public — working through ideas, not finished arguments.

## The day job

Finance. Primarily credit — analysis, structure, the forensics of how things fail to enable an effective fiter for what good looks like. If you have spent time reading financial statements with genuine scepticism rather than confirmation bias, you will find some common ground here.

## The rest of the time

Low-level programming on small devices. Embedded systems, constrained hardware, the kind of work where the use of every byte is a negotiation. Some of this requires a working understanding of machine learning, which means most of the comp science writing here sits at that intersection — the plumbing beneath the tools everyone else uses without thinking about. I have spent a lot of time on machine learning in the last few years. None of the comp science is the day job. It is personal time, chosen freely. That distinction matters.

## On writing style

The text, thought process and commentary in the main is not AI generated. The informal phrasing is deliberate — clarity does not require formality, and pretension is its own form of obscurity. If a sentence is clumsy it is because the thought behind it was still being worked out, not because a language model hallucinated it into existence. But, a caveat. For boiler plate analysis bits I am using AI more now, it saves a lot of pain. For example file naming conventions for corpus for LLM training. File names on the internet are generally awful. Getting AI to write a quick python script to apply naming conventions for a few hundred files is a joy. Compared to the alternative. I'll have to ponder an honest way to flag AI wording, eg one paragraph article summary and the like.

## On social media

No. This is it. I post nonsense is a very small number of WhatsApp groups, and that is the full extent of it. If you want to get in touch, LinkedIn is in the footer. But I am not particularly interested. There is no comments section here, that is not the intended purpose.

## The name

`[1697, 20747]`

A tokenizer output. Run the name through a BPE tokenizer — GPT-family, if you are curious — and those are the token IDs you get back. If that means something to you, you are probably in the right place. If it does not, the writing should still be readable without it.

## Why?

As stated elsewhere, don't do anything without a problem statement that has been developed. There are a couple of reasons why for this site. One is a repository to use, much later, to post train a smaller LLM. It requires structured text, so by default I can scrape this site to use for curated training data. Second, a reminder for myself. Third, the discipline of writing things down. Clear writing requires clear thinking. Shame about my writing, I am not too horrible on the thinking aspect. Fourth, it serves a practical purpose. With a varied background, I have always struggled with have a CV that actually covers my skill set. This site acts as a very expanded skill set description. You can infer what I am good at, or not, from the contents, in a manner impossible in a short form CV. Lastly, in some manner for my kids. Hopefully some life lessons buried in here somewhere. They have heard them all, but it might be a reminder one day. Books, as much as I love them, are not for everyone. This is in essence a book, split across a few subjects. But easier to contain.

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

I tend to use a lot of bash files for my work. So for say historical fx analysis from a csv file, I will take a look manually in VS Studio or Pycharm until I have a feel for the shape of the data. Then, lets say I want a basic stats dashboard, I will almost always set up the workings in a stand alone bash file, all the code contained, all libraries referenced in a requirements file. Slow is fast. It is easier to go back to, cleaner. And faster, as if you need to you can just change the csv or other file with fresh data, then re run the analysis on one go by running the same bash.sh file, with no changes. If you are careful with your work and content in the bash scripts, I find it very helpful. Also, you back track to edit out errors. Good luck with that using AI. To be clear, I often use AI for methods within the bash files, but I keep the work in manner that I can replicate it as needs be. AI for writing slabs of python? Yes. Running the numbers, bash scripts in the main. It gives you repeatability with no hallucination risk. A lot of these larger post are iterations, they won't be finished for perhaps years as I get through the backlog.


---

## File Structure

Here is the file structure of the page if you are looking to replicate the concept. I find basic web pages run this way are easy to manage, as you can edit file however you like. I do not like auto generators, you lose control very quickly. Its not fancy, but it works. I can strip out that data quite easily afterwards. The site refreshes when you run hugo. There is back up shell script so that it copies (for the last 10 runs) each update. This can help you catch any errors.

```
.
├── archetypes
├── assets
│   └── css
├── content
│   ├── about
│   └── blog
├── layouts
│   ├── blog
│   ├── partials
│   └── shortcodes
├── public
│   ├── about
│   ├── assets
│   ├── blog
│   ├── books
│   ├── categories
│   ├── css
│   ├── data
│   ├── economics
│   ├── images
│   ├── js
│   ├── New Folder With Items
│   ├── page
│   ├── tags
│   └── tools
├── resources
│   └── _gen
├── static
│   ├── css
│   ├── data
│   ├── images
│   ├── js
│   └── tools
└── themes
    └── PaperMod

```
---



---

*The views here are personal. They do not represent any employer, client, or institution.*

© 2026 onwards to the Author. All rights reserved.
