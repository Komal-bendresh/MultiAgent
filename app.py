import html
import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Mate · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&display=swap');

:root {
    --bg: #06060f;
    --surface: rgba(255,255,255,0.035);
    --surface-hi: rgba(255,255,255,0.06);
    --line: rgba(255,255,255,0.08);
    --text: #ebeaf7;
    --muted: #a09fbc;
    --faint: #5d5b78;
    --orange: #8b5cf6;
    --orange-2: #ec4899;
    --green: #34d399;
    --radius: 18px;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}
.stApp {
    background: var(--bg);
    background-image:
        radial-gradient(ellipse 70% 45% at 15% -8%, rgba(139,92,246,0.16) 0%, transparent 60%),
        radial-gradient(ellipse 55% 40% at 90% 105%, rgba(34,211,238,0.10) 0%, transparent 55%),
        radial-gradient(circle at 1px 1px, rgba(255,255,255,0.045) 1px, transparent 0);
    background-size: auto, auto, 28px 28px;
    background-attachment: fixed;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 3rem 4rem; max-width: 1240px; }

::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-thumb { background: rgba(139,92,246,0.25); border-radius: 8px; }
::-webkit-scrollbar-track { background: transparent; }

/* ── Hero ── */
.hero { text-align: center; padding: 3rem 0 1.5rem; position: relative; }
.hero-badge {
    display: inline-flex; align-items: center; gap: 0.55rem;
    font-family: 'DM Mono', monospace; font-size: 0.68rem; font-weight: 500;
    letter-spacing: 0.22em; text-transform: uppercase; color: var(--orange);
    background: rgba(139,92,246,0.08);
    border: 1px solid rgba(139,92,246,0.25);
    padding: 0.4rem 0.95rem; border-radius: 999px; margin-bottom: 1.4rem;
}
.hero-badge .dot {
    width: 6px; height: 6px; border-radius: 50%; background: var(--orange);
    box-shadow: 0 0 10px var(--orange);
    animation: pulse 2s ease-in-out infinite;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6.5vw, 5.2rem);
    font-weight: 800; line-height: 1.02; letter-spacing: -0.035em;
    color: #f5f4ff; margin: 0 0 1.1rem;
}
.hero h1 span {
    background: linear-gradient(120deg, #c4b5fd 0%, #8b5cf6 45%, #ec4899 100%);
    -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 1.06rem; font-weight: 300; color: var(--muted);
    max-width: 560px; margin: 0 auto; line-height: 1.7;
}
.hero-stats {
    display: flex; justify-content: center; gap: 0.7rem; flex-wrap: wrap; margin-top: 1.8rem;
}
.hero-stat {
    font-family: 'DM Mono', monospace; font-size: 0.68rem; letter-spacing: 0.1em;
    color: var(--muted); background: var(--surface); border: 1px solid var(--line);
    padding: 0.35rem 0.8rem; border-radius: 8px;
}
.hero-stat b { color: var(--orange); font-weight: 500; margin-right: 0.3rem; }

/* ── Divider ── */
.divider {
    height: 1px; margin: 2rem 0;
    background: linear-gradient(90deg, transparent, rgba(139,92,246,0.35), transparent);
}

/* ── Bordered containers (input, report, feedback) ── */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--surface);
    border: 1px solid rgba(139,92,246,0.16) !important;
    border-radius: var(--radius) !important;
    padding: 0.4rem 0.6rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 10px 40px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.04);
}
/* don't double-style nested wrappers (e.g. inside expanders) */
div[data-testid="stExpander"] div[data-testid="stVerticalBlockBorderWrapper"] {
    background: transparent; border: none !important; box-shadow: none; padding: 0;
}

/* ── Inputs ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(139,92,246,0.25) !important;
    border-radius: 12px !important;
    color: #f5f4ff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.02rem !important;
    padding: 0.85rem 1.05rem !important;
    transition: border-color 0.2s, box-shadow 0.2s, background 0.2s !important;
}
.stTextInput > div > div > input::placeholder { color: var(--faint) !important; }
.stTextInput > div > div > input:focus {
    border-color: var(--orange) !important;
    background: rgba(139,92,246,0.04) !important;
    box-shadow: 0 0 0 4px rgba(139,92,246,0.12) !important;
}
.stTextInput > label, .stTextInput label p {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: var(--orange) !important;
    font-weight: 500 !important;
}

/* ── Buttons ── */
.stButton > button, .stDownloadButton > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.2s, filter 0.2s, background 0.2s !important;
}
.stButton > button {
    background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 40%, #ec4899 100%) !important;
    color: #ffffff !important;
    border: none !important;
    box-shadow: 0 6px 24px rgba(139,92,246,0.32), inset 0 1px 0 rgba(255,255,255,0.35) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 32px rgba(139,92,246,0.45), inset 0 1px 0 rgba(255,255,255,0.35) !important;
    filter: brightness(1.05);
}
.stButton > button:active { transform: translateY(0) !important; }
.stDownloadButton > button {
    background: rgba(52,211,153,0.08) !important;
    color: var(--green) !important;
    border: 1px solid rgba(52,211,153,0.35) !important;
    margin-top: 1rem;
}
.stDownloadButton > button:hover {
    background: rgba(52,211,153,0.16) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(52,211,153,0.2) !important;
}

/* ── Example chips ── */
.chips { display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: center; margin: 1.1rem 0 0.4rem; }
.chips-label {
    font-family: 'DM Mono', monospace; font-size: 0.68rem;
    color: var(--faint); letter-spacing: 0.14em; margin-right: 0.2rem;
}
.chip {
    background: var(--surface); border: 1px solid var(--line); border-radius: 999px;
    padding: 0.3rem 0.85rem; font-size: 0.78rem; color: var(--muted);
    font-family: 'DM Sans', sans-serif; transition: all 0.2s; cursor: default;
}
.chip:hover { border-color: rgba(139,92,246,0.4); color: var(--orange); background: rgba(139,92,246,0.06); }

/* ── Pipeline header + progress ── */
.pipe-head { display: flex; align-items: baseline; justify-content: space-between; margin: 0.2rem 0 0.7rem; }
.section-heading {
    font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 700;
    color: #f5f4ff; margin: 0; letter-spacing: -0.01em;
}
.pipe-count { font-family: 'DM Mono', monospace; font-size: 0.7rem; letter-spacing: 0.12em; color: var(--muted); }
.progress { height: 4px; background: rgba(255,255,255,0.06); border-radius: 4px; overflow: hidden; margin-bottom: 1.2rem; }
.progress > div {
    height: 100%; border-radius: 4px;
    background: linear-gradient(90deg, var(--orange), var(--orange-2));
    box-shadow: 0 0 12px rgba(139,92,246,0.6);
    transition: width 0.5s ease;
}

/* ── Step cards ── */
.step-card {
    background: var(--surface); border: 1px solid var(--line);
    border-radius: 14px; padding: 1.1rem 1.4rem 1.1rem 1.6rem;
    margin-bottom: 0.85rem; position: relative; overflow: hidden;
    transition: border-color 0.3s, background 0.3s, transform 0.3s;
}
.step-card::before {
    content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px;
    background: rgba(255,255,255,0.07); transition: background 0.3s;
}
.step-card.active {
    border-color: rgba(139,92,246,0.45);
    background: linear-gradient(135deg, rgba(139,92,246,0.08), rgba(139,92,246,0.02));
    box-shadow: 0 0 30px rgba(139,92,246,0.10);
}
.step-card.active::before { background: var(--orange); box-shadow: 0 0 14px var(--orange); }
.step-card.active::after {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(100deg, transparent 30%, rgba(139,92,246,0.08) 50%, transparent 70%);
    background-size: 220% 100%; animation: sweep 2.2s linear infinite; pointer-events: none;
}
.step-card.done { border-color: rgba(52,211,153,0.3); background: rgba(52,211,153,0.035); }
.step-card.done::before { background: var(--green); }

.step-header { display: flex; align-items: center; gap: 0.8rem; }
.step-num {
    font-family: 'DM Mono', monospace; font-size: 0.7rem; font-weight: 500; letter-spacing: 0.12em;
    color: var(--orange); background: rgba(139,92,246,0.1);
    width: 2rem; height: 2rem; border-radius: 9px;
    display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.step-card.done .step-num { color: var(--green); background: rgba(52,211,153,0.12); }
.step-card:not(.active):not(.done) .step-num { color: var(--faint); background: rgba(255,255,255,0.04); }
.step-title { font-family: 'Syne', sans-serif; font-size: 0.97rem; font-weight: 700; color: #f5f4ff; }
.step-status {
    margin-left: auto; font-family: 'DM Mono', monospace; font-size: 0.64rem; letter-spacing: 0.12em;
    padding: 0.2rem 0.55rem; border-radius: 6px; white-space: nowrap;
}
.status-waiting { color: var(--faint); background: rgba(255,255,255,0.04); }
.status-running { color: var(--orange); background: rgba(139,92,246,0.12); animation: pulse 1.6s ease-in-out infinite; }
.status-done    { color: var(--green); background: rgba(52,211,153,0.12); }
.step-desc { font-size: 0.82rem; color: #7f7d9c; margin: 0.45rem 0 0 2.8rem; line-height: 1.5; }

/* ── Result panels (raw outputs) ── */
.result-panel {
    background: rgba(0,0,0,0.25); border: 1px solid var(--line);
    border-radius: 14px; padding: 1.4rem 1.6rem; margin: 0.4rem 0 0.6rem;
}
.result-panel-title {
    font-family: 'DM Mono', monospace; font-size: 0.68rem; font-weight: 500;
    letter-spacing: 0.2em; text-transform: uppercase; color: var(--orange);
    margin-bottom: 0.9rem; padding-bottom: 0.7rem; border-bottom: 1px solid rgba(139,92,246,0.15);
}
.result-content {
    font-size: 0.9rem; line-height: 1.8; color: #cfcde6;
    white-space: pre-wrap; font-family: 'DM Sans', sans-serif; word-break: break-word;
}

/* ── Report & feedback labels ── */
.panel-label {
    display: flex; align-items: center; gap: 0.6rem;
    font-family: 'DM Mono', monospace; font-size: 0.72rem; font-weight: 500;
    letter-spacing: 0.2em; text-transform: uppercase;
    margin: 0.4rem 0 1.2rem; padding-bottom: 0.9rem;
}
.panel-label.orange { color: var(--orange); border-bottom: 1px solid rgba(139,92,246,0.2); }
.panel-label.green  { color: var(--green);  border-bottom: 1px solid rgba(52,211,153,0.22); }

/* Markdown typography inside results */
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    font-family: 'Syne', sans-serif; color: #f5f4ff; letter-spacing: -0.01em;
}
.stMarkdown h2 { margin-top: 1.6rem; padding-bottom: 0.4rem; border-bottom: 1px solid var(--line); }
.stMarkdown p, .stMarkdown li { line-height: 1.8; color: #d6d4ec; }
.stMarkdown a { color: var(--orange) !important; text-decoration: none; border-bottom: 1px dashed rgba(139,92,246,0.5); }
.stMarkdown code { background: rgba(139,92,246,0.1); color: #c4b5fd; padding: 0.1rem 0.4rem; border-radius: 5px; }
.stMarkdown blockquote { border-left: 3px solid var(--orange); background: var(--surface); padding: 0.4rem 1rem; border-radius: 0 8px 8px 0; }

/* ── Expander ── */
div[data-testid="stExpander"] {
    background: var(--surface); border: 1px solid var(--line) !important;
    border-radius: 14px !important; margin-bottom: 0.7rem; overflow: hidden;
}
div[data-testid="stExpander"] summary:hover { background: rgba(139,92,246,0.05); }
details summary {
    font-family: 'DM Mono', monospace !important; font-size: 0.76rem !important;
    color: var(--muted) !important; letter-spacing: 0.08em !important; cursor: pointer;
}

/* ── Misc ── */
.stSpinner > div { color: var(--orange) !important; }
.stAlert { border-radius: 12px !important; }
.notice {
    font-family: 'DM Mono', monospace; font-size: 0.7rem; color: var(--faint);
    text-align: center; margin-top: 3.5rem; letter-spacing: 0.08em;
}
.notice span { color: var(--orange); }

/* ── Animations ── */
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.45; } }
@keyframes sweep { 0% { background-position: 120% 0; } 100% { background-position: -120% 0; } }

@media (max-width: 900px) {
    .block-container { padding: 1rem 1.1rem 3rem; }
    .hero { padding-top: 1.5rem; }
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    desc_html = f'<div class="step-desc">{desc}</div>' if desc else ""
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {desc_html}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge"><span class="dot"></span>Multi-Agent AI System</div>
    <h1>Research<span>Mate</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping, writing,
        and critiquing — to deliver a polished research report on any topic.
    </p>
    <div class="hero-stats">
        <span class="hero-stat"><b>01</b>Search</span>
        <span class="hero-stat"><b>02</b>Read</span>
        <span class="hero-stat"><b>03</b>Write</span>
        <span class="hero-stat"><b>04</b>Critique</span>
    </div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    with st.container(border=True):
        topic = st.text_input(
            "Research Topic",
            placeholder="e.g. Quantum computing breakthroughs in 2025",
            key="topic_input",
            label_visibility="visible",
        )
        run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)

    # Example chips
    chips = "".join(
        f'<span class="chip">{ex}</span>'
        for ex in ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]
    )
    st.markdown(
        f'<div class="chips"><span class="chips-label">TRY →</span>{chips}</div>',
        unsafe_allow_html=True,
    )

PIPELINE_STEPS = ["search", "reader", "writer", "critic"]


def step_state(step):
    r_ = st.session_state.results
    if step in r_:
        return "done"
    if st.session_state.running:
        for k in PIPELINE_STEPS:
            if k not in r_:
                return "running" if k == step else "waiting"
    return "waiting"


def render_pipeline():
    r_ = st.session_state.results
    n_done = sum(1 for k in PIPELINE_STEPS if k in r_)
    pct = int(n_done / len(PIPELINE_STEPS) * 100)
    st.markdown(f"""
    <div class="pipe-head">
        <div class="section-heading">Pipeline</div>
        <div class="pipe-count">{n_done}/{len(PIPELINE_STEPS)} COMPLETE</div>
    </div>
    <div class="progress"><div style="width:{pct}%"></div></div>
    """, unsafe_allow_html=True)
    step_card("01", "Search Agent", step_state("search"), "Gathers recent web information")
    step_card("02", "Reader Agent", step_state("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain", step_state("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain", step_state("critic"), "Reviews & scores the report")


with col_pipeline:
    pipeline_slot = st.empty()
    with pipeline_slot.container():
        render_pipeline()


def refresh_pipeline():
    with pipeline_slot.container():
        render_pipeline()


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("🔍  Search Agent is working…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)
    refresh_pipeline()

    # ── Step 2: Reader ──
    with st.spinner("📄  Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)
    refresh_pipeline()

    # ── Step 3: Writer ──
    with st.spinner("✍️  Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)
    refresh_pipeline()

    # ── Step 4: Critic ──
    with st.spinner("🧐  Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    # Raw outputs in expanders
    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Search Agent Output</div>'
                        f'<div class="result-content">{html.escape(str(r["search"]))}</div></div>',
                        unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Reader Agent Output</div>'
                        f'<div class="result-content">{html.escape(str(r["reader"]))}</div></div>',
                        unsafe_allow_html=True)

    # Final report
    if "writer" in r:
        with st.container(border=True):
            st.markdown('<div class="panel-label orange">📝 Final Research Report</div>',
                        unsafe_allow_html=True)
            st.markdown(r["writer"])   # render markdown natively

        # Download
        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:
        st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown('<div class="panel-label green">🧐 Critic Feedback</div>',
                        unsafe_allow_html=True)
            st.markdown(r["critic"])


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    <span>Research Mate</span> · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)