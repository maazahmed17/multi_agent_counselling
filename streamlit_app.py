"""
CompanionAI - Multi-Agent Counseling System
Simplified Streamlit Demo for Vibeathon
"""
import streamlit as st
import sys
from pathlib import Path
import os

# Add demo to path
sys.path.insert(0, str(Path(__file__).parent))

from demo.core.llm_client import LLMClient
from demo.agents.router_agent import RouterAgent
from demo.agents.anxiety_specialist import AnxietySpecialistAgent
from demo.agents.judge_agent import JudgeAgent

# Page config
st.set_page_config(page_title="CompanionAI - Multi-Agent Counseling",
                   page_icon="🧠",
                   layout="wide")


# Initialize agents
@st.cache_resource
def init_system():
    llm = LLMClient()
    router = RouterAgent(llm)
    anxiety = AnxietySpecialistAgent(llm)
    judge = JudgeAgent(llm)
    return llm, router, anxiety, judge


llm, router, anxiety, judge = init_system()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'workflows' not in st.session_state:
    st.session_state.workflows = []

# Header
st.title("🧠 CompanionAI")
st.subheader("Multi-Agent Mental Health Support System")

# Sidebar
with st.sidebar:
    st.header("🎯 System Architecture")
    st.info("""
    **Pipeline:**
    1. 🛡️ Pre-Safety Gate
    2. 🔀 Router Agent
    3. 🧠 Specialist Agent
    4. ⚖️ Judge Agent
    5. ✅ Final Output
    """)

    st.divider()

    st.header("📊 Configuration")
    st.code(f"""
Model: Llama 3.3 70B
Safety: Llama Guard 4
Method: CBT-based
    """)

    if st.button("🔄 Reset Chat"):
        st.session_state.messages = []
        st.session_state.workflows = []
        st.rerun()

# Display chat
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

        # Show workflow for bot messages
        if msg["role"] == "assistant" and i < len(st.session_state.workflows):
            workflow = st.session_state.workflows[i]
            with st.expander("🔍 View Multi-Agent Workflow"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Safety", "✅ Safe")
                with col2:
                    st.metric("Quality",
                              f"{workflow.get('judge_score', 0)}/10")
                with col3:
                    st.metric("Route", workflow.get('specialist', 'N/A'))

# Chat input
if prompt := st.chat_input("Share what's on your mind..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Process through agents
    with st.chat_message("assistant"):
        with st.spinner("🤖 Processing through multi-agent system..."):
            # Step 1: Safety check
            safety = llm.check_safety(prompt)

            if not safety["is_safe"]:
                response = f"⚠️ I'm concerned about your safety. Please contact:\n- India: AASRA 91-22-27546669\n- Emergency: 112"
                st.write(response)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })
                st.stop()

            # Step 2: Route
            routing = router.process(prompt)
            specialist_type = routing["specialist"]

            # Step 3: Specialist response
            if specialist_type == "anxiety":
                specialist_result = anxiety.process(prompt)
                response = specialist_result["response"]
            else:
                # Fallback
                response = llm.generate_response(
                    prompt,
                    system_prompt=
                    "You are a supportive mental health assistant.",
                    max_tokens=400)

            # Step 4: Judge
            evaluation = judge.process(prompt, response)
            judge_score = evaluation["scores"]["overall"]

            # Display
            st.write(response)

            # Store
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
            st.session_state.workflows.append({
                "specialist":
                specialist_type,
                "judge_score":
                judge_score,
                "approved":
                evaluation["approved"]
            })

    st.rerun()

# Info
if len(st.session_state.messages) == 0:
    st.info("""
    👋 **Welcome to CompanionAI!**

    Try: "I'm feeling anxious about my exam tomorrow"

    **Multi-Agent System:**
    - Safety gates check every message
    - Router sends you to specialized agents
    - Judge evaluates response quality
    """)

st.divider()
st.caption("🏆 Vibeathon 2025 | Multi-Agent Counseling AI")
