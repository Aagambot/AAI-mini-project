"""
app.py – Streamlit UI for the Customer Support Triage Crew.

Features:
  - Single ticket input (text box)
  - CSV batch upload
  - Live progress display
  - Results dashboard with metrics
  - LangSmith experiment launcher
"""

from __future__ import annotations

import io
import json
import time
from typing import Any, Dict, List

import pandas as pd
import streamlit as st

# ─── Page config (must be first Streamlit call) ────────────────────────────
st.set_page_config(
    page_title="Support Triage Crew",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Inject CSS ────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    color: #e2e8f0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04);
    border-right: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
}
[data-testid="stSidebar"] .stMarkdown { color: #94a3b8; }

/* ── Main header ── */
.hero-header {
    background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(139,92,246,0.15) 100%);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(10px);
}
.hero-header h1 {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.4rem 0;
}
.hero-header p { color: #94a3b8; font-size: 1rem; margin: 0; }

/* ── Cards ── */
.result-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(8px);
    transition: border-color 0.2s;
}
.result-card:hover { border-color: rgba(99,102,241,0.4); }

/* ── Badges ── */
.badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    margin: 0 0.2rem;
}
.badge-billing    { background: rgba(251,191,36,0.15);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
.badge-technical  { background: rgba(59,130,246,0.15);  color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }
.badge-account    { background: rgba(16,185,129,0.15);  color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
.badge-general    { background: rgba(139,92,246,0.15);  color: #a78bfa; border: 1px solid rgba(139,92,246,0.3); }
.badge-high       { background: rgba(239,68,68,0.15);   color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
.badge-medium     { background: rgba(251,146,60,0.15);  color: #fb923c; border: 1px solid rgba(251,146,60,0.3); }
.badge-low        { background: rgba(74,222,128,0.15);  color: #4ade80; border: 1px solid rgba(74,222,128,0.3); }
.badge-approved   { background: rgba(16,185,129,0.15);  color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
.badge-revision   { background: rgba(251,191,36,0.15);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
.badge-escalated  { background: rgba(239,68,68,0.15);   color: #f87171; border: 1px solid rgba(239,68,68,0.3); }

/* ── Metric cards ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
}
.metric-box {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.2rem 1rem;
    text-align: center;
}
.metric-box .value {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-box .label { font-size: 0.78rem; color: #64748b; margin-top: 0.25rem; }

/* ── Reply box ── */
.reply-box {
    background: rgba(16,185,129,0.06);
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-size: 0.93rem;
    line-height: 1.7;
    color: #e2e8f0;
    white-space: pre-wrap;
}
.escalation-box {
    background: rgba(239,68,68,0.06);
    border: 1px solid rgba(239,68,68,0.25);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: #fca5a5;
}

/* ── Progress steps ── */
.step-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem 0;
    font-size: 0.9rem;
}
.step-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
}
.dot-done    { background: #34d399; }
.dot-running { background: #fbbf24; animation: pulse 1s infinite; }
.dot-pending { background: #374151; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.5rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* ── Input fields ── */
.stTextArea textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}

/* ── Tab styling ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border-radius: 10px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    color: #64748b !important;
    border-radius: 8px;
}
.stTabs [aria-selected="true"] {
    background: rgba(99,102,241,0.2) !important;
    color: #818cf8 !important;
}

/* ── Expander ── */
details { 
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 8px !important;
}

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.06) !important; }

/* ── Select/checkbox ── */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border-color: rgba(255,255,255,0.1) !important;
    color: #e2e8f0 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ─── Imports (after page config) ───────────────────────────────────────────
import config


def _check_config() -> bool:
    """Verify essential API keys are present."""
    return bool(config.GOOGLE_API_KEY and config.LANGCHAIN_API_KEY)


def _badge(text: str, css_class: str) -> str:
    return f'<span class="badge {css_class}">{text}</span>'


def _category_badge(cat: str) -> str:
    cls_map = {
        "billing": "badge-billing",
        "technical": "badge-technical",
        "account": "badge-account",
        "general": "badge-general",
    }
    return _badge(cat.upper(), cls_map.get(cat, "badge-general"))


def _priority_badge(pri: str) -> str:
    return _badge(pri.upper(), f"badge-{pri}")


def _verdict_badge(verdict: str) -> str:
    if verdict == "APPROVED":
        return _badge("✓ APPROVED", "badge-approved")
    elif verdict == "ESCALATED":
        return _badge("⚠ ESCALATED", "badge-escalated")
    else:
        return _badge("↺ REVISED", "badge-revision")


# ─── Sidebar ───────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### ⚙️ Settings")

    use_cheap = st.checkbox(
        f"Use cheaper model ({config.CHEAP_MODEL})",
        value=False,
        help="Faster and cheaper. Switch off for best quality.",
    )
    model_label = config.CHEAP_MODEL if use_cheap else config.PRIMARY_MODEL
    st.caption(f"Active model: `{model_label}`")

    st.markdown("---")
    st.markdown("### 📊 LangSmith")

    ls_ok = bool(config.LANGCHAIN_API_KEY)
    st.markdown(
        f"Status: {'🟢 Connected' if ls_ok else '🔴 Not configured'}",
    )
    st.caption(f"Project: `{config.LANGCHAIN_PROJECT}`")

    if st.button("🔗 Open LangSmith", use_container_width=True):
        st.markdown(
            f"[Open LangSmith ↗](https://smith.langchain.com/projects/{config.LANGCHAIN_PROJECT})",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown(
        """
**Customer Support Triage Crew**

Multi-agent pipeline using:
- 🤖 CrewAI orchestration
- 🗄️ Chroma vector DB (RAG)
- 📡 LangSmith tracing
- ✅ 3-metric evaluation

**Agents:** Classifier → Retriever → Drafter → QA Reviewer
        """,
    )

# ─── Header ────────────────────────────────────────────────────────────────

st.markdown(
    """
<div class="hero-header">
  <h1>🎯 Customer Support Triage Crew</h1>
  <p>AI-powered ticket classification, knowledge retrieval, reply drafting, and QA — all in one pipeline.</p>
</div>
""",
    unsafe_allow_html=True,
)

# ─── Config warning ────────────────────────────────────────────────────────

if not _check_config():
    st.error(
        "⚠️ **API keys not configured.** Copy `.env.example` to `.env` and fill in your "
        "`GOOGLE_API_KEY` and `LANGCHAIN_API_KEY`, then restart the app."
    )
    st.stop()

# ─── Tabs ──────────────────────────────────────────────────────────────────

tab_single, tab_batch, tab_experiments, tab_setup = st.tabs(
    ["🎫 Single Ticket", "📂 Batch CSV", "📈 Experiments", "🔧 Setup"]
)


# ═══════════════════════════════════════════════════════════════════════════
# TAB 1: SINGLE TICKET
# ═══════════════════════════════════════════════════════════════════════════

with tab_single:
    st.markdown("#### Enter a support ticket")

    # Quick examples
    col_ex1, col_ex2, col_ex3, col_ex4 = st.columns(4)
    examples = {
        "💳 Billing": "I was charged twice this month. Please refund the duplicate charge immediately.",
        "🔧 Technical": "I'm getting a 429 Too Many Requests error from your API. What should I do?",
        "👤 Account": "I forgot my password and can't log in. The reset email isn't arriving.",
        "❓ General": "Is your platform GDPR compliant? We're a healthcare company.",
    }
    for col, (label, text) in zip(
        [col_ex1, col_ex2, col_ex3, col_ex4], examples.items()
    ):
        with col:
            if st.button(label, use_container_width=True, key=f"ex_{label}"):
                st.session_state["ticket_input"] = text

    ticket_text = st.text_area(
        "Ticket text",
        value=st.session_state.get("ticket_input", ""),
        height=120,
        placeholder="Paste or type the customer support ticket here…",
        label_visibility="collapsed",
        key="ticket_input_area",
    )

    run_col, _ = st.columns([1, 3])
    with run_col:
        run_btn = st.button("🚀 Run Triage", use_container_width=True)

    if run_btn:
        if not ticket_text.strip():
            st.warning("Please enter a ticket first.")
        else:
            # ── Progress display ────────────────────────────────────────
            steps = ["Classify", "Retrieve Knowledge", "Draft Reply", "QA Review"]
            progress_placeholder = st.empty()

            def render_progress(done: int, current: int):
                rows = ""
                for i, step in enumerate(steps):
                    if i < done:
                        dot = '<div class="step-dot dot-done"></div>'
                        color = "#34d399"
                    elif i == current:
                        dot = '<div class="step-dot dot-running"></div>'
                        color = "#fbbf24"
                    else:
                        dot = '<div class="step-dot dot-pending"></div>'
                        color = "#475569"
                    rows += (
                        f'<div class="step-row">{dot}'
                        f'<span style="color:{color}">{step}</span></div>'
                    )
                progress_placeholder.markdown(
                    f'<div class="result-card">{rows}</div>', unsafe_allow_html=True
                )

            render_progress(done=0, current=0)

            with st.spinner("Running crew…"):
                from crew import run_triage

                # We'll call run_triage which internally runs all steps
                render_progress(done=0, current=0)
                time.sleep(0.3)
                result = run_triage(ticket_text, use_cheap_model=use_cheap)

            progress_placeholder.empty()

            # ── Results ─────────────────────────────────────────────────
            st.markdown("---")
            st.markdown("### Results")

            # Metadata row
            meta_html = (
                _category_badge(result["category"])
                + _priority_badge(result["priority"])
                + _verdict_badge(result["qa_verdict"])
                + f' &nbsp; <span style="color:#64748b;font-size:0.82rem">Confidence: {result["confidence"]:.0%} &nbsp;|&nbsp; '
                f'Latency: {result["latency_seconds"]}s &nbsp;|&nbsp; Model: {result["model_used"]}</span>'
            )
            st.markdown(meta_html, unsafe_allow_html=True)
            st.markdown("")

            if result["escalated"]:
                st.markdown(
                    f'<div class="escalation-box">⚠️ <strong>Escalated to human agent</strong><br>'
                    f'{result["escalation_reason"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                # Columns: reply + sources
                rc1, rc2 = st.columns([3, 2])

                with rc1:
                    st.markdown("**📝 Final Reply**")
                    st.markdown(
                        f'<div class="reply-box">{result["final_reply"]}</div>',
                        unsafe_allow_html=True,
                    )

                    if result["qa_verdict"] == "NEEDS_REVISION" and result.get("qa_issues"):
                        with st.expander("QA issues found (revised inline)", expanded=False):
                            for issue in result["qa_issues"]:
                                st.markdown(f"- {issue}")

                with rc2:
                    st.markdown("**📚 Sources Used**")
                    for src_id in result["sources"]:
                        st.markdown(
                            f"<div class='result-card' style='padding:0.6rem 1rem;margin-bottom:0.5rem'>"
                            f"<code style='color:#818cf8'>{src_id}</code></div>",
                            unsafe_allow_html=True,
                        )

                    st.markdown("**QA Score**")
                    qa_score = result.get("qa_score") or 0
                    st.progress(qa_score, text=f"{qa_score:.0%}")

                # Full JSON (debug)
                with st.expander("🔍 Full pipeline output (JSON)", expanded=False):
                    st.json(result)


# ═══════════════════════════════════════════════════════════════════════════
# TAB 2: BATCH CSV
# ═══════════════════════════════════════════════════════════════════════════

with tab_batch:
    st.markdown("#### Upload CSV for batch processing")
    st.markdown(
        "CSV must have a column named **`ticket_text`** (and optionally `ticket_id`). "
        "Results include predicted category, priority, confidence, and final reply."
    )

    # Sample download
    sample_data = pd.DataFrame(
        {
            "ticket_id": ["T001", "T002", "T003"],
            "ticket_text": [
                "I was charged twice this month.",
                "App won't load — just a blank white screen.",
                "How do I reset my password?",
            ],
        }
    )
    csv_bytes = sample_data.to_csv(index=False).encode()
    st.download_button(
        "⬇️ Download sample CSV",
        data=csv_bytes,
        file_name="sample_tickets.csv",
        mime="text/csv",
    )

    uploaded = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")

    if uploaded:
        df = pd.read_csv(uploaded)
        if "ticket_text" not in df.columns:
            st.error("CSV must contain a 'ticket_text' column.")
        else:
            st.info(f"Loaded **{len(df)}** tickets. Click 'Run Batch' to process.")
            st.dataframe(df.head(5), use_container_width=True)

            if st.button("🚀 Run Batch Triage", use_container_width=False):
                from crew import run_triage

                results_list = []
                progress_bar = st.progress(0, text="Processing tickets…")
                status_text = st.empty()

                for i, row in df.iterrows():
                    ticket = str(row["ticket_text"])
                    status_text.text(f"Ticket {i+1}/{len(df)}: {ticket[:60]}…")
                    try:
                        res = run_triage(ticket, use_cheap_model=use_cheap)
                    except Exception as e:
                        res = {
                            "ticket_text": ticket,
                            "category": "error",
                            "priority": "medium",
                            "confidence": 0.0,
                            "escalated": True,
                            "final_reply": f"Error: {e}",
                            "qa_verdict": "ERROR",
                            "qa_score": 0.0,
                            "sources": [],
                            "latency_seconds": 0,
                        }
                    tid = row.get("ticket_id", f"row_{i}")
                    results_list.append(
                        {
                            "ticket_id": tid,
                            "ticket_text": ticket[:80],
                            "category": res["category"],
                            "priority": res["priority"],
                            "confidence": f"{res['confidence']:.0%}",
                            "escalated": res["escalated"],
                            "qa_verdict": res["qa_verdict"],
                            "qa_score": f"{(res.get('qa_score') or 0):.0%}",
                            "latency_s": res["latency_seconds"],
                            "final_reply": res["final_reply"][:120] + "…",
                        }
                    )
                    progress_bar.progress((i + 1) / len(df))

                status_text.empty()
                progress_bar.empty()

                result_df = pd.DataFrame(results_list)
                st.success(f"✅ Processed {len(result_df)} tickets!")
                st.dataframe(result_df, use_container_width=True)

                # Summary metrics
                total = len(result_df)
                escalated = result_df["escalated"].sum()
                st.markdown("---")
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Total Tickets", total)
                m2.metric("Escalated", escalated, delta=f"{escalated/total:.0%}")
                m3.metric(
                    "Avg Latency",
                    f"{result_df['latency_s'].mean():.1f}s",
                )
                m4.metric(
                    "Auto-resolved",
                    total - escalated,
                )

                # Download results
                out_csv = result_df.to_csv(index=False).encode()
                st.download_button(
                    "⬇️ Download results CSV",
                    data=out_csv,
                    file_name="triage_results.csv",
                    mime="text/csv",
                )


# ═══════════════════════════════════════════════════════════════════════════
# TAB 3: EXPERIMENTS
# ═══════════════════════════════════════════════════════════════════════════

with tab_experiments:
    st.markdown("#### LangSmith Evaluation Experiments")
    st.markdown(
        "Run the full 80-ticket evaluation suite and compare model performance. "
        "Results are stored in your LangSmith project for comparison."
    )

    # Success metrics targets
    st.markdown("**📋 Target Metrics (per PRD)**")
    targets = {
        "Classification Accuracy": ("≥ 85%", "Routing is dependable"),
        "Groundedness Score": ("≥ 80%", "Replies rely on KB"),
        "Avg Latency / Ticket": ("< 15 s", "Usable in practice"),
        "Escalation Rate": ("10–20%", "Balanced automation"),
        "Cost per Ticket": ("Tracked", "Model trade-off"),
    }
    target_df = pd.DataFrame(
        [(k, v[0], v[1]) for k, v in targets.items()],
        columns=["Metric", "Target", "Reason"],
    )
    st.dataframe(target_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    exp_col1, exp_col2 = st.columns(2)

    with exp_col1:
        st.markdown("**Create / refresh dataset**")
        st.caption("Uploads 80 labeled tickets to LangSmith.")
        if st.button("📤 Create Dataset", use_container_width=True, key="create_ds"):
            with st.spinner("Creating LangSmith dataset…"):
                from langsmith import Client
                from langsmith_setup import create_dataset

                client = Client(api_key=config.LANGCHAIN_API_KEY)
                try:
                    did = create_dataset(client)
                    st.success(f"Dataset created! ID: `{did}`")
                except Exception as e:
                    st.error(f"Error: {e}")

    with exp_col2:
        st.markdown("**Run evaluation experiment**")
        exp_model = st.selectbox(
            "Model",
            [f"Primary ({config.PRIMARY_MODEL})", f"Cheap ({config.CHEAP_MODEL})", "Both (comparison)"],
            key="exp_model_select",
        )
        if st.button("▶️ Run Experiment", use_container_width=True, key="run_exp"):
            with st.spinner("Running evaluation (this may take several minutes)…"):
                from langsmith import Client
                from langsmith_setup import run_experiment

                client = Client(api_key=config.LANGCHAIN_API_KEY)
                try:
                    if "Both" in exp_model:
                        run_experiment(client, use_cheap_model=False)
                        run_experiment(client, use_cheap_model=True)
                    elif "Cheap" in exp_model:
                        run_experiment(client, use_cheap_model=True)
                    else:
                        run_experiment(client, use_cheap_model=False)
                    st.success(
                        f"✅ Experiment complete! "
                        f"[View in LangSmith ↗](https://smith.langchain.com/projects/{config.LANGCHAIN_PROJECT})"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")
    st.markdown("**Evaluators**")
    eval_info = [
        {
            "Evaluator": "Classification Accuracy",
            "Type": "Exact Match",
            "Measures": "Predicted vs expected category (billing/technical/account/general)",
        },
        {
            "Evaluator": "Reply Quality",
            "Type": "LLM-as-Judge",
            "Measures": "Relevance, clarity, tone, actionability (0–1 scale)",
        },
        {
            "Evaluator": "Groundedness",
            "Type": "LLM-as-Judge",
            "Measures": "All reply claims supported by retrieved KB sources",
        },
    ]
    st.dataframe(pd.DataFrame(eval_info), use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════════════
# TAB 4: SETUP
# ═══════════════════════════════════════════════════════════════════════════

with tab_setup:
    st.markdown("#### Project Setup")

    # Config status
    status_items = {
        "GOOGLE_API_KEY": bool(config.GOOGLE_API_KEY),
        "LANGCHAIN_API_KEY": bool(config.LANGCHAIN_API_KEY),
        "LANGCHAIN_TRACING_V2": config.LANGCHAIN_TRACING_V2 == "true",
        "LANGCHAIN_PROJECT": bool(config.LANGCHAIN_PROJECT),
        "CHROMA_PERSIST_DIR": True,  # always has default
    }
    for key, ok in status_items.items():
        icon = "✅" if ok else "❌"
        st.markdown(f"{icon} `{key}`")

    st.markdown("---")
    st.markdown("**Build Vector Store**")
    st.caption(
        "Embeds the knowledge base (38 FAQ documents) into a local Chroma vector store. "
        "Run this once before processing tickets."
    )
    if st.button("🗄️ Build Knowledge Base", use_container_width=False, key="build_kb"):
        with st.spinner("Embedding knowledge base (this takes ~30s on first run)…"):
            try:
                from data.knowledge_base import KB_DOCUMENTS
                from vector_store import build_vector_store

                build_vector_store(KB_DOCUMENTS)
                st.success(f"✅ Vector store built with {len(KB_DOCUMENTS)} documents!")
            except Exception as e:
                st.error(f"Error building vector store: {e}")

    st.markdown("---")
    st.markdown("**Quick-start commands**")
    st.code(
        """# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and fill in .env
cp .env.example .env
# Edit .env with your API keys

# 3. Build the vector store
python vector_store.py

# 4. (Optional) Create LangSmith dataset
python langsmith_setup.py --action create_dataset

# 5. Launch the app
streamlit run app.py
""",
        language="bash",
    )

    st.markdown("**Project structure**")
    st.code(
        """mini-project/
├── app.py                  # Streamlit UI
├── crew.py                 # Pipeline orchestrator
├── agents.py               # CrewAI agent definitions
├── tasks.py                # CrewAI task definitions
├── evaluators.py           # LangSmith evaluators
├── langsmith_setup.py      # Dataset + experiment runner
├── vector_store.py         # Chroma DB wrapper
├── config.py               # Central configuration
├── requirements.txt
├── .env.example
└── data/
    ├── knowledge_base.py   # 38 FAQ/policy documents
    └── labeled_dataset.py  # 80 labeled tickets
""",
        language="text",
    )
