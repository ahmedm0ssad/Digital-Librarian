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
	REDUCERS=(1 2 3)
else
	REDUCERS=("$@")
fi

echo "Benchmark reducer counts: ${REDUCERS[*]}"
echo "Results CSV: ${RESULT_CSV}"

if [ ! -f "${RUN_SCRIPT}" ]; then
	echo "Error: run script not found at ${RUN_SCRIPT}" >&2
	exit 1
fi

for n in "${REDUCERS[@]}"; do
	echo "----"
	echo "Running benchmark with ${n} reducer(s)"

	# Note: In a real multi-node cluster scenario, you would provision nodes here
	# For now, we vary the number of reducers to simulate parallelism
	# provision_cluster ${n} || { echo "Provision failed for ${n} nodes"; exit 1; }

	start_ts=$(date +%s)

	# Run the job with specified number of reducers
	# The run script accepts reducer count as first argument
	if bash "${RUN_SCRIPT}" "${n}"; then
		echo "Run completed for ${n} reducer(s)"
	else
		echo "Run failed for ${n} reducer(s)" >&2
		echo "Continuing with next configuration..."
	fi

	end_ts=$(date +%s)
	elapsed=$((end_ts - start_ts))

	# Ensure results directory exists and CSV has header
	mkdir -p "$(dirname "${RESULT_CSV}")"
	if [ ! -f "${RESULT_CSV}" ]; then
		echo "reducers,execution_time_seconds" > "${RESULT_CSV}"
	fi

	# Append result
	echo "${n},${elapsed}" >> "${RESULT_CSV}"

	echo "Recorded: reducers=${n}, time=${elapsed}s -> ${RESULT_CSV}"

	# Optional: deprovision cluster between runs if your environment requires it
	# deprovision_cluster ${n} || true
done

echo "Benchmarking complete. Summary:" 
tail -n +1 "${RESULT_CSV}"
echo "To analyze results, run: python3 ${ROOT_DIR}/analysis/speedup_analysis.py"

# End of benchmark script
