#!/bin/bash
# new-book.sh — create a new book review post
# Usage: ./new-book.sh <slug> "Exact Title"

SLUG=${1:-"new-book"}
TITLE=${2:-"Book Title"}
DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
FILEPATH="content/blog/books/$SLUG.md"

if [ -f "$FILEPATH" ]; then
  echo "❌ File already exists: $FILEPATH"
  exit 1
fi

cat <<EOL > "$FILEPATH"
---
title: "$TITLE"
date: $DATE
draft: false
categories: ["blog/books"]
tags: []
description: ""
showToc: false
---

Write your review here.
EOL

echo ""
echo "✅ Created: $FILEPATH"
echo "📝 Open and write your review."
