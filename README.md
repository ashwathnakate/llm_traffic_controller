# LLM Traffic Controller

An intelligent request routing system that dynamically selects the most suitable LLM model based on **query complexity, ambiguity, and reasoning depth**.

Instead of sending every request to a single large model, this system **analyzes the user query first** and routes it to:

- a **fast, lightweight model** for simple questions
- a **deep reasoning model** for complex queries
- or a **clarification path** when the input is ambiguous

This project demonstrates **LLM orchestration, routing logic, and inference efficiency**, not just prompt usage.

---

## Key Features

- **Dynamic LLM Routing**

  - Fast path for simple queries
  - Deep reasoning path for complex queries
  - Clarification path for ambiguous inputs

- **Rule-based Query Analysis**

  - Length estimation
  - Ambiguity detection
  - Reasoning depth detection
  - Complexity scoring

- **Single Provider, Multiple Models**

  - Uses Groq with different LLaMA models
  - No vendor lock-in logic baked into routing

- **Built-in Metrics**

  - Request counts per route
  - Latency tracking
  - Route distribution visibility

- **Clean, Modular Architecture**
  - Analyzer
  - Router
  - Executor
  - Metrics
  - API layer

---

## Architecture Overview

```

User Query
↓
Analyzer (query signals)
↓
Router (FAST / DEEP / CLARIFY)
↓
Executor (Groq LLM)
↓
Response + Metrics

```

---

## Project Structure

```

app/
├── analyzer.py # Extracts query signals (complexity, ambiguity, etc.)
├── routing.py # Routing logic and Route enum
├── metrics.py # Latency & request metrics
├── models/
│ └── llm_client.py # Llm executor (model selection + inference)
├── main.py # FastAPI entrypoint

```

---

## Supported Routes

| Route                    | Description                                |
| ------------------------ | ------------------------------------------ |
| `FAST_PATH`              | Simple, direct questions                   |
| `DEEP_REASONING`         | Analytical or multi-step reasoning queries |
| `CLARIFICATION_REQUIRED` | Ambiguous or underspecified queries        |

---

## Models Used (Groq)

| Purpose        | Model                     |
| -------------- | ------------------------- |
| Fast responses | `llama-3.1-8b-instant`    |
| Deep reasoning | `llama-3.1-70b-versatile` |

---

## Example Requests

### Simple Query

```bash
curl -X POST http://127.0.0.1:8000/query \
-H "Content-Type: application/json" \
-d '{"query": "Define a personal computer in short"}'
```

➡ Routed to **FAST_PATH**

---

### Complex Query

```bash
curl -X POST http://127.0.0.1:8000/query \
-H "Content-Type: application/json" \
-d '{"query": "Compare supervised and unsupervised learning with real-world examples"}'
```

➡ Routed to **DEEP_REASONING**

---

### Ambiguous Query

```bash
curl -X POST http://127.0.0.1:8000/query \
-H "Content-Type: application/json" \
-d '{"query": "Explain this"}'
```

➡ Routed to **CLARIFICATION_REQUIRED**

---

## Metrics Endpoint

```bash
GET /metrics
```

Returns:

- total requests per route
- average latency per route

---

## Setup & Run

### 1. Install dependencies

```bash
pip install fastapi uvicorn groq
```

### 2. Set environment variable

```bash
export GROQ_API_KEY=your_api_key_here
```

### 3. Start the server

```bash
uvicorn app.main:app --reload
```

---

## Why This Project Is Different

Most LLM projects:

- hardcode a single model
- ignore query complexity
- waste inference capacity

This project:

- **treats LLMs as infrastructure**
- introduces **traffic control logic**
- mirrors real-world AI platform design

This is the kind of system used internally at:

- AI platforms
- agent orchestration layers
- cost-aware inference services

---

## Possible Extensions

- Automatic fallback from fast → deep model
- Cost-aware routing
- Confidence scoring
- Multi-provider support (OpenAI / NVIDIA NIM)
- Learning-based router

---

## Author

Built to demonstrate **LLM systems thinking**, not just model usage.
[Author](https://github.com/ashwathnakate)
