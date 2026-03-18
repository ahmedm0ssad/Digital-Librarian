#!/bin/bash

set -euo pipefail

# Benchmark driver
# Usage: benchmark.sh [nodes...]
# Example: ./benchmark.sh 1 2 3
# Default: 1 2 3

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="${SCRIPT_DIR}/.."
RESULT_CSV="${ROOT_DIR}/analysis/results/benchmark_results.csv"
RUN_SCRIPT="${SCRIPT_DIR}/run_job.sh"

if [ "$#" -eq 0 ]; then
	NODES=(1 2 3)
else
	NODES=("$@")
fi

echo "Benchmark nodes: ${NODES[*]}"
echo "Results CSV: ${RESULT_CSV}"

if [ ! -f "${RUN_SCRIPT}" ]; then
	echo "Error: run script not found at ${RUN_SCRIPT}" >&2
	exit 1
fi

for n in "${NODES[@]}"; do
	echo "----"
	echo "Running benchmark for ${n} node(s)"

	# Placeholder: provision or configure cluster with ${n} worker nodes.
	# e.g., call an orchestration tool or cloud API here. This is environment-specific.
	# provision_cluster ${n} || { echo "Provision failed for ${n} nodes"; exit 1; }

	start_ts=$(date +%s)

	# Run the job. We call the run script and allow it to accept an optional node count argument.
	# The run script is expected to build and submit the MapReduce job and return non-zero on failure.
	if bash "${RUN_SCRIPT}" "${n}"; then
		echo "Run completed for ${n} nodes"
	else
		echo "Run failed for ${n} nodes" >&2
	fi

	end_ts=$(date +%s)
	elapsed=$((end_ts - start_ts))

	# Ensure results directory exists and CSV has header
	mkdir -p "$(dirname "${RESULT_CSV}")"
	if [ ! -f "${RESULT_CSV}" ]; then
		echo "nodes,execution_time_seconds" > "${RESULT_CSV}"
	fi

	# Append result
	echo "${n},${elapsed}" >> "${RESULT_CSV}"

	echo "Recorded: ${n},${elapsed} -> ${RESULT_CSV}"

	# Optional: deprovision cluster between runs if your environment requires it
	# deprovision_cluster ${n} || true
done

echo "Benchmarking complete. Summary:" 
tail -n +1 "${RESULT_CSV}"
echo "To analyze results, run: python3 ${ROOT_DIR}/analysis/speedup_analysis.py"

# End of benchmark script
