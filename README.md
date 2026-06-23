# Token Engine 🧠

> A framework-agnostic context optimization engine that sits between your agent systems and language models — compressing, ranking, and delivering only what matters.

[![MIT License](https://img.shields.io/badge/license-MIT-green)](https://github.com/bhumi1235/Dev-tools-File-optimizer-V1/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue)](https://python.org)
[![CI](https://img.shields.io/github/actions/workflow/status/bhumi1235/Dev-tools-File-optimizer-V1/test.yml)](https://github.com/bhumi1235/Dev-tools-File-optimizer-V1/actions)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://github.com/bhumi1235/Dev-tools-File-optimizer-V1/blob/main/Dockerfile)

---

## What is Token Engine?

Most LLM pipelines blindly stuff entire documents, repositories, or conversation histories into the context window. Token Engine fixes that.

It intelligently ingests your files, chunks them, embeds them semantically, ranks them against your task, and delivers a compressed, deduplicated, task-relevant context to the LLM — all within your token budget.

**65.5% average token reduction. 470ms average latency.**

---

## Core Philosophy

```text
Clients
  ↓
Interfaces (API / Library / MCP / Frameworks)
  ↓
optimizer.py          ← single source of truth
  ↓
Providers
  ↓
LLM
```

The optimizer is the product. Everything else is an interface to it. No matter how many frameworks or protocols are added, they all converge to the same core engine.

---

## Architecture

Every request flows through the following pipeline:

```text
Files
  ↓
Ingestion
  ↓
Chunking
  ↓
Compression
  ↓
Embeddings
  ↓
Semantic Ranking
  ↓
Token Budget Selection
  ↓
Deduplication
  ↓
Context Construction
  ↓
Planner
  ↓
Provider
  ↓
LLM
```

The architecture is intentionally modular. New frameworks, protocols, and interfaces can be added without modifying the optimization engine itself.

---

## Features

### Intelligent File Ingestion

Supports multiple file types out of the box:

* **Text files** — processed via generic file reader
* **PDFs** — dedicated PDF reader with text extraction
* **Markdown** — structure-preserving ingestion
* **Python source code** — logical boundary-aware ingestion

### Smart Chunking System

Different content requires different chunking strategies:

* **Text Chunker** — for general prose
* **Markdown Chunker** — preserves heading hierarchy and document structure
* **Python Code Chunker** — splits at logical code boundaries, not arbitrary character limits

### Semantic Compression Pipeline

Every request flows through a full compression pipeline:

```text
Files → Ingestion → Chunking → Compression → Embeddings
  → Semantic Ranking → Token Budget Selection → Deduplication
    → Context Construction → Planner → Provider → LLM
```

### Embedding-Based Relevance Ranking

Uses sentence-transformer embeddings (MiniLM) to score every chunk against your task:

```text
Task Embedding ──┐
                 ├── Cosine Similarity → Relevance Scores → Ranked Chunks
Chunk Embeddings ┘
```

Lazy model initialization ensures no overhead on import — the model loads once on first use and is reused forever.

### Adaptive Task Planner

Instead of a fixed retrieval strategy, Token Engine generates a plan per request:

```json
{
  "strategy": "retrieval | summarization | code | multi_file",
  "use_embeddings": true,
  "preserve_order": false,
  "bias_code": false,
  "cross_file": true
}
```

| Strategy      | Best For                                             |
| ------------- | ---------------------------------------------------- |
| Retrieval     | Default semantic search across documents             |
| Summarization | Preserves chunk order and disables embedding ranking |
| Code          | Adds code-specific scoring biases                    |
| Multi-file    | Cross-file retrieval with diversity preservation     |

### Multi-file Context Optimization

Processes multiple files simultaneously with:

* Token budget distribution across files
* Cross-file semantic retrieval
* File diversity preservation for repository-level reasoning

### Token Budget Management

A chunk selector enforces your maximum token limit — controlling cost, latency, and context size precisely.

### Deduplication

Repeated information is removed before context construction.

Every response includes:

* `before_dedup`
* `after_dedup`

for full transparency.

### Provider Abstraction

Generation is abstracted behind:

```python
BaseProvider
```

Currently implemented:

* **GroqProvider** (OpenAI-compatible API)

New providers can be added by implementing `BaseProvider`.

---

## Interfaces

Token Engine is simultaneously available through four different interfaces.

### 1. Python Library

```python
from app.core.optimizer import optimize

result = optimize(
    task="Summarize the key decisions",
    files=[
        {
            "file_path": "meeting.pdf",
            "type": "pdf"
        }
    ],
    max_context_tokens=2000
)

print(result["response"])
print(result["metrics"])
```

---

### 2. FastAPI Service

```text
POST /optimize
GET  /health
GET  /version
```

Returns:

* response
* metrics
* optimized context
* debug information
* top chunks

---

### 3. MCP Server

Token Engine exposes `optimize()` as an MCP tool, making it natively compatible with:

* Claude Desktop
* Cursor
* Windsurf
* VS Code
* Future MCP clients

Run the server:

```bash
python -m app.mcp.server
```

The entire MCP layer (`app/mcp/server.py`, `app/mcp/tools.py`) was added without modifying:

* optimizer.py
* planner.py
* embeddings
* compression
* providers

demonstrating strong separation of concerns.

---

### 4. Framework Integrations

Token Engine works inside existing agent ecosystems.

```python
# LangChain
from app.langchain.file_opt_tool import FileOptimizerTool

# CrewAI
from app.agents.crewai_tool import FileOptimizerCrewTool

# OpenAI Agents SDK
from app.agents.openai_agents_tool import FileOptimizerAgentTool

# SmolAgents
from app.agents.smolagents_tool import FileOptimizerSmolTool
```

All wrappers delegate to `optimizer.py`. No duplication, no divergence.

---

## Benchmarks

| Metric                  | Value                                        |
| ----------------------- | -------------------------------------------- |
| Average token reduction | 65.5%                                        |
| Average latency         | 470ms                                        |
| Supported file types    | TXT, PDF, MD, Python                         |
| Framework integrations  | LangChain, CrewAI, OpenAI Agents, SmolAgents |
| Protocol support        | REST API, MCP                                |

---

## Installation

```bash
pip install .
```

Import the optimizer:

```python
from app.core.optimizer import optimize
```

Or run via Docker:

```bash
docker build -t token-engine:v1.6 .

docker run -p 8000:8000 token-engine:v1.6
```

---

## Configuration

All settings are environment-driven — no hardcoded constants.

```env
MAX_CHUNK_WORDS=35
OVERLAP_SENTENCES=1
SIMILARITY_THRESHOLD=0.9
MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
LOG_LEVEL=INFO
GROQ_API_KEY=your_key_here
```

---

## Metrics

Every request returns full observability.

| Metric                    | Description                 |
| ------------------------- | --------------------------- |
| `tokens_before`           | Original context size       |
| `tokens_after`            | Compressed context size     |
| `token_reduction_percent` | Compression effectiveness   |
| `chunks_selected`         | Number of selected chunks   |
| `execution_time_ms`       | End-to-end latency          |
| `before_dedup`            | Chunks before deduplication |
| `after_dedup`             | Chunks after deduplication  |

---

## Project Structure

```text
token-engine/
│
├── app/
│   ├── agents/
│   ├── api/
│   ├── chunking/
│   ├── compression/
│   ├── core/
│   ├── embeddings/
│   ├── ingestion/
│   ├── langchain/
│   ├── llm/
│   ├── mcp/
│   ├── planner/
│   ├── providers/
│   ├── ranking/
│   └── utils/
│
├── benchmark/
├── data/
├── tests/
├── Dockerfile
├── pyproject.toml
├── requirements.txt
└── main.py
```

---

## Architectural Evolution

| Version | Milestone                                                             |
| ------- | --------------------------------------------------------------------- |
| v1.0    | Core engine — ingestion, chunking, embeddings, ranking, deduplication |
| v1.1    | Groq integration — end-to-end response generation                     |
| v1.2    | Framework integrations                                                |
| v1.3    | FastAPI and benchmarks                                                |
| v1.4    | Architecture refactoring and provider abstraction                     |
| v1.5    | Task-aware planner, testing, CI/CD, stabilization                     |
| v1.6    | pyproject.toml packaging, lazy initialization, MCP server support     |

---

## What Token Engine Intentionally Excludes

Token Engine intentionally avoids:

* Databases
* Redis
* Kafka
* Celery
* Vector databases
* Authentication systems
* Frontends

because none of these solve problems Token Engine actually has.

**Minimal dependencies. Maximum focus.**

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT — see [LICENSE](LICENSE).
