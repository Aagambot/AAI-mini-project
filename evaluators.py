"""
evaluators.py – LangSmith evaluators for the three key metrics:

1. classification_accuracy  – exact-match on category
2. reply_quality            – LLM-as-judge (0-1 score)
3. groundedness             – is the reply supported by retrieved sources?
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict

from langsmith.evaluation import EvaluationResult
from langchain_google_genai import ChatGoogleGenerativeAI

import config


# ---------------------------------------------------------------------------
# LLM judge helper (uses Gemini Pro for consistent judging)
# ---------------------------------------------------------------------------

def _judge_llm() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=config.PRIMARY_MODEL,
        temperature=0.0,
        google_api_key=config.GOOGLE_API_KEY,
    )


def _extract_score(text: str) -> float:
    """Pull the first float found in a string."""
    match = re.search(r"\b([0-9](?:\.[0-9]+)?|1\.0)\b", text)
    return float(match.group(1)) if match else 0.5


# ---------------------------------------------------------------------------
# 1. Classification Accuracy (exact match)
# ---------------------------------------------------------------------------

def classification_accuracy(run: Dict, example: Dict) -> EvaluationResult:
    """
    Compares predicted category against the expected label.
    Score: 1.0 if exact match, 0.0 otherwise.
    """
    predicted = (run.get("outputs", {}).get("category") or "").lower().strip()
    expected = (example.get("outputs", {}).get("expected_category") or "").lower().strip()

    score = 1.0 if predicted == expected else 0.0
    return EvaluationResult(
        key="classification_accuracy",
        score=score,
        comment=f"predicted='{predicted}' | expected='{expected}'",
    )


# ---------------------------------------------------------------------------
# 2. Reply Quality (LLM-as-judge)
# ---------------------------------------------------------------------------

_QUALITY_PROMPT = """\
You are a quality evaluator for customer support replies.

Customer ticket:
{ticket}

Support reply:
{reply}

Rate the reply on the following criteria (each 0-1):
- Relevance: Does the reply directly address the customer's issue?
- Clarity: Is the reply easy to understand?
- Tone: Is the reply professional and empathetic?
- Actionability: Does the reply provide clear next steps?

Respond with ONLY a JSON object (no markdown, no explanation):
{{"relevance": <0-1>, "clarity": <0-1>, "tone": <0-1>, "actionability": <0-1>, "overall": <0-1>}}
"""


def reply_quality(run: Dict, example: Dict) -> EvaluationResult:
    """
    LLM-as-judge scoring of the final reply.
    Returns the 'overall' score from the judge.
    """
    ticket = example.get("inputs", {}).get("ticket_text", "")
    reply = run.get("outputs", {}).get("final_reply", "")

    if not reply:
        return EvaluationResult(key="reply_quality", score=0.0, comment="Empty reply")

    llm = _judge_llm()
    prompt = _QUALITY_PROMPT.format(ticket=ticket, reply=reply)

    try:
        response = llm.invoke(prompt)
        text = response.content if hasattr(response, "content") else str(response)
        # Strip markdown fences
        text = re.sub(r"```(?:json)?", "", text).strip().rstrip("```").strip()
        data = json.loads(text)
        score = float(data.get("overall", 0.5))
    except Exception as e:
        score = 0.5
        text = f"Parse error: {e}"

    return EvaluationResult(
        key="reply_quality",
        score=score,
        comment=f"judge_response={text[:200]}",
    )


# ---------------------------------------------------------------------------
# 3. Groundedness (reply supported by retrieved sources)
# ---------------------------------------------------------------------------

_GROUNDEDNESS_PROMPT = """\
You are a factual groundedness evaluator.

The following is a summary of retrieved knowledge base sources:
---
{sources_summary}
---

The following is the final customer support reply:
---
{reply}
---

Task: Determine whether every factual claim in the reply is explicitly supported by the retrieved sources above.
Ignore tone, style, and phrasing. Only evaluate factual accuracy.

Respond with ONLY a JSON object (no markdown, no explanation):
{{"groundedness": <float 0.0 to 1.0>, "unsupported_claims": ["<claim 1>", "<claim 2>"]}}

A score of 1.0 means every claim is grounded. 0.0 means the reply is entirely unsupported.
"""


def groundedness(run: Dict, example: Dict) -> EvaluationResult:
    """
    Checks whether the final reply's claims are supported by the retrieved sources.
    """
    sources_summary = run.get("outputs", {}).get("retrieval_summary", "")
    reply = run.get("outputs", {}).get("final_reply", "")

    if not reply or not sources_summary:
        return EvaluationResult(
            key="groundedness",
            score=0.0,
            comment="Missing reply or sources",
        )

    llm = _judge_llm()
    prompt = _GROUNDEDNESS_PROMPT.format(sources_summary=sources_summary, reply=reply)

    try:
        response = llm.invoke(prompt)
        text = response.content if hasattr(response, "content") else str(response)
        text = re.sub(r"```(?:json)?", "", text).strip().rstrip("```").strip()
        data = json.loads(text)
        score = float(data.get("groundedness", 0.5))
        unsupported = data.get("unsupported_claims", [])
    except Exception as e:
        score = 0.5
        unsupported = []
        text = f"Parse error: {e}"

    return EvaluationResult(
        key="groundedness",
        score=score,
        comment=f"unsupported_claims={unsupported[:3]}",
    )
