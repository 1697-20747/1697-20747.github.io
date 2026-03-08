# Hugo PaperMod Blog Setup

This README explains how to set up and maintain your Hugo blog using the PaperMod theme, including a fix for header rendering errors that were causing your site to fail.

---

## 1. Prerequisites

- [Hugo](https://gohugo.io/getting-started/installing/) installed (v1.0+ recommended)
- Git installed
- Basic knowledge of Markdown and TOML

---

## 2. Project Structure

Your project should follow this structure:

project-root/
├── archetypes/
├── config.toml
├── content/
│   ├── about/
│   ├── blog/
│   │   ├── economics/
│   │   ├── data-analytics/
│   │   ├── comp-science/
│   │   ├── other/
│   │   ├── philosophy/
│   │   └── bjj/
│   └── books/
├── data/
├── public/
├── themes/
│   └── PaperMod/
└── README.md

---

## 3. Config File (`config.toml`)

Ensure your `config.toml` includes the menu with weights:

```toml
[menu]
  [[menu.main]]
    identifier = "economics"
    name = "Economics"
    url = "/categories/economics/"
    weight = 10

  [[menu.main]]
    identifier = "data-analytics"
    name = "Data Analytics"
    url = "/categories/data-analytics/"
    weight = 20

  [[menu.main]]
    identifier = "books"
    name = "Books"
    url = "/books/"
    weight = 50

Notes:
	•	Every menu item needs a weight if you want them sorted.
	•	For blog posts, you can use default sorting by date instead of weight.

⸻

4. Fixing the Header Issue

If you encounter errors like:

Notes:
	•	Every menu item needs a weight if you want them sorted.
	•	For blog posts, you can use default sorting by date instead of weight.

⸻

4. Fixing the Header Issue

If you encounter errors like:

error calling sort: can't sort string

This is caused by the theme attempting to sort a non-existent variable or incorrectly typed data.

Header Partial Fix (themes/PaperMod/layouts/partials/header.html):

Replace the <ul id="menu">...</ul> section with:

<ul id="menu">
  {{- $currentPage := . }}

  {{- /* Use main menu directly, without sorting strings */}}
  {{- range .Site.Menus.main }}
    <li>
      <a href="{{ .URL }}" {{ if eq $.Permalink .URL }}class="active"{{ end }}>
        {{ .Name }}
      </a>
    </li>
  {{- end }}
</ul>

Important:
	•	Avoid using sort "Weight" on a string that isn’t numeric.
	•	Ensure all menu items in config.toml have numeric weight.

5. Creating New Blog Posts

Use the following bash command:

#!/bin/bash
# new-post.sh
# Usage: ./new-post.sh "Post Title" category

TITLE="$1"
CATEGORY="$2"
DATE=$(date -Iseconds)
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g')

mkdir -p "content/blog/$CATEGORY/$SLUG"
cat > "content/blog/$CATEGORY/$SLUG/index.md" <<EOL
---
title: "$TITLE"
date: $DATE
draft: true
categories: ["$CATEGORY"]
tags: []
description: "A short summary."
showToc: true
tocopen: false
---
Write your post content here.
EOL

echo "Created new post at content/blog/$CATEGORY/$SLUG/index.md"

Notes:
	•	CATEGORY must match an existing subfolder under content/blog/.
	•	Draft posts (draft: true) won’t show until hugo server -D is used.

hugo server -D --disableFastRender

	•	-D includes drafts.
	•	--disableFastRender ensures full rebuilds, useful after template changes.

⸻

7. Adding Static Pages (About, Books)

Static pages (like About or Books) do not need weights but should be referenced in your header menu:

{{- $staticPages := slice "about" "books" }}
{{- range $staticPages }}
  {{- with site.GetPage . }}
    <li>
      <a href="{{ .Permalink }}">{{ .Title }}</a>
    </li>
  {{- end }}
{{- end }}

roubleshooting
	•	Duplicate blog folders: Keep only one content/blog/ folder with subfolders for each category.
	•	Index files: Each folder under content/blog/ should have _index.md.
	•	Sorting errors: Ensure you are sorting numeric weights or dates, not strings.
	•	Header errors: Replace <sort "Weight"> with the safe loop shown above.

References
	•	Hugo Documentation￼
	•	PaperMod Theme￼

---

To save it:

1. Open a terminal.
2. Navigate to your project root.
3. Run:

```bash
nano README.md

