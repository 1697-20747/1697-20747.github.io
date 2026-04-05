#!/bin/bash
# new-advice.sh — create a new Unhelpful Advice post (single paragraph only)
# Usage: ./new-advice.sh <post-slug> [exact title]
# Example: ./new-advice.sh never-trust-a-spreadsheet
# Example: ./new-advice.sh never-trust-a-spreadsheet "Never Trust a Spreadsheet"
# This version Mar 22 2026

SLUG=${1:-"new-advice"}
EXACT_TITLE=${2:-""}

DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
FILEPATH="content/blog/unhelpful-advice/$SLUG.md"

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
mkdir -p "content/blog/unhelpful-advice"

cat <<EOL > "$FILEPATH"
---
title: "$TITLE"
date: $DATE
draft: false
categories: ["unhelpful-advice"]
tags: []
description: ""
showToc: false
tocopen: false
---

> Your text here.
EOL

echo ""
echo "✅ Created: $FILEPATH"
echo "📝 Title:   $TITLE"
echo "📝 Open it and replace 'Your text here.' with your content."
echo "🌐 Preview with: hugo server -D"
