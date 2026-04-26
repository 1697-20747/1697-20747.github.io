---
title: "The Big Give Away"
date: 2026-04-12T09:52:19Z
draft: true
categories: ["comp-science"]
tags: []
description: "A short summary shown in post listings."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

## Overview

My oh my, there are mistakes, and then there are mistakes.... This one is going down in the history books of comp science.

---

## Claude code got completely forked...

On 31 march 2026, for about 3 hours, Anthropic accidentally released a large chunk of the source code, some 512,000 lines. 1,906 TypeScript files. 44 hidden feature flags. Ouch. The internet was all over this like a rash in a heartbeat. The takedown was too late, damage done. Conspiracy theorists unite to have a field day on it being on the cusp of April's Fools day.

The how was a problem in npm, a topic for a whole other post at some point. So not using .npmignore is reported as the cause. But in brief, npm is package manager fro node.js. If you use the internet, you have used the product of this.  There are a lot of package managers around such uv (for python, if you are not scared of potential problems), etc. PHP was an old school one, that worked pretty well actually fro the early web. pip is the one you are most likely to have come across. npm is github, now microsoft. You cannot develop software without package managers. They are mostly open sourced in origin, which is the problematic bit for security. As languages evolved, package managers are essential infrastructure. Maintained by......? Exactly. What do they do, they manage dependencies and environments. And a lot more. But you have called scipy in some of your code. Scipy changes in one of the functions in the library. Without depreciation management, your code won't work. It is of course way more complicated than that, but you get the gist.

This is now a key date in the history of software development, like it or not. I would not like to be the poor dev ops person whose name is on this. At least one day they will be famous for missing the most expensive missing characters in modern computing. Even nasa screwing up metric and imperial units only cost a sliver of what this one did, as at mere $125m in 1999. That was quite a bit of money to spread some broken bits and pieces over Mars surface. The acceleration readings measured in English units of pound-seconds^2, needed force in newton-seconds^2. Whoops.

Life is not perfect, neither is any of us.

```
*.map
dist/*.map
```

Apparently that's the missing bit, but I am no expert on npm. Possibly half a billion per character.


> Overview of Python Packaging
As a general-purpose programming language, Python is designed to be used in many ways. You can build web sites or industrial robots or a game for your friends to play, and much more, all using the same core technology. Python’s flexibility is why the first step in every Python project must be to think about the project’s audience and the corresponding environment where the project will run. It might seem strange to think about packaging before writing code, but this process does wonders for avoiding future headaches. This overview provides a general-purpose decision tree for reasoning about Python’s plethora of packaging options. Read on to choose the best technology for your next project. Source: [PIP documentation](https://packaging.python.org/en/latest/overview/)

Fun fact. Python the programming language, now dominant in machine learning, is indeed named after Monty Python. pyPI, the Python Package Indexer was originally called Cheese Shop, after the skit of the same name. Apparently in the governance meeting back in the day they thought that was a bit too much, so the changed it back to pyPI. Fact, not speculation. Source: https://packaging.python.org/en/latest/overview/ Also, listeners of Practical AI have heard the first person discussion of the meeting. Shout out to [Practical AI podcast](https://practicalai.fm/) for giving it to us straight. Their discussion on the Claude release is insightful, that is the origin of the path to open source speculation below.


---

## Key Takeaways

- The cat is out of the bag. it is never going back in, ever. Open Source is probably the only path left now.
- Lawsuits left right and centre when you give away billions in valuations.
- Discovery will be interesting, as a lot of speculation will be resolved in the disclosures.

---

## References

- [Claude Code Leak](https://dev.to/varshithvhegde/the-great-claude-code-leak-of-2026-accident-incompetence-or-the-best-pr-stunt-in-ai-history-3igm)
