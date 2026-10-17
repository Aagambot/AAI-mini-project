"""
crew.py – Orchestrates the four-agent pipeline with LangSmith tracing.

Flow:
  Classifier → Knowledge Retriever → Response Drafter → QA Reviewer
  ↳ If escalation needed: returns ESCALATED status immediately.
  ↳ QA produces final reply (with built-in one-revision loop).
"""

from __future__ import annotations

import json
import re
import time
from typing import Any, Dict, List

from crewai import Crew, Process
from langsmith import traceable

import config
from agents import build_classifier, build_drafter, build_qa_reviewer, build_retriever
from tasks import build_classify_task, build_draft_task, build_qa_task, build_retrieve_task
from vector_store import retrieve_relevant_chunks


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract_json(text: str) -> Dict[str, Any]:
    """Extract the first JSON object found in a string (handles markdown fences)."""
    # Strip markdown code fences
    text = re.sub(r"```(?:json)?", "", text).strip().rstrip("```").strip()
    # Find first {...} block
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    # Fallback: try whole string
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text}


def _format_retrieved_chunks(chunks: List[Dict]) -> str:
    """Convert raw Chroma results into a readable context string."""
    lines = []
    for c in chunks:
        lines.append(f"[{c['id']}] {c['title']}\n{c['content']}")
    return "\n\n---\n\n".join(lines)


# ---------------------------------------------------------------------------
# Main traceable pipeline
# ---------------------------------------------------------------------------

@traceable(name="support_triage_pipeline", project_name=config.LANGCHAIN_PROJECT)
def run_triage(ticket_text: str, use_cheap_model: bool = False) -> Dict[str, Any]:
    """
    Run the full triage pipeline for a single ticket.

    Returns a dict with:
      - ticket_text
      - category, priority, confidence
      - escalated (bool)
      - sources (list of retrieved doc IDs)
      - draft_reply
      - qa_verdict, qa_score, qa_issues
      - final_reply
      - latency_seconds
      - model_used
    """
    start = time.time()
    model_label = config.CHEAP_MODEL if use_cheap_model else config.PRIMARY_MODEL

    # ── Step 1: Classify ──────────────────────────────────────────────────
    classifier = build_classifier(use_cheap_model)
    classify_task = build_classify_task(classifier, ticket_text)
    classify_crew = Crew(
        agents=[classifier],
        tasks=[classify_task],
        process=Process.sequential,
        verbose=False,
    )
    classify_result = classify_crew.kickoff()
    classification = _extract_json(str(classify_result))

    category = classification.get("category", "general")
    priority = classification.get("priority", "medium")
    confidence = float(classification.get("confidence", 0.5))
    reasoning = classification.get("reasoning", "")

    # Validate
    if category not in config.VALID_CATEGORIES:
        category = "general"
    if priority not in config.VALID_PRIORITIES:
        priority = "medium"

    # ── Escalation check ─────────────────────────────────────────────────
    if confidence < config.CONFIDENCE_THRESHOLD:
        return {
            "ticket_text": ticket_text,
            "category": category,
            "priority": priority,
            "confidence": confidence,
            "escalated": True,
            "escalation_reason": f"Low confidence ({confidence:.2f} < {config.CONFIDENCE_THRESHOLD}). Routing to human.",
            "sources": [],
            "retrieval_summary": "",
            "draft_reply": "",
            "qa_verdict": "ESCALATED",
            "qa_score": None,
            "qa_issues": [],
            "final_reply": "This ticket has been escalated to a human agent for review.",
            "latency_seconds": round(time.time() - start, 2),
            "model_used": model_label,
        }

    # ── Step 2: Retrieve ──────────────────────────────────────────────────
    raw_chunks = retrieve_relevant_chunks(ticket_text, category_filter=category)
    source_ids = [c["id"] for c in raw_chunks]
    retrieval_context = _format_retrieved_chunks(raw_chunks)

    retriever = build_retriever(use_cheap_model)
    retrieve_task = build_retrieve_task(retriever, ticket_text, category)
    # Inject context into the task description
    retrieve_task.description = (
        retrieve_task.description
        + f"\n\nKnowledge base chunks:\n---\n{retrieval_context}\n---"
    )
    retrieve_crew = Crew(
        agents=[retriever],
        tasks=[retrieve_task],
        process=Process.sequential,
        verbose=False,
    )
    retrieve_result = retrieve_crew.kickoff()
    retrieval_data = _extract_json(str(retrieve_result))
    retrieval_summary = retrieval_data.get(
        "retrieval_summary", retrieval_context[:500]
    )

    # ── Step 3: Draft ─────────────────────────────────────────────────────
    drafter = build_drafter(use_cheap_model)
    draft_task = build_draft_task(drafter, ticket_text, retrieval_summary)
    draft_crew = Crew(
        agents=[drafter],
        tasks=[draft_task],
        process=Process.sequential,
        verbose=False,
    )
    draft_result = draft_crew.kickoff()
    draft_data = _extract_json(str(draft_result))
    draft_reply = draft_data.get("draft_reply", str(draft_result))

    # ── Step 4: QA Review (with built-in revision) ───────────────────────
    qa_reviewer = build_qa_reviewer(use_cheap_model)
    qa_task = build_qa_task(qa_reviewer, ticket_text, draft_reply, retrieval_summary)
    qa_crew = Crew(
        agents=[qa_reviewer],
        tasks=[qa_task],
        process=Process.sequential,
        verbose=False,
    )
    qa_result = qa_crew.kickoff()
    qa_data = _extract_json(str(qa_result))

    verdict = qa_data.get("verdict", "APPROVED")
    qa_score = float(qa_data.get("score", 0.8))
    qa_issues = qa_data.get("issues", [])
    final_reply = qa_data.get("final_reply", draft_reply)

    # If reviewer says NEEDS_REVISION: it produces the corrected reply inline
    # (capped at 1 loop as per PRD §5.5)

    return {
        "ticket_text": ticket_text,
        "category": category,
        "priority": priority,
        "confidence": confidence,
        "escalated": False,
        "escalation_reason": "",
        "sources": source_ids,
        "retrieval_summary": retrieval_summary,
        "draft_reply": draft_reply,
        "qa_verdict": verdict,
        "qa_score": qa_score,
        "qa_issues": qa_issues,
        "final_reply": final_reply,
        "latency_seconds": round(time.time() - start, 2),
        "model_used": model_label,
    }


# ---------------------------------------------------------------------------
# Batch runner (for evaluation)
# ---------------------------------------------------------------------------

def run_batch(tickets: List[str], use_cheap_model: bool = False) -> List[Dict]:
    """Run triage on a list of ticket texts and return all results."""
    results = []
    for i, ticket in enumerate(tickets):
        print(f"[Batch] Processing ticket {i+1}/{len(tickets)}...")
        try:
            result = run_triage(ticket, use_cheap_model=use_cheap_model)
        except Exception as e:
            result = {
                "ticket_text": ticket,
                "error": str(e),
                "category": "unknown",
                "priority": "medium",
                "confidence": 0.0,
                "escalated": True,
                "final_reply": "Error during processing.",
            }
        results.append(result)
    return results
