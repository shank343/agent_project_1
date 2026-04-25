import streamlit as st
import json
from dotenv import load_dotenv
from multi_agent_research_system import create_research_system
 
load_dotenv()
 
@st.cache_resource
def get_research_system():
    return create_research_system()
 
# ── Page config ────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide",
)
 
# ── Global styles ───────────────────────────────────────────────
st.markdown("""
<style>
#MainMenu, footer, header { visibility: hidden; }
.terminal-box {
    background: #050508;
    border: 1px solid #1a1a2e;
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
    font-family: monospace;
    font-size: 0.85rem;
    line-height: 1.8;
    min-height: 120px;
    color: #00ffcc;
}
</style>
""", unsafe_allow_html=True)
 
# ── Header ──────────────────────────────────────────────────────
st.markdown("""
<div class="hero-title">Multi<span class="hero-accent">.</span>Agent<br>Research System</div>
<div class="hero-sub">// Powered by LangGraph &nbsp;·&nbsp; Groq &nbsp;·&nbsp; Parallel AI Agents</div>
""", unsafe_allow_html=True)
 
# ── Tabs ────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["ABOUT", "RESEARCH"])
 
# ════════════════════════════════════════════════════════════════
# TAB 1 — ABOUT
# ════════════════════════════════════════════════════════════════
with tab1:
 
    st.markdown('<div class="section-label">Project Overview</div>', unsafe_allow_html=True)
 
    # Placeholder: writeup
    st.markdown("""
    <div class="placeholder-card">
        <span class="icon">📝</span>
        <strong>PROJECT WRITEUP PLACEHOLDER</strong><br><br>
        Replace this with your project description —<br>
        what it does, why you built it, what you learned.
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown('<div class="section-label">Agent Pipeline</div>', unsafe_allow_html=True)
 
    # Pipeline diagram
    st.markdown("""
    <div class="pipeline">
        <div class="agent-node highlight">USER TOPIC</div>
        <span class="arrow">→</span>
        <div class="agent-node">SUPERVISOR</div>
        <span class="arrow">→</span>
        <div class="agent-node">SEARCH ×3-5<br><span style="font-size:0.6rem;color:#333355">parallel</span></div>
        <span class="arrow">→</span>
        <div class="agent-node">ANALYST</div>
        <span class="arrow">→</span>
        <div class="agent-node">WRITER</div>
        <span class="arrow">→</span>
        <div class="agent-node">QUALITY CHECK</div>
        <span class="arrow">→</span>
        <div class="agent-node highlight">REPORT</div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown('<div class="section-label">Flow Diagram</div>', unsafe_allow_html=True)
 
    # Placeholder: flow diagram image
    st.markdown("""
    <div class="placeholder-card" style="min-height: 220px; display:flex; flex-direction:column; align-items:center; justify-content:center;">
        <span class="icon">🗺️</span>
        <strong>FLOW DIAGRAM PLACEHOLDER</strong><br><br>
        Replace this with your LangGraph diagram image.<br>
        <span style="font-size:0.7rem; margin-top:0.5rem;">Hint: your code already saves it as <code style="color:#00ffcc">research_graph.png</code></span>
    </div>
    """, unsafe_allow_html=True)
 
 
# ════════════════════════════════════════════════════════════════
# TAB 2 — RESEARCH
# ════════════════════════════════════════════════════════════════
with tab2:
 
    st.markdown('<div class="section-label">Start a Research Run</div>', unsafe_allow_html=True)
 
    col1, col2 = st.columns([5, 1])
    with col1:
        topic = st.text_input(
            "Please choose a topic",
            placeholder="e.g. The future of quantum computing...",
            key="topic_input",
            label_visibility="visible"
        )
    with col2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run = st.button("▶ RUN", disabled=not topic.strip())
 
    st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)
 
    # ── Terminal log placeholder ─────────────────────────────
    log_placeholder = st.empty()
    report_placeholder = st.empty()
 
    def render_log(lines):
        def style_line(line):
            if "[supervisor]" in line.lower():
                return f'<p class="log-line log-supervisor">{line}</p>'
            elif "[search" in line.lower():
                return f'<p class="log-line log-search">{line}</p>'
            elif "[analyst]" in line.lower():
                return f'<p class="log-line log-analyst">{line}</p>'
            elif "[report" in line.lower() or "[writer]" in line.lower():
                return f'<p class="log-line log-writer">{line}</p>'
            elif "[quality" in line.lower():
                return f'<p class="log-line log-quality">{line}</p>'
            elif "✓" in line or "done" in line.lower() or "complete" in line.lower():
                return f'<p class="log-line log-done">{line}</p>'
            else:
                return f'<p class="log-line log-system">{line}</p>'
 
        html = '<div class="terminal-box">' + "".join(style_line(l) for l in lines) + '</div>'
        log_placeholder.markdown(html, unsafe_allow_html=True)
 
    # Show idle state
    if not run:
        render_log(["// Waiting for topic input..."])
 
    # ── On RUN ───────────────────────────────────────────────
    if run and topic.strip():
        logs = []
 
        def add_log(msg):
            logs.append(msg)
            render_log(logs)
 
        add_log(f"// Topic: {topic}")
        add_log("// Starting pipeline...")
        add_log("")
        add_log("[SUPERVISOR]  Planning search queries...")
 
        try:
            add_log("[SEARCH]      Dispatching parallel agents...")
            add_log("              Number of agents decided by supervisor (3-5)...")
 
            research_system = get_research_system()
 
            result = research_system.invoke({
                "messages": [],
                "topic": topic,
                "search_queries": [],
                "findings": [],
                "analysis": "",
                "report": "",
                "quality_score": 0.0,
                "quality_feedback": "",
                "iteration": 0,
            })
 
            add_log("[ANALYST]     Synthesising findings...")
            add_log("[WRITER]      Drafting report...")
            add_log(f"[QUALITY]     Score: {result['quality_score']:.2f}  |  Iterations: {result['iteration']}")
            add_log("")
            add_log("✓ Pipeline complete.")
 
            # ── Report ───────────────────────────────────
            report_placeholder.markdown(f"""
            <div class="report-wrapper">
                <div class="report-meta">
                    <div class="meta-item">QUALITY SCORE &nbsp;<span class="meta-value">{result['quality_score']:.2f}</span></div>
                    <div class="meta-item">ITERATIONS &nbsp;<span class="meta-value">{result['iteration']}</span></div>
                    <div class="meta-item">TOPIC &nbsp;<span class="meta-value">{topic[:60]}</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
 
            st.markdown(result["report"])
 
        except Exception as e:
            add_log(f"✗ Error: {str(e)}")