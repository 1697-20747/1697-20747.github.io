#!/bin/bash
# new-post.sh — create a new blog post
# Usage: ./new-post.sh <category> <post-slug> [exact title]
# Example: ./new-post.sh economics my-post-title
# Example: ./new-post.sh credit-risk one-ring-to-rule-them-all "One Ring to Rule them All...."
# This version Mar 08 2026 19:31

CATEGORY=${1:-"other"}
SLUG=${2:-"new-post"}
EXACT_TITLE=${3:-""}

# Validate category
VALID=("economics" "data-analytics" "comp-science" "other" "philosophy" "bjj" "unhelpful-advice" "credit-risk")
if [[ ! " ${VALID[@]} " =~ " ${CATEGORY} " ]]; then
  echo "❌ Invalid category. Choose from: economics | data-analytics | comp-science | other | philosophy | bjj | unhelpful-advice | credit-risk"
  exit 1
fi

DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
FILEPATH="content/blog/$CATEGORY/$SLUG.md"

# Don't overwrite existing posts
if [ -f "$FILEPATH" ]; then
  echo "❌ File already exists: $FILEPATH"
  exit 1
fi

# Use exact title if provided, otherwise auto-capitalise from slug
if [ -n "$EXACT_TITLE" ]; then
  TITLE="$EXACT_TITLE"
else
  TITLE=$(echo $SLUG | tr '-' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2); print}')
fi

# Create category directory if it doesn't exist
mkdir -p "content/blog/$CATEGORY"

cat <<EOL > "$FILEPATH"
---
title: "$TITLE"
date: $DATE
draft: true
categories: ["$CATEGORY"]
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

Write your introduction here.

---

## Section One

Your content here. You can use **bold**, *italic*, and \`inline code\`.

---

## Key Takeaways

- Point one
- Point two
- Point three

---

## References

- [Source title](https://url.com)
EOL

echo ""
echo "✅ Created: $FILEPATH"
echo "📝 Title:   $TITLE"
echo "📝 Open it, set draft: false when ready to publish."
echo "🌐 Preview with: hugo server -D"
