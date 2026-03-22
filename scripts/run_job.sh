#!/bin/bash

set -euo pipefail

# Usage: run_job.sh [NUM_REDUCERS]
# Example: ./run_job.sh 3
# Default: 2 reducers

NUM_REDUCERS=${1:-2}

# HDFS paths
HDFS_INPUT="/user/hduser/digital-librarian/input"
HDFS_OUTPUT="/user/hduser/digital-librarian/output"
HDFS_STOPWORDS="/user/hduser/digital-librarian/stopwords/stopwords.txt"

# Project paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="${SCRIPT_DIR}/.."
JAR_NAME="digital-librarian-1.0-SNAPSHOT.jar"
JAR_PATH="${ROOT_DIR}/target/${JAR_NAME}"

echo "========================================"
echo "Digital Librarian MapReduce Job"
echo "========================================"
echo "Input: ${HDFS_INPUT}"
echo "Output: ${HDFS_OUTPUT}"
echo "Stopwords: ${HDFS_STOPWORDS}"
echo "Reducers: ${NUM_REDUCERS}"
echo "========================================"

# Build the project
echo "Building project with Maven..."
cd "${ROOT_DIR}"
mvn clean package -DskipTests || {
	echo "Error: Maven build failed!" >&2
	exit 1
}

# Check JAR exists
if [ ! -f "${JAR_PATH}" ]; then
	echo "Error: JAR not found at ${JAR_PATH}" >&2
	exit 1
fi
echo "JAR found: ${JAR_PATH}"

# Verify HDFS input exists
echo "Verifying HDFS input directory..."
if ! hdfs dfs -test -d "${HDFS_INPUT}"; then
	echo "Error: HDFS input directory not found: ${HDFS_INPUT}" >&2
	echo "Run setup_hdfs.sh first to create directories and upload data." >&2
	exit 1
fi

# Verify stopwords file exists
echo "Verifying stopwords file..."
if ! hdfs dfs -test -f "${HDFS_STOPWORDS}"; then
	echo "Error: Stopwords file not found: ${HDFS_STOPWORDS}" >&2
	exit 1
fi

# Delete old output if exists
echo "Cleaning old output directory (if exists)..."
hdfs dfs -rm -r "${HDFS_OUTPUT}" 2>/dev/null || true

# Submit MapReduce job
echo "Submitting MapReduce job..."
hadoop jar "${JAR_PATH}" digital.librarian.ReverseIndexDriver \
	"${HDFS_INPUT}" \
	"${HDFS_OUTPUT}" \
	"${NUM_REDUCERS}"

JOB_STATUS=$?

if [ ${JOB_STATUS} -eq 0 ]; then
	echo "========================================"
	echo "Job completed successfully!"
	echo "========================================"
	echo "Output location: ${HDFS_OUTPUT}"
	echo ""
	echo "View results with:"
	echo "  hdfs dfs -ls ${HDFS_OUTPUT}"
	echo "  hdfs dfs -cat ${HDFS_OUTPUT}/part-r-00000 | head -20"
	exit 0
else
	echo "========================================"
	echo "Job failed with status: ${JOB_STATUS}"
	echo "========================================"
	exit ${JOB_STATUS}
fi
