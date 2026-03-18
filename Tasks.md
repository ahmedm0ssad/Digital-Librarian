# 📚 The Digital Librarian — Task Board
**Project:** Distributed Reverse Indexing | HDFS & MapReduce  
**Team:** Mossad & Habiba  
**Due:** Thursday, 19 March 2026 — 11:59 PM  

---

## 🟢 Mossad's Tasks (Infrastructure & Setup)

### Code
- [ ] **Task 1** — Download 10–20 books from Project Gutenberg into `/books/` ✅
- [ ] **Task 2** — Implement `src/ReverseIndexMapper.java`
  - Normalize text (lowercase, remove punctuation)
  - Load `stopwords.txt` from DistributedCache in `setup()`
  - Emit `(word, filename)` for each valid token
- [ ] **Task 3** — Fill `resources/stopwords.txt` with 150+ stop words (one per line)
- [ ] **Task 4** — Implement `scripts/setup_hdfs.sh`
  - Create HDFS dirs, upload books + stopwords, verify upload
- [ ] **Task 5** — Implement `scripts/benchmark.sh`
  - Run job on 1, 2, 3+ nodes, record times to `benchmark_results.csv`

### Report (do last)
- [ ] **Task 6** — Write: Introduction & Problem Definition
- [ ] **Task 7** — Write: Storage Analysis (HDFS blocks, replication, data locality)
- [ ] **Task 8** — Write: Conclusion

---

## 🟣 Habiba's Tasks (Core Logic & Analysis)

### Code
- [ ] **Task 1** — Implement `src/ReverseIndexReducer.java`
  - Parse values (handle raw filenames AND `filename:count` format)
  - Aggregate counts per document using `HashMap<String, Integer>`
  - Output: `word --> doc1.txt:5, doc2.txt:2` (sorted alphabetically)
- [ ] **Task 2** — Implement `src/ReverseIndexDriver.java`
  - Configure job (mapper, combiner, reducer, I/O types)
  - Accept CLI args: inputPath, outputPath, numReducers
  - Add `stopwords.txt` to DistributedCache
  - Delete output path if exists before running
- [ ] **Task 3** ⭐ BONUS — Implement `src/ReverseIndexCombiner.java`
  - Local aggregation before shuffle to reduce network I/O
  - Emit `(word, "filename:count")` per unique filename
  - Also analyze effect of changing number of reducers
- [ ] **Task 4** — Implement `analysis/speedup_analysis.py`
  - Read `benchmark_results.csv` with pandas
  - Compute Speedup `S = T1 / Tn` for each row
  - Plot actual vs ideal linear speedup with matplotlib
  - Save graph to `analysis/results/speedup_graph.png`

### Report (do last)
- [ ] **Task 5** — Write: Data Preparation Impact
  - Quantify stop-word filtering effect on shuffle size
- [ ] **Task 6** — Write: Processing Logic (Mapper → Shuffle → Combiner → Reducer)
- [ ] **Task 7** — Write: Scalability Analysis & Results
  - Speedup table, graph, Amdahl's Law discussion, bottleneck identification

---

## 🟡 Shared Tasks (do together)

### Code
- [ ] **Task 1** — Implement & test `scripts/run_job.sh`
  - Compile all Java files, package into jar, run MapReduce job end-to-end
- [ ] **Task 2** — Write `README.md`
  - Prerequisites, compile steps, execution instructions, expected output

### Report (do last)
- [ ] **Task 3** — Assemble full report PDF
- [ ] **Task 4** — Final ZIP packaging & submission

---

## 📦 Deliverables Checklist

- [ ] `src/ReverseIndexMapper.java`
- [ ] `src/ReverseIndexReducer.java`
- [ ] `src/ReverseIndexCombiner.java` ⭐ bonus
- [ ] `src/ReverseIndexDriver.java`
- [ ] `resources/stopwords.txt`
- [ ] `scripts/setup_hdfs.sh`
- [ ] `scripts/run_job.sh`
- [ ] `scripts/benchmark.sh`
- [ ] `analysis/speedup_analysis.py`
- [ ] `analysis/results/benchmark_results.csv`
- [ ] `analysis/results/speedup_graph.png`
- [ ] `README.md`
- [ ] `report/report.pdf`
- [ ] Final `submission.zip`

---

## 🏆 Marks Coverage

| Category | Marks | Owner |
|---|---|---|
| Problem Definition & Prep | 2 | Mossad (report) |
| Functional Correctness (Reverse Index) | 5 | Habiba (Reducer) |
| HDFS & Distributed Logic | 2 | Mossad (Mapper + HDFS) |
| Performance Testing (1/2/3+ nodes) | 3 | Mossad (benchmark) |
| Scalability Analysis & Speedup | 2 | Habiba (Python + report) |
| Professionalism (README, code quality) | 1 | Shared |
| **Combiner Bonus** | **+1** | **Habiba** |
| **Total** | **15 + 1** | |

---

> 💡 **Tip:** After finishing your code tasks, do a `git pull` before writing your report sections so you have the latest version of everything.