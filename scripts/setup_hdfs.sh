#!/bin/bash

set -euo pipefail

# Usage: setup_hdfs.sh [LOCAL_BOOKS_DIR] [HDFS_BASE_PATH]
# Example: ./setup_hdfs.sh ./books /user/hduser/digital-librarian

LOCAL_BOOKS_DIR=${1:-"./books"}
HDFS_BASE=${2:-"/user/hduser/digital-librarian"}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STOPWORDS_LOCAL="${SCRIPT_DIR}/../resources/stopwords.txt"

echo "HDFS setup: base=${HDFS_BASE}, local_books=${LOCAL_BOOKS_DIR}"
echo "Stopwords file: ${STOPWORDS_LOCAL}"

echo "Creating HDFS directories..."
hdfs dfs -mkdir -p "${HDFS_BASE}/input"
hdfs dfs -mkdir -p "${HDFS_BASE}/stopwords"
hdfs dfs -mkdir -p "${HDFS_BASE}/output"
hdfs dfs -mkdir -p "${HDFS_BASE}/logs"

echo "Setting permissions (755) on ${HDFS_BASE}"
hdfs dfs -chmod -R 755 "${HDFS_BASE}" || true

echo "Uploading stopwords..."
if [ -f "${STOPWORDS_LOCAL}" ]; then
	hdfs dfs -put -f "${STOPWORDS_LOCAL}" "${HDFS_BASE}/stopwords/" && \
		echo "Stopwords uploaded successfully to ${HDFS_BASE}/stopwords/stopwords.txt"
else
	echo "Error: ${STOPWORDS_LOCAL} not found; stopwords are required!" >&2
	exit 1
fi

echo "Uploading books from ${LOCAL_BOOKS_DIR} (if present)"
if [ -d "${LOCAL_BOOKS_DIR}" ]; then
	# Only upload files (not directories) from the local books dir
	shopt -s nullglob
	files=("${LOCAL_BOOKS_DIR}"/*)
	if [ ${#files[@]} -gt 0 ]; then
		for f in "${LOCAL_BOOKS_DIR}"/*; do
			if [ -f "$f" ]; then
				echo "Uploading $f -> ${HDFS_BASE}/input/"
				hdfs dfs -put -f "$f" "${HDFS_BASE}/input/"
			fi
		done
	else
		echo "No files found in ${LOCAL_BOOKS_DIR}; nothing uploaded." >&2
	fi
else
	echo "Warning: Local books directory ${LOCAL_BOOKS_DIR} not found; skipping upload." >&2
fi

echo "Verifying HDFS contents:"
hdfs dfs -ls -R "${HDFS_BASE}" || true

echo "HDFS setup complete."

# End of script
