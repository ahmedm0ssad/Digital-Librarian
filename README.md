# The Digital Librarian

[![Java](https://img.shields.io/badge/Java-1.8-ED8B00?style=flat&logo=java&logoColor=white)](https://www.java.com/)
[![Hadoop](https://img.shields.io/badge/Hadoop-3.3.6-66CCFF?style=flat&logo=apachehadoop&logoColor=white)](https://hadoop.apache.org/)
[![Maven](https://img.shields.io/badge/Maven-C71A36?style=flat&logo=apachemaven&logoColor=white)](https://maven.apache.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

A **distributed reverse-indexing system** built on **HDFS and Hadoop MapReduce**. The Digital Librarian ingests a corpus of Project Gutenberg books and produces an inverted index mapping every term to a posting list of document identifiers and per-document term counts — enabling fast full-text search over large document collections.

> Joint project by **Ahmed Mossad** and **Habiba Arafa** — Big Data course (DSAI 427).

---

## Features

- **Full MapReduce pipeline** — Mapper → Combiner → Reducer → Driver
- **Distributed Cache** — stopword list (174 words) distributed to all nodes
- **Text preprocessing** — tokenization, normalization, stopword filtering
- **Scalability experiments** — configurable reducer counts with automated benchmarking
- **Multi-node support** — Docker Compose setup for 2-node clusters
- **Performance analysis** — Python suite with speedup graphs and **Amdahl's Law** analysis

## Architecture

The system is organized as a standard MapReduce workflow:

```
Gutenberg books (HDFS)
        │
        ▼
  Mapper ──── tokenizes text, filters stopwords,
        │     emits (term, docID)
        ▼
 Combiner ─── local aggregation to reduce shuffle traffic
        │
        ▼
 Reducer ──── aggregates term frequencies per document
        │
        ▼
Inverted index:  word → doc1:12, doc3:5
```

The **Combiner** reduces network shuffle by **~40–60%**.

## Repository Structure

```
Digital-Librarian/
├── src/main/java/digital/librarian/   # Java MapReduce classes
│   ├── ReverseIndexMapper.java        #   tokenizes + filters stopwords
│   ├── ReverseIndexCombiner.java      #   local aggregation (optimization)
│   ├── ReverseIndexReducer.java       #   aggregates counts per document
│   └── ReverseIndexDriver.java        #   job configuration & submission
├── books/                             # 10 Project Gutenberg books (~6 MB)
├── resources/stopwords.txt            # 174-word English stopword list
├── scripts/                           # automation scripts
│   ├── setup_hdfs.sh                  #   HDFS setup + data upload
│   ├── run_job.sh                     #   build JAR + run job
│   └── benchmark.sh                   #   multi-config performance sweep
├── analysis/                          # Python performance analysis
│   ├── speedup_analysis.py            #   speedup graphs + Amdahl's Law
│   └── results/                       #   benchmark CSV, TXT, PNG outputs
├── report/                            # project report outline
├── docker-compose-2nodes.yml          # 2-node cluster orchestration
├── pom.xml                            # Maven build (Hadoop 3.3.6, Java 1.8)
└── README.md
```

## Getting Started

### Prerequisites

- **Java 8+**
- **Hadoop 3.x** (HDFS + YARN)
- **Maven** (or preferred Java build tool)
- **Python 3** with `pandas` and `matplotlib` (`pip install pandas matplotlib`)

### 1. Setup HDFS and upload data

```bash
cd scripts
./setup_hdfs.sh ../books /user/hduser/digital-librarian
```

### 2. Build and run the job (automated)

```bash
./run_job.sh 2        # runs the job with 2 reducers
```

### 3. Run manually

```bash
mvn clean package
hadoop jar target/reverse-index-1.0-SNAPSHOT.jar digital.librarian.ReverseIndexDriver \
  /user/hduser/digital-librarian/input \
  /user/hduser/digital-librarian/output \
  2
```

### 4. Inspect the output

```bash
hdfs dfs -cat /user/hduser/digital-librarian/output/part-* | head -20
```

## Benchmarking & Performance Analysis

Run the automated sweep across reducer configurations:

```bash
cd scripts
./benchmark.sh            # default: 1, 2, 3 reducers
./benchmark.sh 1 2 4 8    # or a custom set
```

Results are saved to `analysis/results/benchmark_results.csv`. Then generate the analysis:

```bash
python3 analysis/speedup_analysis.py
```

This produces speedup graphs and efficiency metrics in `analysis/results/`.

### Key Results

| Configuration | Time |
|---|---|
| 1 reducer | 39s |
| 2 reducers | 34s |
| 3 reducers | 30s |

Multi-node experiments (1–3 nodes) reveal **negative scaling on small corpora** — Hadoop job startup and HDFS overhead dominate computation, with speedup peaking at ~1.00× (single node). This is the classic small-data/Hadoop behavior predicted by **Amdahl's Law**.

## Output Format

Each line maps a term to its posting list:

```
word --> doc1.txt:12, doc3.txt:5
```

## Implementation Notes

- HDFS base directory: `/user/hduser/digital-librarian/`
- Stopwords: `/user/hduser/digital-librarian/stopwords/stopwords.txt`
- Input: `/user/hduser/digital-librarian/input` · Output: `/user/hduser/digital-librarian/output`
- Tested against **Hadoop 3.3.6**

## Report

Full project report: [Google Docs](https://docs.google.com/document/d/1IyiDaDBKHouCJTS8brZ-xddPb-4QmZy4JsN_pmGj4po/edit?tab=t.0)

## Authors

- **Ahmed Mossad** — Data Science & AI, Zewail City
- **Habiba Arafa** — Data Science & AI, Zewail City