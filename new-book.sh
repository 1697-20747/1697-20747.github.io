#!/bin/bash
# new-book.sh — create a new book review post
# Usage: ./new-book.sh <slug> "Exact Title" "Author Name" "2025"
# Example: ./new-book.sh stress-test "Stress Test" "Timothy Geithner" "2014"

SLUG=${1:-"new-book"}
TITLE=${2:-"Book Title"}
AUTHOR=${3:-"Author Name"}
YEAR=${4:-""}
DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
FILEPATH="content/blog/books/$SLUG.md"

if [ -f "$FILEPATH" ]; then
  echo "❌ File already exists: $FILEPATH"
  exit 1
fi

cat <<EOL > "$FILEPATH"
---
title: "$TITLE"
author: "$AUTHOR"
date: $DATE
draft: false
categories: ["blog/books"]
tags: []
description: ""
showToc: false
---

{{< bookcover title="$TITLE" author="$AUTHOR" year="$YEAR" img="/images/book_img.png" >}}

Write your review here.
EOL

echo ""
echo "✅ Created: $FILEPATH"
echo "📝 Open and write your review."
echo "💡 Replace /images/book_img.png with a specific cover image if you have one."
