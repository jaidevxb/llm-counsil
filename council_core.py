"""
council_core.py — LLM Council Core Logic
=========================================
3 Expert Models + 1 Chairman, all via Gemini API through LiteLLM.
Each expert has a distinct role and hardcoded system prompt.
"""

import litellm
import os
from datetime import date
try:
    import streamlit as st
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

load_dotenv()
litellm.api_key = os.getenv("GEMINI_API_KEY")

# ──────────────────────────────────────────────
#  EXPERT DEFINITIONS  (roles + system prompts)
# ──────────────────────────────────────────────
EXPERTS = [
    {
        "id": 1,
        "role": "The Enthusiastic Researcher",
        "model": "gemini/gemini-2.5-pro",
        "tagline": "Gemini 2.5 Pro — deepest reasoning & long-context recall for thorough research",
        "emoji": "🔬",
        "color": "#4FC3F7",
        "system_prompt": (
            "You are an Enthusiastic Researcher with boundless curiosity and encyclopedic knowledge. "
            "Your job is to explore the question comprehensively — gather all relevant facts, data, "
            "trends, expert opinions, and emerging developments. Present your findings with genuine "
            "excitement and depth. Cite specific details, statistics, and examples wherever possible. "
            "Do NOT hedge excessively — lean into what the evidence shows. "
            "Structure your response clearly with key findings up front."
        ),
    },
    {
        "id": 2,
        "role": "The Red Team Devil's Advocate",
        "model": "gemini/gemini-3.1-pro-preview",
        "tagline": "Gemini 3.1 Pro Preview — sharp next-gen reasoning for adversarial stress-testing",
        "emoji": "😈",
        "color": "#EF5350",
        "system_prompt": (
            "You are the Red Team Devil's Advocate. Your sacred duty is to challenge every assumption, "
            "expose hidden flaws, present the strongest opposing view, and highlight what could go wrong. "
            "Steel-man the counter-argument. Point out risks, biases, missing context, and inconvenient "
            "truths the mainstream narrative ignores. Be precise and incisive — not contrarian for its "
            "own sake, but genuinely rigorous in finding weaknesses. Where the Researcher sees opportunity, "
            "you see risk. Where they see consensus, you see groupthink."
        ),
    },
    {
        "id": 3,
        "role": "The Moderator",
        "model": "gemini/gemma-3-27b-it",
        "tagline": "Gemma 3 27B — open-weights model for balanced, grounded synthesis",
        "emoji": "⚖️",
        "color": "#66BB6A",
        "system_prompt": (
            "You are the Moderator — a measured, clear-headed synthesizer of perspectives. "
            "After hearing both enthusiastic research and devil's advocacy, your role is to find "
            "the nuanced middle path grounded in evidence. Acknowledge the strongest points from "
            "both sides, reconcile genuine tensions, and present a balanced conclusion that a "
            "thoughtful, senior expert would stand behind. Avoid both hype and excessive pessimism. "
            "Deliver calibrated confidence: strong where evidence is strong, uncertain where it isn't."
        ),
    },
]

CHAIRMAN = {
    "role": "The Chairman",
    "model": "gemini/gemini-2.5-pro",
    "tagline": "Gemini 2.5 Pro — orchestrates final verdict, hallucination check & synthesis",
    "emoji": "👑",
    "color": "#FFD700",
}

# ──────────────────────────────────────────────
#  CORE PIPELINE
# ──────────────────────────────────────────────

def query_expert(expert: dict, question: str) -> str:
    """Call a single expert model and return its response text."""
    response = litellm.completion(
        model=expert["model"],
        messages=[
            {"role": "system", "content": expert["system_prompt"]},
            {"role": "user", "content": question},
        ],
        api_key=os.getenv("GEMINI_API_KEY"),
    )
    return response.choices[0].message.content


def query_chairman(question: str, expert_responses: list[dict]) -> str:
    """Chairman synthesizes all expert drafts, checks hallucinations, issues verdict."""
    drafts_text = "\n\n".join(
        f"=== Expert {r['id']}: {r['role']} ===\n{r['response']}"
        for r in expert_responses
    )

    today = date.today().strftime("%B %d, %Y")
    chairman_prompt = f"""You are the Chairman of an elite AI Council. Today's date is {today}.

USER QUESTION:
{question}

You have received three expert reports below. Your tasks:
1. **Synthesize** them into one definitive, well-structured final answer.
2. **Highlight disagreements** between experts and explain which view the evidence favors.
3. **Flag hallucinations or unsupported claims** explicitly — mark them as [⚠️ UNVERIFIED].
4. **Issue a Final Verdict** — a clear, actionable conclusion.

{drafts_text}

Deliver your Chairman's Report now:"""

    response = litellm.completion(
        model=CHAIRMAN["model"],
        messages=[{"role": "user", "content": chairman_prompt}],
        api_key=os.getenv("GEMINI_API_KEY"),
    )
    return response.choices[0].message.content


def run_council(question: str, progress_callback=None) -> dict:
    """
    Run the full council pipeline.
    progress_callback(step: str, expert_id: int | None) called at each stage.
    Returns dict with expert_responses list and chairman_response str.
    """
    expert_responses = []

    for expert in EXPERTS:
        if progress_callback:
            progress_callback("expert_start", expert["id"])
        response_text = query_expert(expert, question)
        expert_responses.append(
            {
                "id": expert["id"],
                "role": expert["role"],
                "model": expert["model"],
                "emoji": expert["emoji"],
                "color": expert["color"],
                "tagline": expert["tagline"],
                "response": response_text,
            }
        )
        if progress_callback:
            progress_callback("expert_done", expert["id"])

    if progress_callback:
        progress_callback("chairman_start", None)

    chairman_response = query_chairman(question, expert_responses)

    if progress_callback:
        progress_callback("chairman_done", None)

    return {
        "question": question,
        "expert_responses": expert_responses,
        "chairman_response": chairman_response,
    }