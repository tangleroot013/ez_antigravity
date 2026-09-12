#!/bin/bash
# Carter's Atomic Workspace Backup
# Quack! One command to save the entire pond.

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
BACKUP_NAME="workspace_backup_${TIMESTAMP}.tar.gz"
BACKUP_PATH="backups/${BACKUP_NAME}"

echo "🦆 Creating atomic backup: ${BACKUP_NAME}"

# Create backup excluding ignored files and .git
tar --exclude='.git' --exclude='.venv' --exclude='__pycache__' \
    --exclude='*.pyc' --exclude='backups/*' -czf "${BACKUP_PATH}" .

echo "✅ Backup created at ${BACKUP_PATH}"
echo "💡 To restore: tar -xzf ${BACKUP_PATH}"
