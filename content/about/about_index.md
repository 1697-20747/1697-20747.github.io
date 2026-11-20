---
title: "About"
layout: "single"
ShowReadingTime: false
ShowBreadCrumbs: false
hidemeta: true
---

This is a personal site. The writing here covers economics, data analytics, computer science, credit risk, philosophy, book notes, BJJ, and whatever else earns a place. The posts are notes made public — working through ideas, not finished arguments. The in development items on git are private during sessions, when completed or useful they are public. The projects tend to drift to real world edge computing cases, with hardware.

## The day job

Finance. Primarily credit — analysis, structure, the forensics of how things fail. Understanding failure is what builds an effective filter for what good looks like. If you have spent time reading financial statements with genuine scepticism rather than confirmation bias, you will find some common ground here.

## The rest of the time

Low-level programming on small devices. Embedded systems, constrained hardware, the kind of work where every byte is a negotiation. Most of the comp-science writing here sits at the intersection of that and machine learning — the plumbing beneath the tools everyone else uses without a second thought. None of this is the day job. It is personal time, chosen freely, and that distinction matters.

## On writing style

The analysis, thought process and commentary here are mine. Take the Enron piece: the read on what went wrong and why comes from my own experience, not a model's. What AI increasingly does is the re drafting — tightening sentences, cutting the flab, making an argument read more coherently. It writes better than I do. Sadly. Think of it as an editor's pass, not authorship. The informal phrasing is still a choice I keep control of — clarity does not require formality, and pretension is its own form of obscurity.

For boilerplate work I lean on AI more heavily still — it saves a lot of pain. Naming conventions for an LLM training corpus, for example: file names on the internet are generally awful and inconsistent, even for large cap banks they are a mess of inconsistency. . Agents are getting much more productive for repetitive tasks, such as scraping data from hundreds of pdfs.

## On social media

No. This is it. I post nonsense in a very small number of WhatsApp groups, and that is the full extent of it. If you want to get in touch, LinkedIn is in the footer. But I am not particularly interested. There is no comments section here — that is not the intended purpose.

## The name

`[1697, 20747]`

A tokenizer output. Run the name through a BPE tokenizer — GPT-family, if you are curious — and those are the token IDs you get back. If that means something to you, you are probably in the right place. If it does not, the writing should still be readable without it.

## Why?

As stated elsewhere: don't do anything without a developed problem statement. There are a few reasons for this site.

One, a repository to draw on much later for a variety of projects — it's structured text, so by default I can scrape it for curated training data. Two, a reminder to myself. Three, the discipline of writing things down: clear writing requires clear thinking. (Shame about my writing — I'm not too bad on the thinking.) Four, a practical purpose. With a varied background, I have always struggled to have a CV that actually covers my skill set; this site works as a much-expanded version of one. You can infer what I am good at, and not, from the contents, in a way a short-form CV can't manage. Lastly, in some manner, for my kids. Hopefully there are a few life lessons buried in here. They have heard them all already, but it might serve as a reminder one day. Books, much as I love them, are not for everyone — this is in essence a book, split across a few subjects, but easier to contain.

I hope the traditional CV dies and gets replaced by an actual skills framework. I have a lot of respect for people who can do the doing. 

I hope something here is useful to someone.

---

## Workflow

As for context, this is broadly how I work. I generate a new post in bash with the basic frontmatter, then do a brain dump of the post's essence, and edit for quality later. It's basic markdown with the odd code block. Hugo renders it, and the file structure is set up by hand. Other than VS Code, no Microsoft tools are involved — open source, all the way. Hopefully they don't ruin VS Code any time soon.

I use a lot of standalone scripts for this kind of work. Say, historical FX analysis from a CSV file: I'll take a manual look in VS Code or PyCharm until I have a feel for the shape of the data. Then, if I want a basic stats dashboard, I'll set up the workings in a standalone script — all the code contained, all libraries pinned in a requirements file. Slow is fast. Many of these longer posts are iterations; they won't be finished for years as I work through the backlog.

---

## AI and Agents

You have to move with the times. For coding sessions — say, at the end of a long one — I'll use AI to generate a full summary. This applies to larger projects (months-long) and gives me a record of the solution path over time, which shifts as the project goes. Agentic methods are getting more interesting. The agentic harness and MCP might become the new operating systems. Too early to tell, this stuff is barely 10 years old. In the main, I just try and make things that work, code and in real life.

---

*The views here are personal. They do not represent any employer, client, or institution.*

© 2026 onwards to the Author. All rights reserved.
