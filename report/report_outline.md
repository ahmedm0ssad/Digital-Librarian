1. Title Page
   - Project Title: The Digital Librarian — Distributed Reverse Indexing
   - Team: [Your Name] and Habiba
   - Course: [Course Name / Number] (placeholder)
   - Date

2. Introduction / Problem Definition
   - Background and motivation for reverse indexing in large-scale text corpora
   - Problem statement: build a distributed reverse index using HDFS and MapReduce
   - Goals and success criteria

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
   - Limitations and future work
   - Final remarks on practicality of the approach
