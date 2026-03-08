#!/bin/bash
# publish.sh — run from your site root to push a new post live
# Usage: ./publish.sh "commit message"

set -e

MSG=${1:-"new post"}

echo "🔍 Building site locally to check for errors..."
hugo --minify

echo "📦 Staging changes..."
git add .

echo "💬 Committing: $MSG"
git commit -m "$MSG"

echo "🚀 Pushing to GitHub (Netlify will auto-deploy)..."
git push origin main

echo "✅ Done! Your site will update in ~30 seconds at your Netlify URL."
