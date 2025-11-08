"""
🤖 CompanionAI - Multi-Agent Counseling System
Enhanced Streamlit Demo with Chat Memory & Conversation Context
"""
import streamlit as st
import sys
from pathlib import Path
import os
from datetime import datetime
import uuid

# Add demo to path
sys.path.insert(0, str(Path(__file__).parent))

from demo.core.llm_client import LLMClient
from demo.agents.router_agent import RouterAgent
from demo.agents.anxiety_specialist import AnxietySpecialistAgent
from demo.agents.judge_agent import JudgeAgent

# Page config
st.set_page_config(
    page_title="CompanionAI - Mental Health Support",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .stChatMessage {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .conversation-stats {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize agents
@st.cache_resource
def init_system():
    """Initialize the multi-agent system (cached to avoid reloading)"""
    llm = LLMClient()
    router = RouterAgent(llm)
    anxiety = AnxietySpecialistAgent(llm)
    judge = JudgeAgent(llm)
    return llm, router, anxiety, judge

# Initialize session state
def init_session_state():
    """Initialize all session state variables with proper structure"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'conversation_history' not in st.session_state:
        # Full conversation context for AI (includes role + content)
        st.session_state.conversation_history = []
    
    if 'workflows' not in st.session_state:
        st.session_state.workflows = []
    
    if 'conversation_summary' not in st.session_state:
        st.session_state.conversation_summary = ""
    
    if 'user_profile' not in st.session_state:
        # Track user patterns for better personalization
        st.session_state.user_profile = {
            "main_concerns": [],
            "interaction_count": 0,
            "first_interaction": datetime.now().isoformat()
        }

def get_conversation_context(limit=5):
    """
    Get recent conversation context for context-aware responses
    Args:
        limit: Number of recent message pairs to include
    Returns:
        Formatted string with conversation history
    """
    if not st.session_state.conversation_history:
        return ""
    
    recent_messages = st.session_state.conversation_history[-limit*2:]
    context = "Previous conversation:\n"
    for msg in recent_messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        context += f"{role}: {msg['content']}\n"
    return context

def process_with_context(user_input, llm, router, anxiety, judge):
    """
    Process user input through multi-agent pipeline WITH conversation context
    """
    # Get conversation context
    context = get_conversation_context(limit=3)
    
    # STEP 1: Pre-Safety Gate
    safety = llm.check_safety(user_input)
    
    if not safety["is_safe"]:
        crisis_response = generate_crisis_response(safety)
        return {
            "response": crisis_response,
            "workflow": {
                "safety_status": "blocked",
                "category": safety['category'],
                "specialist": "crisis",
                "judge_score": 0,
                "approved": False
            }
        }
    
    # STEP 2: Router (with context)
    routing_input = f"{context}\n\nCurrent message: {user_input}" if context else user_input
    routing = router.process(routing_input)
    specialist_type = routing["specialist"]
    
    # STEP 3: Specialist Response (with context)
    if specialist_type == "anxiety":
        # Add context to anxiety specialist
        contextual_input = f"{context}\n\nCurrent concern: {user_input}" if context else user_input
        specialist_result = anxiety.process(contextual_input)
        response = specialist_result["response"]
    else:
        # Fallback with context
        system_prompt = f"""You are a supportive mental health assistant. 
        
{context if context else 'This is the start of the conversation.'}

Provide contextually aware support that references previous conversation when relevant."""
        response = llm.generate_response(
            user_input,
            system_prompt=system_prompt,
            max_tokens=400,
            temperature=0.7
        )
    
    # STEP 4: Judge Evaluation
    evaluation = judge.process(user_input, response)
    judge_score = evaluation["scores"]["overall"]
    
    # STEP 5: Post-Safety Check
    post_safety = llm.check_safety(response)
    approved = evaluation["approved"] and post_safety["is_safe"]
    
    if not post_safety["is_safe"]:
        response = "I apologize, but I need to rephrase that. Could you help me understand your concern differently?"
        approved = False
    
    return {
        "response": response,
        "workflow": {
            "specialist": specialist_type,
            "judge_score": judge_score,
            "approved": approved,
            "safety_passed": post_safety["is_safe"]
        }
    }

def generate_crisis_response(safety_result):
    """Generate appropriate crisis response"""
    category = safety_result.get("category", "unknown")
    
    if category == "S11":  # Self-harm
        return """I'm really concerned about what you've shared. Your safety is the most important thing right now.

**Please reach out to crisis support immediately:**
- 🇮🇳 India: AASRA - 91-22-27546669
- 🇺🇸 USA: 988 (Suicide & Crisis Lifeline)
- 🌍 International: https://findahelpline.com

**You can also:**
- Call emergency services: 112 (India)
- Go to the nearest emergency room
- Tell someone you trust right now

You don't have to face this alone. Professional help is available 24/7."""
    else:
        return "I'm not able to provide support for this type of concern. Please consult with an appropriate professional."

def update_user_profile(user_input, specialist_type):
    """Track user patterns for better understanding"""
    st.session_state.user_profile["interaction_count"] += 1
    
    if specialist_type not in st.session_state.user_profile["main_concerns"]:
        st.session_state.user_profile["main_concerns"].append(specialist_type)

# Initialize system
try:
    llm, router, anxiety, judge = init_system()
    system_ready = True
except Exception as e:
    system_ready = False
    st.error(f"❌ Error initializing system: {e}")

init_session_state()

# Header
st.markdown('<h1 class="main-header">🧠 CompanionAI</h1>', unsafe_allow_html=True)
st.markdown("**Your Multi-Agent Mental Health Support System**")

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 System Architecture")
    st.info("""
    **Multi-Agent Pipeline:**
    1. 🛡️ Pre-Safety Gate
    2. 🔀 Smart Router
    3. 🧠 Specialist Agent
    4. ⚖️ Quality Judge
    5. ✅ Final Response
    
    **✨ New: Conversation Memory**
    - Context-aware responses
    - Remembers previous messages
    - Personalized support
    """)
    
    st.divider()
    
    st.markdown("### 📊 Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Messages", len(st.session_state.messages))
    with col2:
        st.metric("Exchanges", len(st.session_state.messages) // 2)
    
    if st.session_state.user_profile["main_concerns"]:
        st.markdown("**Topics Discussed:**")
        for concern in st.session_state.user_profile["main_concerns"]:
            st.markdown(f"- {concern.title()}")
    
    st.divider()
    
    st.markdown("### ⚙️ Configuration")
    st.code("""
Model: Llama 3.3 70B
Safety: Llama Guard 4
Memory: Last 3 exchanges
Method: CBT-based
    """)
    
    st.divider()
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 New Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_history = []
            st.session_state.workflows = []
            st.session_state.conversation_summary = ""
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()
    
    with col2:
        if st.button("📥 Export", use_container_width=True):
            # Export conversation
            export_data = {
                "session_id": st.session_state.session_id,
                "timestamp": datetime.now().isoformat(),
                "messages": st.session_state.messages,
                "workflows": st.session_state.workflows
            }
            st.download_button(
                label="💾 Download JSON",
                data=str(export_data),
                file_name=f"conversation_{st.session_state.session_id[:8]}.json",
                mime="application/json",
                use_container_width=True
            )

# Main chat area
if not system_ready:
    st.error("System not ready. Please check the logs.")
    st.stop()

# Display welcome message for new chats
if len(st.session_state.messages) == 0:
    with st.container():
        st.markdown("""
        <div class="conversation-stats">
            <h3>👋 Welcome to CompanionAI!</h3>
            <p>I'm here to provide mental health support through our advanced multi-agent system.</p>
            <p><strong>✨ New: I now remember our conversation!</strong> Feel free to refer back to things we've discussed.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Try these:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("😰 I'm feeling anxious...", use_container_width=True):
                st.session_state.quick_prompt = "I'm feeling very anxious about my upcoming exam"
                st.rerun()
        
        with col2:
            if st.button("😔 Feeling down today", use_container_width=True):
                st.session_state.quick_prompt = "I've been feeling really down lately"
                st.rerun()
        
        with col3:
            if st.button("😓 Stressed about work", use_container_width=True):
                st.session_state.quick_prompt = "I'm overwhelmed with work stress"
                st.rerun()

# Display chat history
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # Show workflow details for assistant messages
        if msg["role"] == "assistant" and i < len(st.session_state.workflows):
            workflow = st.session_state.workflows[i]
            with st.expander("🔍 View Multi-Agent Workflow"):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Safety", "✅ Safe" if workflow.get('safety_passed', True) else "⚠️ Blocked")
                with col2:
                    st.metric("Specialist", workflow.get('specialist', 'N/A').title())
                with col3:
                    st.metric("Quality", f"{workflow.get('judge_score', 0)}/10")
                with col4:
                    status = "✅" if workflow.get('approved', False) else "⚠️"
                    st.metric("Status", status)

# Handle quick prompts
if 'quick_prompt' in st.session_state:
    prompt = st.session_state.quick_prompt
    del st.session_state.quick_prompt
else:
    prompt = st.chat_input("Share what's on your mind...")

# Process user input
if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.conversation_history.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process through agents with context
    with st.chat_message("assistant"):
        with st.spinner("🤖 Processing through multi-agent system..."):
            result = process_with_context(prompt, llm, router, anxiety, judge)
            response = result["response"]
            workflow = result["workflow"]
            
            # Display response
            st.markdown(response)
            
            # Store in session
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.conversation_history.append({"role": "assistant", "content": response})
            st.session_state.workflows.append(workflow)
            
            # Update user profile
            update_user_profile(prompt, workflow["specialist"])
            
            # Show workflow
            with st.expander("🔍 View Multi-Agent Workflow", expanded=False):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Safety", "✅ Safe" if workflow.get('safety_passed', True) else "⚠️ Blocked")
                with col2:
                    st.metric("Specialist", workflow.get('specialist', 'N/A').title())
                with col3:
                    st.metric("Quality", f"{workflow.get('judge_score', 0)}/10")
                with col4:
                    status = "✅" if workflow.get('approved', False) else "⚠️"
                    st.metric("Status", status)
    
    st.rerun()

# Footer
st.divider()
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    st.markdown("*🧠 CompanionAI - Multi-Agent System*")

# Debug info (collapsible)
with st.expander("🔧 Developer Info"):
    st.json({
        "session_id": st.session_state.session_id,
        "total_messages": len(st.session_state.messages),
        "conversation_turns": len(st.session_state.messages) // 2,
        "profile": st.session_state.user_profile
    })
