"""
app.py — LLM Council Streamlit UI
===================================
Run with:  streamlit run app.py
Requires:  council_core.py + .env with GEMINI_API_KEY
"""

import streamlit as st
from council_core import EXPERTS, CHAIRMAN, run_council

# ──────────────────────────────────────────────
#  PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="LLM Council",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
#  STYLING
# ──────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;600&family=DM+Serif+Display&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #0D0D0D;
        color: #D8D4CC;
    }

    .main-title {
        font-family: 'DM Serif Display', serif;
        font-size: 2.8rem;
        font-weight: 400;
        letter-spacing: -0.5px;
        color: #E8E0D0;
        text-align: center;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        text-align: center;
        color: #555;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.78rem;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        margin-bottom: 2.5rem;
    }

    /* Expert cards row */
    .expert-card {
        border-radius: 10px;
        border: 1px solid #222;
        background: #111;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.8rem;
        position: relative;
        overflow: hidden;
    }

    .expert-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 3px; height: 100%;
        border-radius: 3px 0 0 3px;
        background: #2a2a2a;
    }

    .expert-role {
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        margin: 0;
        color: #E0DDD8;
        letter-spacing: -0.2px;
    }

    .expert-model {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.68rem;
        color: #555;
        margin-top: 0.3rem;
    }

    .expert-tagline {
        font-size: 0.82rem;
        color: #888;
        margin-top: 0.5rem;
        line-height: 1.4;
    }

    /* Chairman block */
    .chairman-box {
        border: 1px solid #2a2a2a;
        border-top: 2px solid #C8B97A;
        border-radius: 10px;
        background: #0f0f0d;
        padding: 2rem 2.2rem;
        margin-top: 1.5rem;
    }

    .chairman-header {
        font-family: 'DM Serif Display', serif;
        font-size: 1.4rem;
        color: #C8B97A;
        font-weight: 400;
        margin-bottom: 1.2rem;
        letter-spacing: 0.2px;
    }

    /* Code snippet box */
    .code-section {
        border: 1px solid #2a2a2a;
        border-radius: 10px;
        background: #0a0a0a;
        padding: 1.5rem;
        margin-top: 1rem;
    }

    .code-section-title {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #FFD700;
        margin-bottom: 0.8rem;
    }

    /* Input box */
    .stTextArea textarea {
        background: #141414 !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
        color: #E8E0D0 !important;
        font-family: 'Source Serif 4', serif !important;
        font-size: 1rem !important;
    }

    /* Button */
    .stButton > button {
        background: #C8B97A !important;
        color: #0D0D0D !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        letter-spacing: 1.5px !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.65rem 2rem !important;
        width: 100%;
        cursor: pointer;
        transition: opacity 0.2s;
    }

    .stButton > button:hover {
        opacity: 0.8 !important;
    }

    /* Expander */
    details > summary {
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.8rem !important;
        letter-spacing: 1px !important;
        color: #aaa !important;
        cursor: pointer;
    }

    /* Divider */
    hr {
        border-color: #222;
        margin: 2rem 0;
    }

    /* Status messages */
    .status-pill {
        display: inline-block;
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 20px;
        padding: 0.2rem 0.8rem;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.75rem;
        color: #aaa;
    }

    .status-pill.active {
        border-color: #FFD700;
        color: #FFD700;
    }

    .section-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #555;
        margin-bottom: 1rem;
        margin-top: 2rem;
    }

    /* Chairman content markdown area */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] .stMarkdown p,
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] .stMarkdown li,
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] .stMarkdown h1,
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] .stMarkdown h2,
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] .stMarkdown h3 {
        color: #D8D4CC;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
#  HEADER
# ──────────────────────────────────────────────
st.markdown('<div class="main-title">⚖️ The LLM Council</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Multi-Expert AI Deliberation · Powered by Gemini</div>',
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
#  COUNCIL COMPOSITION (always visible)
# ──────────────────────────────────────────────
st.markdown('<div class="section-label">Council Composition</div>', unsafe_allow_html=True)

all_members = EXPERTS + [CHAIRMAN]
cols = st.columns(len(all_members))

for col, member in zip(cols, all_members):
    with col:
        is_chairman = member.get("role") == CHAIRMAN["role"] and len(member) < 7
        border_color = member["color"]
        st.markdown(
            f"""
            <div class="expert-card">
                <div class="expert-role">{member["emoji"]} {member["role"]}</div>
                <div class="expert-model">{member["model"]}</div>
                <div class="expert-tagline">{member["tagline"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<hr>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  CORE LOGIC SNIPPET (always visible)
# ──────────────────────────────────────────────
st.markdown('<div class="section-label">How It Works — Core Pipeline</div>', unsafe_allow_html=True)

with st.expander("📋 View Core Backend Logic", expanded=False):
    st.code(
        '''\
# STAGE 1 — Each expert answers independently with its own system prompt
for expert in EXPERTS:
    response = litellm.completion(
        model=expert["model"],
        messages=[
            {"role": "system", "content": expert["system_prompt"]},
            {"role": "user",   "content": question},
        ]
    )
    expert_responses.append(response.choices[0].message.content)

# STAGE 2 — Chairman synthesizes all drafts, flags hallucinations
chairman_prompt = f"""
You are the Chairman of an elite AI Council.
USER QUESTION: {question}

You received three expert reports. Your tasks:
1. Synthesize them into one definitive answer.
2. Highlight disagreements and which view evidence favors.
3. Flag hallucinations / unsupported claims as [⚠️ UNVERIFIED].
4. Issue a clear Final Verdict.

{expert_drafts}
"""
final = litellm.completion(model=CHAIRMAN["model"],
                            messages=[{"role": "user", "content": chairman_prompt}])
''',
        language="python",
    )

st.markdown("<hr>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  QUESTION INPUT
# ──────────────────────────────────────────────
st.markdown('<div class="section-label">Pose Your Question</div>', unsafe_allow_html=True)

question = st.text_area(
    label="",
    placeholder="Ask the council anything — complex, controversial, technical, or speculative…",
    height=120,
    key="question_input",
    label_visibility="collapsed",
)

col_btn, col_space = st.columns([1, 3])
with col_btn:
    submit = st.button("⚖️  Convene the Council")

st.markdown("<hr>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
#  COUNCIL RUN
# ──────────────────────────────────────────────
if submit:
    if not question.strip():
        st.warning("Please enter a question before convening the council.")
        st.stop()

    st.markdown(
        '<div class="section-label">Council in Session</div>', unsafe_allow_html=True
    )

    # Progress area
    status_area = st.empty()
    progress_bar = st.progress(0)

    total_steps = len(EXPERTS) + 1  # 3 experts + chairman
    step = [0]

    expert_placeholders = {}
    for expert in EXPERTS:
        expert_placeholders[expert["id"]] = st.empty()

    chairman_placeholder = st.empty()

    # Collect results as they come in
    results_store = {"experts": [], "chairman": None}

    # Run with streaming status updates
    def on_progress(stage: str, expert_id):
        if stage == "expert_start":
            expert = next(e for e in EXPERTS if e["id"] == expert_id)
            status_area.markdown(
                f'<span class="status-pill active">🔄 {expert["emoji"]} {expert["role"]} is deliberating…</span>',
                unsafe_allow_html=True,
            )
        elif stage == "expert_done":
            step[0] += 1
            progress_bar.progress(step[0] / total_steps)
        elif stage == "chairman_start":
            status_area.markdown(
                f'<span class="status-pill active">👑 Chairman is reviewing all drafts…</span>',
                unsafe_allow_html=True,
            )
        elif stage == "chairman_done":
            step[0] += 1
            progress_bar.progress(step[0] / total_steps)
            status_area.markdown(
                '<span class="status-pill">✅ Council deliberation complete.</span>',
                unsafe_allow_html=True,
            )

    # Run the council
    with st.spinner(""):
        result = run_council(question.strip(), progress_callback=on_progress)

    progress_bar.progress(1.0)

    # ── EXPERT RESPONSES (collapsible) ──────────
    st.markdown(
        '<div class="section-label">Expert Drafts</div>', unsafe_allow_html=True
    )

    for er in result["expert_responses"]:
        with st.expander(
            f"{er['emoji']}  Expert {er['id']} — {er['role']}  ({er['model']})",
            expanded=False,
        ):
            st.markdown(
                f'<div style="color:{er["color"]}; font-family: IBM Plex Mono, monospace; '
                f'font-size:0.72rem; margin-bottom:0.6rem;">{er["tagline"]}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(er["response"])

    # ── CHAIRMAN VERDICT (fully expanded) ───────
    st.markdown(
        '<div class="section-label">Chairman\'s Final Verdict</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="
            display: flex;
            align-items: center;
            gap: 0.8rem;
            margin-bottom: 1.2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #2a2a2a;
            border-left: 3px solid #C8B97A;
            padding-left: 1rem;
        ">
            <span style="
                font-family: 'DM Serif Display', serif;
                font-size: 1.4rem;
                color: #C8B97A;
                letter-spacing: 0.2px;
            ">👑 Chairman's Report</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(result["chairman_response"])

# ──────────────────────────────────────────────
#  FOOTER
# ──────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    '<div style="text-align:center; font-family: IBM Plex Mono, monospace; '
    'font-size:0.68rem; color:#333; letter-spacing:2.5px;">'
    "LLM COUNCIL · ALL MODELS VIA GEMINI API · LITELLM"
    "</div>",
    unsafe_allow_html=True,
)