# File Optimizer
> 60-72% token reduction | Sub-second latency | TXT, PDF, MD, Python support
> Semantic context compression for AI agents and LLM applications.

File Optimizer is a lightweight, task-aware context optimization engine that reduces token consumption while preserving the information that actually matters.

Instead of blindly truncating files or relying on keyword matching, File Optimizer performs semantic chunking, relevance ranking, token budgeting, and intelligent context construction to deliver compact and meaningful context to language models.

Built for modern AI systems, File Optimizer helps agents spend fewer tokens, lower costs, and maintain high-quality responses.

---

## Why File Optimizer?

Large Language Models are powerful, but context windows are expensive.

Most applications send entire files, documentation, notes, or codebases to an LLM—even when only a small fraction is relevant.

File Optimizer solves this problem.

### Traditional Approach

```
Files
 ↓
Entire Context
 ↓
LLM
 ↓
High Cost
```

### File Optimizer Approach

```
Files
 ↓
File Optimizer
 ↓
Relevant Context
 ↓
LLM
 ↓
Lower Cost + Better Focus
```

---

# Features

### Semantic Context Compression

Reduce unnecessary context while preserving task-relevant information.

### Multi-Format Support

Supports:

* TXT files
* PDF documents
* Markdown files
* Python source files

Additional formats are planned for future versions.

---

### Task-Aware Retrieval

Optimize context according to the agent's objective:

* Authentication logic
* Database transactions
* Machine learning concepts
* API documentation
* Research tasks
* Technical notes

---

### Token Budget Management

Control how much context is sent to the LLM.

Prevent unnecessary token usage and reduce inference costs.

---

### Chunk Deduplication

Removes repeated information and overlapping chunks.

---

### Docker Support

Deploy anywhere with reproducible environments.

---

### Modular Architecture

Each component is independent and can be extended separately.

* Ingestion
* Chunking
* Embeddings
* Ranking
* Budget Selection
* Deduplication
* Context Building

---

### Lightweight

No vector databases.

No heavy infrastructure.

No complex setup.

Simple API.

---

# Architecture

```
Input Files
      │
      ▼
File Ingestion
      │
      ▼
Chunking Engine
      │
      ▼
Embeddings
      │
      ▼
Semantic Ranking
      │
      ▼
Token Budget Selection
      │
      ▼
Deduplication
      │
      ▼
Optimized Context
```

---

# Supported File Formats

| Format   | Status |
| -------- | ------ |
| TXT      | ✅      |
| PDF      | ✅      |
| Markdown | ✅      |
| Python   | ✅      |

---

# Benchmarks

## Domain Benchmarks

| Query                 | Token Reduction |
| --------------------- | --------------- |
| JWT Authentication    | 72.44%          |
| Neural Networks       | 65.22%          |
| Database Transactions | 63.10%          |
| REST APIs             | 61.24%          |

### Average Token Reduction

**65.5%**

### Average Latency

**470 ms**

### Typical Output Size

60–70 tokens

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
cd token-engine
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Docker

Build:

```bash
docker build -t file-optimizer .
```

Run:

```bash
docker run --rm --name file-opt -p 8000:8000 file-optimizer
```

---

# API

Endpoint:

```
POST /file_opt
```

---

## Example Request

```json
{
  "agent_task": "jwt authentication and password hashing",
  "target_compression_ratio": 0.3,
  "max_context_tokens": 100,
  "files": [
    {
      "file_path": "benchmark/auth.txt",
      "type": "txt"
    }
  ]
}
```

---

## Example Response

```json
{
  "metrics": {
    "tokens_before": 225,
    "tokens_after": 62,
    "token_reduction_percent": 72.44
  },
  "optimized_context": "..."
}
```

---

# Project Structure

```
app/
├── api/
├── chunking/
├── compression/
├── embeddings/
├── ingestion/
├── ranking/
├── utils/

benchmark/
tests/
Dockerfile
main.py
requirements.txt
```

---

# Design Principles

## Relevance Over Aggressive Compression

Compression should never destroy meaning.

If the entire file is relevant, the engine preserves it.

---

## Simplicity First

No unnecessary infrastructure.

No mandatory databases.

No vendor lock-in.

---

## Modular by Design

Every component can evolve independently.

Future improvements do not require rewriting the entire system.

---

## Agent-Oriented

Built for AI workflows rather than traditional search systems.

---

# Use Cases

### AI Agents

Reduce context before invoking LLMs.

### RAG Pipelines

Compress retrieved documents.

### Documentation Systems

Send only relevant sections.

### Research Assistants

Focus on task-specific information.

### Developer Tools

Optimize source files and notes.

### Multi-File Context Management

Combine information from multiple files while respecting token budgets.

---

# Why File Optimizer?

Unlike traditional retrieval systems that focus on storage, File Optimizer focuses on consumption.

Its goal is not to store more information.

Its goal is to send less information while preserving meaning.

This makes File Optimizer an ideal companion for:

* OpenAI
* Anthropic
* Gemini
* Local LLMs
* Agent frameworks
* RAG pipelines

---

# Roadmap

---

## Version 1.0

Core Engine

* Multi-format support
* Semantic ranking
* Token budgeting
* Deduplication
* Docker support
* Benchmark suite

---

## Version 1.1

Quality Improvements

* Better overlap handling
* Similarity threshold selection
* Embedding caching
* Improved Markdown chunking

---

## Version 2.0

Agent Ecosystem

* LangChain integration
* CrewAI integration
* OpenAI Agents SDK support
* Batch optimization

---

## Version 3.0

Advanced Context Management

* Hybrid retrieval
* Vector database support
* Memory layers
* Incremental context updates

---

## Version 4.0

Distributed Context Infrastructure

* MCP server
* Streaming support
* Context orchestration
* Multi-agent optimization

---

# Contributing

Contributions are welcome.

Whether you're improving chunking, adding new file formats, optimizing ranking algorithms, or enhancing integrations, every contribution helps push the project forward.

Please open an issue or submit a pull request.

---

# Philosophy

Context windows are valuable.

Not everything deserves to be sent to the model.

The future of AI systems is not bigger prompts.

The future is smarter context.

---

# License

MIT License.

---

## Built for AI agents, researchers, and developers who want smarter context—not bigger prompts.
