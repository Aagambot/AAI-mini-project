"""
agents.py – Defines all four CrewAI agents for the Support Triage Crew.

Agents:
  1. Classifier       – category + priority + confidence
  2. KnowledgeRetriever – RAG over the Chroma KB
  3. ResponseDrafter  – writes the customer reply
  4. QAReviewer       – checks tone, accuracy, policy compliance
"""

from crewai import Agent, LLM

from config import PRIMARY_MODEL, CHEAP_MODEL, GOOGLE_API_KEY


def _llm(model: str) -> LLM:
    # CrewAI uses LiteLLM internally; ensure the 'gemini/' prefix is present
    model_name = model if model.startswith("gemini/") else f"gemini/{model}"
    return LLM(
        model=model_name,
        temperature=0.2,
        api_key=GOOGLE_API_KEY,
    )


# ─── 1. Classifier ──────────────────────────────────────────────────────────

def build_classifier(use_cheap_model: bool = False) -> Agent:
    model = CHEAP_MODEL if use_cheap_model else PRIMARY_MODEL
    return Agent(
        role="Support Ticket Classifier",
        goal=(
            "Accurately classify the incoming support ticket into one of the four categories "
            "(billing, technical, account, general) and assign a priority (low, medium, high). "
            "Also produce a confidence score between 0.0 and 1.0."
        ),
        backstory=(
            "You are a seasoned support operations expert who has read thousands of customer tickets. "
            "You quickly identify the root concern and route tickets to the right team. "
            "Your output is always a clean JSON object so downstream agents can act on it reliably."
        ),
        llm=_llm(model),
        verbose=True,
        allow_delegation=False,
    )


# ─── 2. Knowledge Retriever ─────────────────────────────────────────────────

def build_retriever(use_cheap_model: bool = False) -> Agent:
    model = CHEAP_MODEL if use_cheap_model else PRIMARY_MODEL
    return Agent(
        role="Knowledge Base Retriever",
        goal=(
            "Find the most relevant FAQ and policy chunks from the knowledge base "
            "that will help answer the customer's ticket. "
            "Return a structured list of sources with their content."
        ),
        backstory=(
            "You are a research specialist embedded in the support team. "
            "You know the product inside out and can instantly locate the right policy or FAQ entry. "
            "You never fabricate information — everything you surface comes directly from the knowledge base."
        ),
        llm=_llm(model),
        verbose=True,
        allow_delegation=False,
    )


# ─── 3. Response Drafter ────────────────────────────────────────────────────

def build_drafter(use_cheap_model: bool = False) -> Agent:
    model = CHEAP_MODEL if use_cheap_model else PRIMARY_MODEL
    return Agent(
        role="Customer Response Drafter",
        goal=(
            "Write a clear, empathetic, and actionable reply to the customer's support ticket "
            "using ONLY the information provided by the Knowledge Retriever. "
            "The reply should be concise (3-6 sentences), professional, and friendly."
        ),
        backstory=(
            "You are an expert customer success writer. "
            "You turn retrieved KB content into warm, helpful replies that resolve tickets on the first touch. "
            "You never introduce facts that were not in the retrieved sources, "
            "and you always include specific next steps the customer can take."
        ),
        llm=_llm(model),
        verbose=True,
        allow_delegation=False,
    )


# ─── 4. QA Reviewer ─────────────────────────────────────────────────────────

def build_qa_reviewer(use_cheap_model: bool = False) -> Agent:
    model = CHEAP_MODEL if use_cheap_model else PRIMARY_MODEL
    return Agent(
        role="QA Reviewer",
        goal=(
            "Review the drafted reply for tone, factual accuracy against the retrieved sources, "
            "policy compliance, and overall helpfulness. "
            "Output a structured verdict: APPROVED or NEEDS_REVISION, with a brief justification "
            "and (if revising) specific instructions for the drafter."
        ),
        backstory=(
            "You are a quality assurance lead who has set the gold standard for customer communication "
            "across the organization. You catch hallucinations, off-brand tone, and policy violations "
            "before replies reach customers. You are fair but exacting."
        ),
        llm=_llm(model),
        verbose=True,
        allow_delegation=False,
    )
