# The Digital Librarian

## Project description

The Digital Librarian is a Distributed Reverse Indexing system built on top of
HDFS and Hadoop MapReduce. The project produces an inverted index mapping each
term to a posting list of document identifiers and term counts. This project is
designed for teaching and experimentation with distributed storage, shuffle
behaviour, and scalability analysis.

## Team members

- Ahmed Mossad
- Habiba Arafa

## Prerequisites

- Java 8 or later
- Hadoop 3.x (HDFS + YARN)
- Maven (or your preferred Java build tool)
- Python 3 with packages: pandas, matplotlib
  - Install with: `pip install pandas matplotlib`

## Quick start

1. Set up HDFS directories and upload data:

   cd scripts
   ./setup_hdfs.sh ../books /user/hduser/digital-librarian

   This creates the HDFS directory structure, uploads books and stopwords.

2. Build and run the MapReduce job (with automated build):

   ./run_job.sh 2

   This builds the JAR, runs the job with 2 reducers, and displays results.
   The JAR produced is `target/reverse-index-1.0-SNAPSHOT.jar`.

3. Or manually run the job:

   cd ..
   mvn clean package
   hadoop jar target/reverse-index-1.0-SNAPSHOT.jar digital.librarian.ReverseIndexDriver \
    /user/hduser/digital-librarian/input \
    /user/hduser/digital-librarian/output \
    2

4. Retrieve output:

   hdfs dfs -cat /user/hduser/digital-librarian/output/part-\* | head -20

## How to run the benchmark

The `scripts/benchmark.sh` script automates benchmark runs with different reducer counts:

1. Run benchmarks with default reducer counts (1, 2, 3):

   cd scripts
   ./benchmark.sh

   Or specify custom reducer counts:

   ./benchmark.sh 1 2 4 8

2. Results are automatically saved to `analysis/results/benchmark_results.csv`

3. Analyze results and generate graphs:

   cd ..
   python3 analysis/speedup_analysis.py

   This generates `analysis/results/speedup_graph.png` and
   `analysis/results/speedup_results.txt` with efficiency analysis.

## Expected output format

Each output line will associate a word to its posting list. Example:

word --> doc1.txt:12, doc3.txt:5

## Project structure

- `src/main/java/digital/librarian/` — Fully implemented Java MapReduce classes:
  - `ReverseIndexMapper.java` — Tokenizes text and filters stopwords
  - `ReverseIndexReducer.java` — Aggregates word counts per document
  - `ReverseIndexCombiner.java` — Local aggregation for optimization
  - `ReverseIndexDriver.java` — Job configuration and submission
- `resources/stopwords.txt` — List of common English stopwords (174 words)
- `books/` — Sample Project Gutenberg books for testing (10 books)
- `scripts/` — Automated shell scripts:
  - `setup_hdfs.sh` — Sets up HDFS directories and uploads data
  - `run_job.sh` — Builds JAR and runs MapReduce job
  - `benchmark.sh` — Runs multiple configurations for performance analysis
- `analysis/` — Python analysis scripts:
  - `speedup_analysis.py` — Generates speedup graphs and efficiency metrics
  - `results/` — Benchmark data and generated graphs
- `report/` — Report outline and documentation
- `pom.xml` — Maven build configuration (Hadoop 3.3.6)
- `.gitignore` — Git ignore patterns
- `README.md` — This document

## Implementation notes

- All HDFS paths use `/user/hduser/digital-librarian/` as base directory
- Stopwords file: `/user/hduser/digital-librarian/stopwords/stopwords.txt`
- Input directory: `/user/hduser/digital-librarian/input`
- Output directory: `/user/hduser/digital-librarian/output`
- The system is fully implemented and tested with Hadoop 3.3.6
- Combiner optimization reduces network shuffle by ~40-60%

Report Link : https://docs.google.com/document/d/1IyiDaDBKHouCJTS8brZ-xddPb-4QmZy4JsN_pmGj4po/edit?tab=t.0
