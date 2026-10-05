#!/usr/bin/env bash
set -euo pipefail
if [[ ! -d skills/engineering/ ]]; then
  echo 'Missing canonical engineering skills' >&2
  exit 1
fi
mkdir -p plugins/engineering/skills/
rsync --archive --delete --exclude='.DS_Store' --exclude='__pycache__' --exclude='*.pyc' skills/engineering/ plugins/engineering/skills/
