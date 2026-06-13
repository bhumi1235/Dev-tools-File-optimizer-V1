# Benchmark Results

## Overview

File Optimizer was evaluated across multiple domains and file formats to measure semantic relevance, token reduction, and execution latency.

The engine aims to preserve task-relevant information rather than maximize compression at all costs.

---

## Domain Benchmarks

| File         | Query                                   | Tokens Before | Tokens After | Reduction (%) | Latency (ms) |
| ------------ | --------------------------------------- | ------------: | -----------: | ------------: | -----------: |
| auth.txt     | JWT authentication and password hashing |           225 |           62 |         72.44 |       722.68 |
| ml.txt       | Neural networks and gradient descent    |           184 |           64 |         65.22 |       454.12 |
| database.txt | Database transactions and indexes       |           168 |           62 |         63.10 |       359.32 |
| api.txt      | REST APIs and HTTP status codes         |           178 |           69 |         61.24 |       345.26 |

### Aggregate Metrics

* **Average token reduction:** 65.5%
* **Average execution latency:** 470.35 ms
* **Typical selected chunks:** 2
* **Typical output size:** 60–70 tokens

---

## File Format Validation

| Format   | Query                                   | Tokens Before | Tokens After | Reduction (%) | Latency (ms) | Status |
| -------- | --------------------------------------- | ------------: | -----------: | ------------: | -----------: | ------ |
| TXT      | JWT authentication and password hashing |           225 |           62 |         72.44 |       722.68 | ✅      |
| PDF      | JWT authentication                      |           206 |           82 |         60.19 |       576.68 | ✅      |
| Markdown | Password hashing                        |            48 |           33 |         31.25 |       382.75 | ✅      |
| Python   | Authentication logic                    |            45 |           45 |          0.00 |       395.89 | ✅      |

---

## Observations

### Semantic Compression

The engine consistently removed unrelated information while preserving content relevant to the requested task.

### Stable Latency

Execution time remained below one second across all benchmarks.

### Multi-Format Support

The system successfully processed:

* Plain text files
* PDF documents
* Markdown notes
* Python source code

### Relevance Over Aggressive Compression

Compression is not forced.

If an input file is already highly relevant to the task, the engine may preserve the entire file.

For example, the Python benchmark achieved 0% token reduction because every function in the file contributed to the requested authentication logic.

---

## Strengths

* Semantic chunk ranking
* Task-aware context reduction
* Multi-format support
* Modular architecture
* Dockerized deployment
* Sub-second response times

---

## Future Improvements

Potential enhancements for future versions include:

* Improved overlap handling between adjacent chunks
* More advanced Markdown chunking
* Similarity threshold-based selection
* Embedding caching
* Additional language support
* Hybrid keyword and semantic retrieval

---

## Conclusion

Across multiple domains and file types, File Optimizer consistently reduced context size while preserving task-relevant information.

The engine achieved an average token reduction of approximately **65%** with an average execution latency of **470 ms**, demonstrating that semantic compression can significantly reduce context size without sacrificing relevance.
