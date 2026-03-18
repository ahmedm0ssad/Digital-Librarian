1. Title Page
   - Project Title: The Digital Librarian — Distributed Reverse Indexing
   - Team: Ahmed and Habiba

2. Introduction / Problem Definition
   - Background and motivation for reverse indexing in large-scale text corpora
     - Large text collections (books, articles, web archives) require efficient
       indexing to support search and retrieval. Single-node indexes are limited
       by disk I/O, memory, and CPU constraints; a distributed approach enables
       processing much larger corpora.
     - An inverted (reverse) index maps each token to a posting list of document
       identifiers and counts; it is fundamental to retrieval systems and search engines.
   - Problem statement: build a distributed reverse index using HDFS and MapReduce
     - Implement a MapReduce pipeline that ingests documents from HDFS,
       tokenizes and normalizes text, removes stop-words, and produces a final
       inverted index in the format `word --> doc1.txt:count, doc2.txt:count`.
     - Minimize network shuffle by applying preprocessing and using a combiner
       for local aggregation while preserving correctness.
   - Goals and success criteria
     - Correctness: accurate per-document term counts and well-formed posting lists.
     - Efficiency: preprocessing and combiners should reduce intermediate
       shuffle volume compared to a naive implementation.
     - Scalability: execution time should decrease as worker nodes increase; the
       project will capture timing results for 1/2/3+ node configurations.

3. Data Science Lifecycle Implementation
   - Data Acquisition & Storage
     - Source of documents (local/ingest pipeline)
     - HDFS storage layout, block size, replication settings
     - Discussion on data locality and its effects on performance
   - Storage Analysis
     - HDFS blocks and replication factor used in experiments
     - Expected impact on throughput and fault tolerance
   - Preparation Impact
     - Stop-word removal: rationale and expected reduction in intermediate data
     - Tokenization choices and normalization (lowercasing, punctuation removal)
     - Quantify the effect on shuffle size (expected/observed)
   - Processing Logic
     - Mapper responsibilities: tokenization, stop-word filtering, per-doc counts
     - Combiner responsibilities: local aggregation to reduce shuffle
     - Reducer responsibilities: merging postings into final list
     - Data flow diagram: Mapper -> Shuffle/Sort -> Combiner -> Reducer

4. Scalability Analysis & Results
   - Experimental Setup
     - Cluster configuration for each experiment (nodes, cores, memory, HDFS replication)
     - Input dataset size and composition
     - Job configuration parameters (map/reduce slots, memory settings)
   - Performance Table
     - Table columns: nodes | exec_time_seconds | speedup
     - Reference to CSV: analysis/results/benchmark_results.csv
   - Speedup Graph
     - Reference image: analysis/results/speedup_graph.png
     - Instructions for generating the graph from CSV using `analysis/speedup_analysis.py`
   - Discussion
     - Compare observed speedup vs ideal/linear speedup
     - Apply Amdahl's Law to explain deviations
     - Identify bottlenecks (IO, shuffle, skew, startup costs)
     - Recommendations to improve scalability (combiner tuning, partitioning)

5. Conclusion
  - Summary of findings
    - A Hadoop MapReduce approach, combined with preprocessing (normalization
      and stop-word removal) and the use of a combiner for local aggregation,
      provides a practical and reproducible method for producing an inverted
      index at cluster scale. These techniques reduce intermediate data size
      and network shuffle, improving end-to-end job efficiency.
  - Limitations and future work
    - Many small files can negatively impact NameNode metadata and task
      scheduling; consider packing small inputs or using `CombineFileInputFormat`.
    - Additional preprocessing (stemming, language-specific tokenization) and
      partitioning strategies can improve index quality and reduce reducer skew.
    - For interactive or low-latency workloads, explore migrating the index to
      a specialized search engine (e.g., Elasticsearch) or reimplementing the
      pipeline in Spark for in-memory speedups.
  - Final remarks on practicality of the approach
    - The skeletons, scripts, and analysis scaffolding included in this
      repository enable reproducible laboratory experiments. Careful tuning of
      HDFS parameters, YARN resources, and MapReduce settings is required to
      achieve optimal performance on larger clusters.
