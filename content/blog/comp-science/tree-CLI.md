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

## 📚 Documentation
- Official-style guide: https://cmdbox.mikihands.com/en/tree/  
- Linux manual overview: https://www.systutorials.com/docs/linux/man/1-tree/  

---

## ⚙️ Basic Usage

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

## 🔑 Most Useful Commands

| Command | Description |
|--------|------------|
| `tree` | Show full directory tree |
| `tree -L 2` | Limit depth (2 levels) |
| `tree -a` | Include hidden files |
| `tree -d` | Show directories only |
| `tree -f` | Show full file paths |
| `tree -I pattern` | Exclude files/dirs matching pattern |
| `tree --help` | Show all options |

`tree - d -L 2` is one I use all the time.

---

## 🧠 Key Concepts

- Recursively traverses directories  
- Displays structure visually (like branches of a tree)  
- Useful for:
  - Exploring projects
  - Documentation
  - Debugging file layouts  

---

## ⚡ Install (if missing)

```bash
# Ubuntu / Debian
sudo apt install tree
```

---

## ✅ When to Use

- Understanding unfamiliar codebases  
- Generating quick documentation  
- Debugging file organisation  

