#!/bin/bash

# Prompt for commit message
read -p "Enter commit message: " msg

# Check if empty
if [ -z "$msg" ]; then
  echo "❌ Commit message cannot be empty"
  exit 1
fi

# Run git commands
git add .
git commit -m "$msg"
git push

echo "✅ Changes pushed with message: $msg"