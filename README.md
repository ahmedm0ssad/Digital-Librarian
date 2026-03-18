The Digital Librarian
=====================

Project description
-------------------
The Digital Librarian is a Distributed Reverse Indexing system built on top of
HDFS and Hadoop MapReduce. The project produces an inverted index mapping each
term to a posting list of document identifiers and term counts. This project is
designed for teaching and experimentation with distributed storage, shuffle
behaviour, and scalability analysis.

Team members
------------
- Ahmed Mossad
- Habiba Arafa

Prerequisites
-------------
- Java 8 or later
- Hadoop 3.x (HDFS + YARN)
- Maven (or your preferred Java build tool)
- Python 3 with packages: pandas, matplotlib
  - Install with: `pip install pandas matplotlib`

Quick start
-----------
1. Compile and package the Java project (example using Maven):

   mvn clean package

   This should produce a jar such as `target/digital-librarian.jar`.

2. Upload input data to HDFS:

   hdfs dfs -mkdir -p /user/hduser/digital-librarian/input
   hdfs dfs -put local_docs/* /user/hduser/digital-librarian/input

3. Run the MapReduce job:

   hadoop jar target/digital-librarian.jar digital.librarian.ReverseIndexDriver \
     /user/hduser/digital-librarian/input /user/hduser/digital-librarian/output

4. Retrieve output:

   hdfs dfs -cat /user/hduser/digital-librarian/output/part-* > inverted_index.txt

How to run the benchmark
------------------------
- The `scripts/benchmark.sh` script (todo) is intended to automate runs across
  different cluster sizes (1, 2, 3+ nodes). The high-level process is:
  1. Configure or provision the cluster for N worker nodes.
  2. Run the job using `run_job.sh` and capture start/end timestamps.
  3. Append `nodes,execution_time_seconds` to `analysis/results/benchmark_results.csv`.
  4. Use `analysis/speedup_analysis.py` to compute speedup and generate plots.

Expected output format
----------------------
Each output line will associate a word to its posting list. Example:

  word --> doc1.txt:12, doc3.txt:5

Project structure
-----------------
- `src/` — Java source skeletons for mapper, reducer, combiner, and driver
- `resources/stopwords.txt` — list of common English stop-words used in preprocessing
- `scripts/` — helper shell scripts: HDFS setup, job run, benchmarking
- `analysis/` — analysis scripts and `results/benchmark_results.csv`
- `report/` — report outline for writing the final PDF
- `.gitignore` — files to ignore in git
- `README.md` — this document

Notes and next steps
--------------------
- All Java classes are skeletons with TODOs for the student implemention.
- Ensure you adapt paths and cluster config in the scripts to match your environment.
- After running experiments, populate `analysis/results/benchmark_results.csv` and
  generate the speedup graph via `analysis/speedup_analysis.py`.
