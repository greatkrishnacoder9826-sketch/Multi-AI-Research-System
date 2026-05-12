import streamlit as st
import threading
import time
from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Astavakara 🗿",
    page_icon="🗿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

* { font-family: 'Syne', sans-serif; }
code, pre, .mono { font-family: 'DM Mono', monospace; }

/* Dark background */
.stApp {
    background: #0a0a0f;
    color: #e8e8f0;
}

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem; max-width: 1200px; }

/* Hero Title */
.hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 0.3rem;
}
.hero-sub {
    font-size: 1rem;
    color: #6b7280;
    font-weight: 400;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
}

/* Input area */
.stTextInput > div > div > input {
    background: #13131f !important;
    border: 1px solid #2d2d45 !important;
    border-radius: 12px !important;
    color: #e8e8f0 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.9rem 1.2rem !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.15) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #4b5563 !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.75rem 2rem !important;
    letter-spacing: 0.03em !important;
    transition: all 0.2s !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(124,58,237,0.4) !important;
}

/* Step cards */
.step-card {
    background: #13131f;
    border: 1px solid #1e1e30;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.3s;
}
.step-card.active {
    border-color: #a78bfa;
    box-shadow: 0 0 20px rgba(167,139,250,0.1);
}
.step-card.done {
    border-color: #34d399;
    box-shadow: 0 0 15px rgba(52,211,153,0.08);
}
.step-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.step-label.active { color: #a78bfa; }
.step-label.done { color: #34d399; }
.step-label.pending { color: #374151; }
.step-title {
    font-size: 1rem;
    font-weight: 600;
    color: #e8e8f0;
}
.step-title.pending { color: #374151; }

/* Result containers */
.result-box {
    background: #0f0f1a;
    border: 1px solid #1e1e30;
    border-radius: 14px;
    padding: 1.5rem;
    margin-top: 1rem;
    font-size: 0.9rem;
    line-height: 1.7;
    color: #c4c4d4;
    white-space: pre-wrap;
    font-family: 'DM Mono', monospace;
    max-height: 300px;
    overflow-y: auto;
}
.report-box {
    background: #0f0f1a;
    border: 1px solid #2d2d45;
    border-radius: 14px;
    padding: 2rem;
    margin-top: 1rem;
    line-height: 1.9;
    color: #d1d5db;
    font-size: 0.95rem;
}

/* Score badge */
.score-badge {
    display: inline-block;
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    color: white;
    font-family: 'DM Mono', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    padding: 0.4rem 1.2rem;
    border-radius: 50px;
    margin-bottom: 1rem;
}

/* Divider */
.my-divider {
    border: none;
    border-top: 1px solid #1e1e30;
    margin: 2rem 0;
}

/* Spinner override */
.stSpinner > div { border-top-color: #a78bfa !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2d2d45; border-radius: 5px; }

/* Tab style */
.stTabs [data-baseweb="tab-list"] {
    background: #13131f;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #1e1e30;
}
.stTabs [data-baseweb="tab"] {
    color: #6b7280 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
}
.stTabs [aria-selected="true"] {
    background: #7c3aed !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">Astavakara ❤️‍🔥</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Made_by_Paradox &nbsp;·&nbsp; Powered Krishna_Great </div>', unsafe_allow_html=True)

# ─── Input ──────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([4, 1])
with col1:
    topic = st.text_input(
        label="",
        placeholder="Enter a research topic'",
        key="topic_input",
        label_visibility="collapsed"
    )
with col2:
    run_btn = st.button(" Research", use_container_width=True)

st.markdown('<hr class="my-divider">', unsafe_allow_html=True)

# ─── Pipeline Steps Definition ───────────────────────────────────────────────────
STEPS = [
    {"icon": " ", "label": "Step 1", "title": "Search Agent — Finding Sources"},
    {"icon": " ", "label": "Step 2", "title": "Reader Agent — Scraping Content"},
    {"icon": " ", "label": "Step 3", "title": "Writer — Drafting Report"},
    {"icon": " ", "label": "Step 4", "title": "Critic — Reviewing Report"},
]

def render_steps(current_step=-1, done_steps=set()):
    cols = st.columns(4)
    for i, step in enumerate(STEPS):
        with cols[i]:
            if i in done_steps:
                status = "done"
                icon = ""
            elif i == current_step:
                status = "active"
                icon = step["icon"]
            else:
                status = "pending"
                icon = step["icon"]

            st.markdown(f"""
            <div class="step-card {status}">
                <div class="step-label {status}">{step['label']}</div>
                <div class="step-title {'pending' if status=='pending' else ''}">
                    {icon} {step['title']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ─── Main Logic ─────────────────────────────────────────────────────────────────
if run_btn and topic.strip():

    steps_placeholder = st.empty()
    content_placeholder = st.empty()

    state = {}
    done = set()

    # ── STEP 1: Search ──────────────────────────────────────────────────────────
    with steps_placeholder.container():
        render_steps(current_step=0, done_steps=done)

    with content_placeholder.container():
        with st.spinner(" Search Agent is hunting the web..."):
            try:
                search_agent = build_search_agent()
                result = search_agent.invoke({
                    "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
                })
                state["search_results"] = result['messages'][-1].content
            except Exception as e:
                state["search_results"] = f"Search failed: {str(e)}"

    done.add(0)

    # ── STEP 2: Reader ──────────────────────────────────────────────────────────
    with steps_placeholder.container():
        render_steps(current_step=1, done_steps=done)

    with content_placeholder.container():
        with st.spinner(" Reader Agent is scraping top sources..."):
            try:
                reader_agent = build_reader_agent()
                result = reader_agent.invoke({
                    "messages": [("user",
                        f"Based on the following search results about '{topic}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{state['search_results'][:800]}"
                    )]
                })
                state["scraped_content"] = result['messages'][-1].content
            except Exception as e:
                state["scraped_content"] = f"Scraping failed: {str(e)}"

    done.add(1)

    # ── STEP 3: Writer ──────────────────────────────────────────────────────────
    with steps_placeholder.container():
        render_steps(current_step=2, done_steps=done)

    with content_placeholder.container():
        with st.spinner(" Writer is drafting the full report..."):
            research_combined = (
                f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
            )
            try:
                state["report"] = writer_chain.invoke({
                    "topic": topic,
                    "research": research_combined
                })
            except Exception as e:
                state["report"] = f"Writing failed: {str(e)}"

    done.add(2)

    # ── STEP 4: Critic ──────────────────────────────────────────────────────────
    with steps_placeholder.container():
        render_steps(current_step=3, done_steps=done)

    with content_placeholder.container():
        with st.spinner(" Critic is reviewing the report..."):
            try:
                state["feedback"] = critic_chain.invoke({"report": state["report"]})
            except Exception as e:
                state["feedback"] = f"Critique failed: {str(e)}"

    done.add(3)

    # ── All Done ────────────────────────────────────────────────────────────────
    with steps_placeholder.container():
        render_steps(current_step=-1, done_steps=done)

    content_placeholder.empty()
    st.markdown('<hr class="my-divider">', unsafe_allow_html=True)

    # ── Results Tabs ────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs([" Full Report", " Critic Feedback", " Raw Research"])

    with tab1:
        st.markdown("###  Research Report")
        st.markdown(f'<div class="report-box">{state["report"]}</div>', unsafe_allow_html=True)
        st.download_button(
            label="⬇ Download Report",
            data=state["report"],
            file_name=f"research_{topic[:30].replace(' ','_')}.txt",
            mime="text/plain"
        )

    with tab2:
        st.markdown("###  Critic's Review")
        feedback = state["feedback"]
        # Extract score if present
        score_line = ""
        for line in feedback.split("\n"):
            if line.strip().lower().startswith("score"):
                score_line = line.strip().replace("Score:", "").replace("score:", "").strip()
                break
        if score_line:
            st.markdown(f'<div class="score-badge">Score: {score_line}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="report-box">{feedback}</div>', unsafe_allow_html=True)

    with tab3:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("####  Search Results")
            st.markdown(f'<div class="result-box">{state["search_results"]}</div>', unsafe_allow_html=True)
        with col_b:
            st.markdown("####  Scraped Content")
            st.markdown(f'<div class="result-box">{state["scraped_content"]}</div>', unsafe_allow_html=True)

elif run_btn and not topic.strip():
    st.warning(" Pehle topic daalo bhai!", icon="")

else:
    # ── Empty state ─────────────────────────────────────────────────────────────
    render_steps(current_step=-1, done_steps=set())
    st.markdown("""
    <div style="text-align:center; margin-top: 3rem; color: #374151;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🔬</div>
        <div style="font-size: 1.1rem; font-weight: 600; color: #4b5563;">Enter a topic above and hit Research</div>
        <div style="font-size: 0.85rem; margin-top: 0.5rem; color: #374151;">
            4 AI agents will search, scrape, write & critique — automatically
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    
    #streamlit run app.py