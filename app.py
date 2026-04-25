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
.log-line { margin: 0; padding: 0; }
.log-supervisor { color: #ffaa00; }
.log-search     { color: #4488ff; }
.log-analyst    { color: #aa66ff; }
.log-writer     { color: #00ffcc; }
.log-quality    { color: #ff6688; }
.log-done       { color: #44ff88; }
.log-system     { color: #445566; }
</style>
""", unsafe_allow_html=True)
 
# ── Header ──────────────────────────────────────────────────────
st.markdown("## 🔬 Multi-Agent Research System")
st.caption("Powered by LangGraph · Groq · Tavily · Parallel AI Agents")
st.markdown("[View on GitHub](https://github.com/shank343/agent_project_1)")
 
# ── Tabs ────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["ABOUT", "RESEARCH"])
 
 
# ════════════════════════════════════════════════════════════════
# TAB 1 — ABOUT
# ════════════════════════════════════════════════════════════════
with tab1:
 
    # ── Author card ─────────────────────────────────────────────
    st.markdown("""
    <div style="display:flex; align-items:center; gap:1.5rem; padding:1.25rem 1.5rem;
                background:#f8f9ff; border:1px solid #e0e0f0; border-radius:10px;
                margin-bottom:2rem;">
        <div style="width:48px; height:48px; border-radius:50%; background:#e8f4ff;
                    border:2px solid #4488ff; display:flex; align-items:center;
                    justify-content:center; font-size:1.3rem; flex-shrink:0;">👤</div>
        <div>
            <div style="font-size:1.05rem; font-weight:700; color:#111133;">Shashank M</div>
            <div style="font-size:0.78rem; color:#4488ff; letter-spacing:0.08em;
                        font-family:monospace; margin-top:0.2rem;">
                DATA SCIENTIST · ROLLS-ROYCE
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    # ── Heading ─────────────────────────────────────────────────
    st.markdown("### Multi-Agentic System")
    st.markdown("---")
 
    # ── Project description ──────────────────────────────────────
    st.markdown("""
    This project implements a fully autonomous, multi-agent research pipeline built on
    **LangGraph** — a framework for orchestrating stateful, graph-based AI workflows.
    Given any research topic, the system independently plans, searches, analyses, writes,
    and self-reviews a structured report with no human intervention required beyond the
    initial prompt.
 
    The system is composed of five specialised agents, each with a distinct role:
    """)
 
    col1, col2 = st.columns(2)
 
    with col1:
        st.markdown("""
        **🟢 Supervisor**
        Receives the user's topic and dynamically determines the research scope —
        generating between 3 and 5 targeted search queries depending on the complexity
        of the subject matter.
 
        ---
 
        **🔵 Search Agents (Parallel)**
        Multiple search agents are spawned simultaneously using LangGraph's Send API,
        each executing an independent Tavily web search query. Results are collected in
        a shared state blackboard, giving the system broad, real-time coverage of the topic.
 
        ---
 
        **🟣 Analyst**
        Synthesises all gathered findings into a coherent analysis — identifying key themes,
        surfacing contradictions, and distilling the most actionable insights across all
        search results.
        """)
 
    with col2:
        st.markdown("""
        **🟡 Report Writer**
        Transforms the analysis into a structured, professional report comprising an
        executive summary, key findings, in-depth analysis, and specific recommendations.
        On revision cycles, the writer explicitly incorporates feedback from the quality
        checker.
 
        ---
 
        **🔴 Quality Checker**
        Independently scores the report on completeness, clarity, and actionability on
        a 0-1 scale. Reports scoring below 0.7 are returned to the writer with specific
        feedback for revision. The system allows up to two rewrites before finalising
        the output.
        """)
 
    st.markdown("""
    ---
    The entire pipeline runs on **Groq's inference API** (llama-3.1-8b-instant &
    llama-3.3-70b-versatile) and **Tavily** for live web search — making it fast,
    capable, and fully free to run.
    """)
 
    # ── Process Flow ────────────────────────────────────────────
    st.markdown("### Process Flow")
 
    st.image("research_graph.png", use_container_width=True)
 
 
# ════════════════════════════════════════════════════════════════
# TAB 2 — RESEARCH
# ════════════════════════════════════════════════════════════════
with tab2:
 
    st.markdown("#### Start a Research Run")
 
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
 
    st.markdown("---")
 
    # ── Terminal log ─────────────────────────────────────────
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
        add_log("[SEARCH]      Dispatching parallel agents...")
        add_log("              Number of agents decided by supervisor (3-5)...")
 
        try:
            research_system = get_research_system()
            with st.spinner("Agents are working... this may take a minute or two."):
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
 
            add_log(f"[SUPERVISOR]  Queries: {result['search_queries']}")
            add_log(f"[SEARCH]      Total findings collected: {len(result['findings'])}")
            add_log("[ANALYST]     Synthesising findings...")
 
            draft_count = 0
            for msg in result['messages']:
                if hasattr(msg, 'content'):
                    content = msg.content
                    if '[REPORT WRITER]' in content:
                        draft_count += 1
                        add_log(f"[WRITER]      Draft {draft_count} complete")
                    elif '[QUALITY CHECK]' in content:
                        add_log(f"[QUALITY]     {content[16:]}")
 
            add_log("")
            add_log(f"[DONE]        Final Score: {result['quality_score']:.2f}  |  "
                    f"Total Iterations: {result['iteration']}")
            add_log("✓ Pipeline complete.")
 
            # ── Report metadata ───────────────────────────
            report_placeholder.markdown(f"""
            **Quality Score:** `{result['quality_score']:.2f}` &nbsp;|&nbsp;
            **Iterations:** `{result['iteration']}` &nbsp;|&nbsp;
            **Topic:** {topic[:60]}
            """)
 
            st.markdown("---")
            st.markdown(result["report"])
 
        except Exception as e:
            if "429" in str(e) or "rate_limit" in str(e):
                add_log("✗ Rate limit hit — too many tokens at once.")
                add_log("  Try a more specific topic and run again.")
            else:
                add_log(f"✗ Error: {str(e)}")