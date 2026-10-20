# 🎯 Customer Support Triage Crew

> **AI-powered multi-agent pipeline** that automatically classifies, answers, and quality-checks support tickets — with every step traced and evaluated via LangSmith.

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Quick Start](#quick-start)
4. [Project Structure](#project-structure)
5. [Agents & Flow](#agents--flow)
6. [LangSmith Integration](#langsmith-integration)
7. [Evaluation Results](#evaluation-results)
8. [Configuration](#configuration)

---

## Overview

This project builds a four-agent CrewAI pipeline for customer support automation:

| Capability | Description |
|---|---|
| **Classification** | Assigns category (billing / technical / account / general) + priority + confidence |
| **RAG Retrieval** | Pulls the most relevant FAQ/policy chunks from a Chroma vector store |
| **Reply Drafting** | Writes a grounded, empathetic reply using retrieved context only |
| **QA Review** | Checks tone, accuracy, and policy compliance before the reply is sent |
| **Escalation** | Tickets below the confidence threshold are flagged for human review |
| **Evaluation** | 3-metric LangSmith evaluation across 80 labeled tickets |

---

## Architecture

```
Customer Ticket
      │
      ▼
┌─────────────────┐
│   Classifier    │ ──→ category, priority, confidence
└─────────────────┘
      │
      │ confidence < 0.70 → ⚠️ ESCALATED to human
      │
      ▼
┌─────────────────┐
│    Retriever    │ ──→ Chroma vector search (top-4 chunks)
└─────────────────┘
      │
      ▼
┌─────────────────┐
│    Drafter      │ ──→ draft reply (grounded in KB)
└─────────────────┘
      │
      ▼
┌─────────────────┐
│   QA Reviewer   │ ──→ APPROVED or NEEDS_REVISION (inline fix)
└─────────────────┘
      │
      ▼
   Final Reply + sources + QA verdict
```

All runs are automatically traced in LangSmith.

---

## Quick Start

### 1. Clone / navigate to the project

```bash
cd "mini-project"
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
GOOGLE_API_KEY=AIzaSy...
LANGCHAIN_API_KEY=lsv2_...
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=customer-support-triage
```

### 5. Build the knowledge base (vector store)

```bash
python setup_kb.py
```

This embeds 38 FAQ/policy documents into a local Chroma DB (`./chroma_db/`).

### 6. (Optional) Create LangSmith dataset

```bash
python langsmith_setup.py --action create_dataset
```

### 7. Launch the Streamlit app

```bash
streamlit run app.py
```

### OR: Run the CLI demo

```bash
# Single ticket
python run_demo.py --ticket "I was charged twice this month"

# All demo tickets
python run_demo.py --all

# Use cheaper model
python run_demo.py --cheap
```

---

## Project Structure

```
mini-project/
├── app.py                   # Streamlit UI (4 tabs)
├── crew.py                  # Pipeline orchestrator (@traceable)
├── agents.py                # CrewAI agent definitions (4 agents)
├── tasks.py                 # CrewAI task definitions (4 tasks)
├── evaluators.py            # LangSmith evaluators (3 metrics)
├── langsmith_setup.py       # Dataset creation + experiment runner
├── vector_store.py          # Chroma DB builder and query wrapper
├── config.py                # Central configuration (all env vars)
├── setup_kb.py              # One-shot KB build script
├── run_demo.py              # CLI demo runner
├── requirements.txt
├── .env.example
└── data/
    ├── knowledge_base.py    # 38 FAQ/policy KB documents
    └── labeled_dataset.py   # 80 labeled evaluation tickets
```

---

## Agents & Flow

### Agent 1 — Classifier
- **Model:** configurable (primary or cheap)
- **Output:** `{category, priority, confidence, reasoning}` (strict JSON)
- **Escalation:** tickets with `confidence < CONFIDENCE_THRESHOLD` (default 0.70) are immediately escalated

### Agent 2 — Knowledge Retriever
- **Retrieval:** Chroma cosine similarity, top-4 chunks, optionally filtered by category
- **Embedding:** `text-embedding-3-small`
- **Output:** `{sources, retrieval_summary}`

### Agent 3 — Response Drafter
- **Input:** ticket + retrieval summary
- **Constraint:** may only use information from the retrieved sources
- **Output:** `{draft_reply}` (3-6 sentences, professional & empathetic)

### Agent 4 — QA Reviewer
- **Checks:** tone · factual accuracy · completeness · policy compliance
- **Output:** `{verdict, score, issues, revision_instructions, final_reply}`
- **Revision loop:** capped at 1 revision (reviewer produces the corrected reply inline)

---

## LangSmith Integration

### Tracing
Every `run_triage()` call is decorated with `@traceable` and automatically logged to LangSmith with:
- Per-agent latency
- Token counts / metadata (via Google Gemini)
- Input/output for each step
- Metadata (model, confidence threshold, top-k)

### Dataset
80 labeled tickets across 4 categories (20 each), each with:
- `ticket_text` (input)
- `expected_category`, `expected_priority`, `reference_reply` (outputs)

### Evaluators

| Evaluator | Type | Measures |
|---|---|---|
| `classification_accuracy` | Exact match | Predicted vs expected category |
| `reply_quality` | LLM-as-Judge | Relevance, clarity, tone, actionability |
| `groundedness` | LLM-as-Judge | All claims supported by retrieved sources |

### Running experiments

```bash
# Primary model (gemini-1.5-pro)
python langsmith_setup.py --action run_experiment --model primary

# Cheap model (gemini-1.5-flash)
python langsmith_setup.py --action run_experiment --model cheap

# Both (side-by-side comparison)
python langsmith_setup.py --action compare
```

---

## Evaluation Results

*Fill in your actual results after running experiments.*

| Metric | Target | Primary Model | Cheap Model |
|---|---|---|---|
| Classification Accuracy | ≥ 85% | — | — |
| Reply Quality (LLM Judge) | ≥ 0.80 | — | — |
| Groundedness | ≥ 0.80 | — | — |
| Avg Latency / Ticket | < 15 s | — | — |
| Escalation Rate | 10–20% | — | — |
| Approx. Cost / Ticket | Tracked | — | — |

> View detailed experiment comparisons in your [LangSmith project](https://smith.langchain.com).

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `GOOGLE_API_KEY` | — | Google Gemini API key |
| `LANGCHAIN_API_KEY` | — | LangSmith API key |
| `LANGCHAIN_PROJECT` | `customer-support-triage` | LangSmith project name |
| `LANGCHAIN_TRACING_V2` | `true` | Enable LangSmith tracing |
| `PRIMARY_MODEL` | `gemini-1.5-pro` | Main LLM |
| `CHEAP_MODEL` | `gemini-1.5-flash` | Comparison LLM |
| `CONFIDENCE_THRESHOLD` | `0.7` | Below this → escalate |
| `MAX_REVISION_LOOPS` | `1` | Max QA revision cycles |
| `CHROMA_PERSIST_DIR` | `./chroma_db` | Vector store location |

---

## Tech Stack

| Component | Technology |
|---|---|
| Agent orchestration | [CrewAI](https://github.com/crewAIInc/crewAI) |
| Tracing & evaluation | [LangSmith](https://smith.langchain.com) |
| LLM | Google Gemini 3.6 Flash |
| Vector store | [Chroma](https://www.trychroma.com/) |
| Embeddings | Google text-embedding-004 |
| UI | [Streamlit](https://streamlit.io) |
