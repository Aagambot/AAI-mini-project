"""
tasks.py – Defines the four CrewAI tasks that map to the four agents.

Task chain:
  classify_ticket → retrieve_knowledge → draft_response → qa_review
"""

from crewai import Task

from agents import Agent


# ─── Task 1: Classify ───────────────────────────────────────────────────────

def build_classify_task(agent: Agent, ticket_text: str) -> Task:
    return Task(
        description=f"""
You are given the following customer support ticket:

---
{ticket_text}
---

Classify this ticket by responding with ONLY a valid JSON object in the following format (no markdown, no extra text):

{{
  "category": "<billing|technical|account|general>",
  "priority": "<low|medium|high>",
  "confidence": <float between 0.0 and 1.0>,
  "reasoning": "<one sentence explaining why you chose this category>"
}}

Rules:
- category must be exactly one of: billing, technical, account, general
- priority must be exactly one of: low, medium, high
- confidence must be a float (e.g. 0.85)
- Do NOT include any text outside the JSON object
""",
        expected_output=(
            'A valid JSON object with keys: category, priority, confidence, reasoning. '
            'Example: {"category": "billing", "priority": "high", "confidence": 0.92, "reasoning": "..."}'
        ),
        agent=agent,
    )


# ─── Task 2: Retrieve Knowledge ─────────────────────────────────────────────

def build_retrieve_task(agent: Agent, ticket_text: str, category: str) -> Task:
    return Task(
        description=f"""
A customer has submitted the following support ticket (category: {category}):

---
{ticket_text}
---

You have been provided with the top relevant knowledge base chunks below.
Summarize the most useful facts from these chunks to help a drafter write the reply.
Focus on actionable steps, policy details, and relevant product links.

Return your response as a JSON object:
{{
  "sources": [
    {{
      "id": "<doc_id>",
      "title": "<doc_title>",
      "key_points": ["<point 1>", "<point 2>"]
    }}
  ],
  "retrieval_summary": "<2-3 sentence summary of what was found>"
}}
""",
        expected_output=(
            "A JSON object with 'sources' (list of retrieved doc summaries) "
            "and 'retrieval_summary' (concise summary of findings)."
        ),
        agent=agent,
    )


# ─── Task 3: Draft Response ──────────────────────────────────────────────────

def build_draft_task(agent: Agent, ticket_text: str, retrieval_summary: str) -> Task:
    return Task(
        description=f"""
Write a professional, friendly, and actionable customer support reply.

Customer ticket:
---
{ticket_text}
---

Relevant knowledge base information:
---
{retrieval_summary}
---

Guidelines:
- Start with a brief acknowledgement of the customer's issue
- Provide clear, step-by-step instructions where applicable
- Keep the reply to 3-6 sentences (or bullet points where clearer)
- Do NOT invent information not present in the knowledge base summary
- End with an offer to help further

Return your response as a JSON object:
{{
  "draft_reply": "<the full customer reply text>"
}}
""",
        expected_output=(
            "A JSON object with a single key 'draft_reply' containing the customer reply text."
        ),
        agent=agent,
    )


# ─── Task 4: QA Review ──────────────────────────────────────────────────────

def build_qa_task(
    agent: Agent,
    ticket_text: str,
    draft_reply: str,
    retrieval_summary: str,
) -> Task:
    return Task(
        description=f"""
Review the following draft customer support reply for quality.

Original ticket:
---
{ticket_text}
---

Knowledge base summary (ground truth):
---
{retrieval_summary}
---

Draft reply:
---
{draft_reply}
---

Evaluate on:
1. Tone – professional, empathetic, not robotic
2. Accuracy – every factual claim is supported by the knowledge base summary
3. Completeness – addresses the customer's actual question
4. Policy compliance – does not promise anything outside stated policies

Return your verdict as a JSON object:
{{
  "verdict": "<APPROVED|NEEDS_REVISION>",
  "score": <float 0.0 to 1.0 overall quality>,
  "issues": ["<issue 1>", "<issue 2>"],
  "revision_instructions": "<specific instructions if NEEDS_REVISION, else empty string>",
  "final_reply": "<the approved reply (same as draft if APPROVED, or revised version if NEEDS_REVISION)>"
}}

If verdict is APPROVED, final_reply should be the draft reply unchanged.
If verdict is NEEDS_REVISION, produce a corrected final_reply directly in this response.
""",
        expected_output=(
            "A JSON object with: verdict, score, issues, revision_instructions, final_reply."
        ),
        agent=agent,
    )
