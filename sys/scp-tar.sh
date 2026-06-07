#!/usr/bin/env bash
set -euo pipefail

show_usage() {
  cat <<USAGE
Usage:
  ssh-tgz-cp <source> <destination>

Format:
  local_path
  server:/remote/path
  user@server:/remote/path

Examples:
  # Download
  ssh-tgz-cp server:/path/to/file .
  ssh-tgz-cp server:/path/to/directory ./downloads/
  ssh-tgz-cp server:/path/to/directory ./renamed_directory

  # Upload
  ssh-tgz-cp ./file server:/path/to/destination/
  ssh-tgz-cp ./directory server:/path/to/destination/
  ssh-tgz-cp ./directory server:/path/to/renamed_directory

Destination behavior:
  - If destination exists as a directory, the source basename is kept under it.
  - If destination ends with '/', it is treated as a directory and created if needed.
  - Otherwise, the source is copied to that exact destination path.

Requirements:
  - ssh access to the remote server
  - bash, tar, gzip, du on both local and remote machines
  - optional: pv on the local machine for progress display
USAGE
}

is_remote_spec() {
  [[ "$1" =~ ^([^/:]+@)?[^/:]+:.+ ]] && [[ "$1" != ./* ]] && [[ "$1" != ../* ]] && [[ "$1" != /* ]]
}

parse_remote_host() {
  printf '%s' "${1%%:*}"
}

parse_remote_path() {
  printf '%s' "${1#*:}"
}

quote_for_remote_shell() {
  printf '%q' "$1"
}

has_trailing_slash() {
  [[ "$1" == */ ]]
}

local_size_bytes() {
  du -sb -- "$1" | awk '{print $1}'
}

remote_size_bytes() {
  local host="$1"
  local path="$2"
  local path_q
  path_q=$(quote_for_remote_shell "$path")

  ssh "$host" "bash -s -- $path_q" <<'REMOTE_SIZE_SCRIPT'
set -euo pipefail
remote_path=$1

case "$remote_path" in
  "~")
    remote_path="$HOME"
    ;;
  "~/"*)
    remote_path="$HOME/${remote_path#~/}"
    ;;
esac

if [[ ! -e "$remote_path" ]]; then
  echo "Error: remote source does not exist: $remote_path" >&2
  exit 2
fi

du -sb -- "$remote_path" | awk '{print $1}'
REMOTE_SIZE_SCRIPT
}

make_local_tar() {
  local src="$1"

  if [[ ! -e "$src" ]]; then
    echo "Error: local source does not exist: $src" >&2
    exit 2
  fi

  local parent_dir
  local item_name
  parent_dir=$(dirname -- "$src")
  item_name=$(basename -- "$src")

  cd -- "$parent_dir"
  tar -cf - -- "$item_name"
}

make_remote_tar_gz() {
  local host="$1"
  local path="$2"
  local path_q
  path_q=$(quote_for_remote_shell "$path")

  ssh "$host" "bash -s -- $path_q" <<'REMOTE_TAR_SCRIPT'
set -euo pipefail
remote_path=$1

case "$remote_path" in
  "~")
    remote_path="$HOME"
    ;;
  "~/"*)
    remote_path="$HOME/${remote_path#~/}"
    ;;
esac

if [[ ! -e "$remote_path" ]]; then
  echo "Error: remote source does not exist: $remote_path" >&2
  exit 2
fi

parent_dir=$(dirname -- "$remote_path")
item_name=$(basename -- "$remote_path")

cd -- "$parent_dir"
tar -cf - -- "$item_name" | gzip -1
REMOTE_TAR_SCRIPT
}

extract_tar_to_local_destination() {
  local dst="$1"

  if [[ -d "$dst" ]] || has_trailing_slash "$dst"; then
    mkdir -p -- "$dst"
    tar --no-same-owner -xf - -C "$dst"
  else
    local parent_dir
    local tmp_dir
    local item_count
    local item_path

    parent_dir=$(dirname -- "$dst")
    mkdir -p -- "$parent_dir"
    tmp_dir=$(mktemp -d "$parent_dir/.ssh-tgz-cp.XXXXXX")

    tar --no-same-owner -xf - -C "$tmp_dir"

    item_count=$(find "$tmp_dir" -mindepth 1 -maxdepth 1 -print | wc -l)
    if [[ "$item_count" -ne 1 ]]; then
      echo "Error: archive should contain exactly one top-level item, got $item_count" >&2
      rm -rf -- "$tmp_dir"
      exit 3
    fi

    item_path=$(find "$tmp_dir" -mindepth 1 -maxdepth 1 -print -quit)
    rm -rf -- "$dst"
    mv -T -- "$item_path" "$dst"
    rmdir -- "$tmp_dir"
  fi
}

extract_gzipped_tar_to_remote_destination() {
  local host="$1"
  local path="$2"
  local path_q
  path_q=$(quote_for_remote_shell "$path")

  ssh "$host" "bash -s -- $path_q" <<'REMOTE_EXTRACT_SCRIPT'
set -euo pipefail
remote_dest=$1

case "$remote_dest" in
  "~")
    remote_dest="$HOME"
    ;;
  "~/"*)
    remote_dest="$HOME/${remote_dest#~/}"
    ;;
esac

if [[ -d "$remote_dest" || "$remote_dest" == */ ]]; then
  mkdir -p -- "$remote_dest"
  gzip -d | tar --no-same-owner -xf - -C "$remote_dest"
else
  parent_dir=$(dirname -- "$remote_dest")
  mkdir -p -- "$parent_dir"
  tmp_dir=$(mktemp -d "$parent_dir/.ssh-tgz-cp.XXXXXX")

  gzip -d | tar --no-same-owner -xf - -C "$tmp_dir"

  item_count=$(find "$tmp_dir" -mindepth 1 -maxdepth 1 -print | wc -l)
  if [[ "$item_count" -ne 1 ]]; then
    echo "Error: archive should contain exactly one top-level item, got $item_count" >&2
    rm -rf -- "$tmp_dir"
    exit 3
  fi

  item_path=$(find "$tmp_dir" -mindepth 1 -maxdepth 1 -print -quit)
  rm -rf -- "$remote_dest"
  mv -T -- "$item_path" "$remote_dest"
  rmdir -- "$tmp_dir"
fi
REMOTE_EXTRACT_SCRIPT
}

download_remote_to_local() {
  local src="$1"
  local dst="$2"
  local host
  local remote_path
  local size

  host=$(parse_remote_host "$src")
  remote_path=$(parse_remote_path "$src")

  echo "Mode: download"
  echo "Source:      $host:$remote_path"
  echo "Destination: $dst"
  echo

  size=$(remote_size_bytes "$host" "$remote_path" || true)
  if ! [[ "$size" =~ ^[0-9]+$ ]]; then
    size=""
  fi

  if command -v pv >/dev/null 2>&1 && [[ -n "$size" ]]; then
    make_remote_tar_gz "$host" "$remote_path" \
      | gzip -d \
      | pv -s "$size" \
      | extract_tar_to_local_destination "$dst"
  else
    if ! command -v pv >/dev/null 2>&1; then
      echo "Note: pv is not installed locally, continuing without progress display." >&2
    fi

    make_remote_tar_gz "$host" "$remote_path" \
      | gzip -d \
      | extract_tar_to_local_destination "$dst"
  fi
}

upload_local_to_remote() {
  local src="$1"
  local dst="$2"
  local host
  local remote_path
  local size

  if [[ ! -e "$src" ]]; then
    echo "Error: local source does not exist: $src" >&2
    exit 2
  fi

  host=$(parse_remote_host "$dst")
  remote_path=$(parse_remote_path "$dst")
  size=$(local_size_bytes "$src")

  echo "Mode: upload"
  echo "Source:      $src"
  echo "Destination: $host:$remote_path"
  echo

  if command -v pv >/dev/null 2>&1 && [[ "$size" =~ ^[0-9]+$ ]]; then
    make_local_tar "$src" \
      | pv -s "$size" \
      | gzip -1 \
      | extract_gzipped_tar_to_remote_destination "$host" "$remote_path"
  else
    if ! command -v pv >/dev/null 2>&1; then
      echo "Note: pv is not installed locally, continuing without progress display." >&2
    fi

    make_local_tar "$src" \
      | gzip -1 \
      | extract_gzipped_tar_to_remote_destination "$host" "$remote_path"
  fi
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  show_usage
  exit 0
fi

if [[ $# -ne 2 ]]; then
  show_usage >&2
  exit 1
fi

SOURCE="$1"
DESTINATION="$2"

SOURCE_IS_REMOTE=0
DESTINATION_IS_REMOTE=0

if is_remote_spec "$SOURCE"; then
  SOURCE_IS_REMOTE=1
fi

if is_remote_spec "$DESTINATION"; then
  DESTINATION_IS_REMOTE=1
fi

if [[ "$SOURCE_IS_REMOTE" -eq 1 && "$DESTINATION_IS_REMOTE" -eq 0 ]]; then
  download_remote_to_local "$SOURCE" "$DESTINATION"
elif [[ "$SOURCE_IS_REMOTE" -eq 0 && "$DESTINATION_IS_REMOTE" -eq 1 ]]; then
  upload_local_to_remote "$SOURCE" "$DESTINATION"
elif [[ "$SOURCE_IS_REMOTE" -eq 1 && "$DESTINATION_IS_REMOTE" -eq 1 ]]; then
  echo "Error: remote-to-remote transfer is not supported." >&2
  exit 1
else
  echo "Error: either source or destination must be remote, e.g. server:/path." >&2
  exit 1
fi

echo
echo "Transfer completed."
