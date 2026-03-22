#!/bin/bash

SITE_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKUP_ROOT="$HOME/blog-backups"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_DIR="$BACKUP_ROOT/$TIMESTAMP"

mkdir -p "$BACKUP_DIR"

rsync -av --exclude="public/" --exclude=".git/" "$SITE_DIR/" "$BACKUP_DIR/"

ls -dt "$BACKUP_ROOT"/*/ | tail -n +11 | xargs rm -rf

echo ""
echo "Backup complete: $BACKUP_DIR"
echo "Size: $(du -sh "$BACKUP_DIR" | cut -f1)"
echo "Total backups kept: $(ls -d "$BACKUP_ROOT"/*/ | wc -l | tr -d ' ')"
