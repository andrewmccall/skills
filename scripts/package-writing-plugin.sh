#!/usr/bin/env bash

set -euo pipefail

source_dir="skills/writing/"
package_dir="plugins/writing/skills/"

if [[ ! -d "$source_dir" ]]; then
  echo "Missing canonical writing skills at $source_dir" >&2
  exit 1
fi

mkdir -p "$package_dir"
rsync --archive --delete --exclude='.DS_Store' "$source_dir" "$package_dir"
