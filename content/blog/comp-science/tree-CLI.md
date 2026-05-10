---
title: "Tree CLI"
date: 2026-04-07T10:04:08Z
draft: false
categories: ["comp-science"]
tags: []
description: "Quick reminder/overview on tree CLI tool."
showToc: true
tocopen: false
cover:
  image: ""
  alt: ""
  caption: ""
---

# tree (CLI tool) — Quick Summary

**tree** is a command-line utility that prints a directory structure in a hierarchical, tree-like format, making it easy to visualize files and folders.

---

## Documentation
- Official-style guide: https://cmdbox.mikihands.com/en/tree/  
- Linux manual overview: https://www.systutorials.com/docs/linux/man/1-tree/  

---

## Basic Usage

```bash
tree [options] [directory]
```

- If no directory is provided → runs on current directory  
- Recursively lists all files/subdirectories  
- Output is indented to show hierarchy  

**Examples**
```bash
tree
tree /path/to/project
tree -L 2
```

---

## Most Useful Commands

| Command | Description |
|--------|------------|
| `tree` | Show full directory tree |
| `tree -L 2` | Limit depth (2 levels) |
| `tree -a` | Include hidden files |
| `tree -d` | Show directories only |
| `tree -f` | Show full file paths |
| `tree -I pattern` | Exclude files/dirs matching pattern |
| `tree --help` | Show all options |

`tree -d -L 2` is one I use all the time. Watch the spaces, syntax matters.

---

## Key Concepts

- Recursively traverses directories  
- Displays structure visually (like branches of a tree)  
- Useful for:
  - Exploring projects
  - Documentation
  - Debugging file layouts
  - Adjusting scale of branching to reduce noise 

---

## Install (if missing)

```bash
# Ubuntu / Debian
sudo apt install tree
```
On mac's, use Homebrew. Sudo stands for “superuser do”. It’s a command on macOS (and Linux) that lets you run other commands with administrator (root) privileges. Sudo can be (potentially) more dangerous if you don't *really* know what you are doing.

What it does:
* Runs commands as root user
* Can modify any file on your system
* Can bypass macOS protections (partially)

```bash
# Homebrew is used, checks if it is installed or not. Skip if you don't want to use homebrew.
which brew >/dev/null 2>&1 || /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && \
brew install tree && \
tree --version && \
tree -L 2
```
---

## When to Use Tree

- Understanding unfamiliar codebases  
- Generating quick documentation  
- Debugging file organisation  

