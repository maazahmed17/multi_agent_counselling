"""
Flask Backend for CompanionAI Multi-Agent System
Integrates with existing frontend
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
from pathlib import Path
import os
from datetime import datetime
import uuid

# Add demo directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import multi-agent system
from demo.core.llm_client import LLMClient
from demo.agents.router_agent import RouterAgent
from demo.agents.anxiety_specialist import AnxietySpecialistAgent
from demo.agents.judge_agent import JudgeAgent

# Initialize Flask
app = Flask(__name__, static_folder='frontend/dist', static_url_path='')
CORS(app)

# Initialize multi-agent system
print("🚀 Initializing CompanionAI Multi-Agent System...")
llm_client = LLMClient()
router = RouterAgent(llm_client)
anxiety_specialist = AnxietySpecialistAgent(llm_client)
judge = JudgeAgent(llm_client)
print("✅ Multi-Agent System Ready!\n")

# Replit Database integration
try:
    from replit import db
    HAS_DB = True
    print("✅ Replit Database connected")
except ImportError:
    HAS_DB = False
    print("⚠️  Running without Replit DB")
    db = {}

# In-memory session storage
sessions = {}


@app.route('/')
def index():
    """Serve React frontend"""
    return send_from_directory('frontend/dist', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('frontend/dist', path)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "system": "CompanionAI Multi-Agent",
        "models": {
            "instruct": llm_client.llama_instruct,
            "guard": llm_client.llama_guard
        }
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint - processes user input through multi-agent pipeline

    Request body:
    {
        "message": "user message",
        "session_id": "optional session id"
    }

    Response:
    {
        "response": "bot response",
        "session_id": "session id",
        "workflow": {...},
        "approved": true/false
    }
    """
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id') or str(uuid.uuid4())

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        print(f"\n{'='*60}")
        print(f"📝 Processing: {user_message[:50]}...")
        print(f"{'='*60}\n")

        # STEP 1: Pre-Safety Gate
        print("🛡️  Step 1: Pre-Safety Check")
        pre_safety = llm_client.check_safety(user_message)

        if not pre_safety["is_safe"]:
            print(f"   ⚠️  UNSAFE INPUT: {pre_safety['category']}")
            crisis_response = _generate_crisis_response(pre_safety)

            # Store in DB
            _store_chat(
                session_id, user_message, crisis_response, {
                    "approved": False,
                    "reason": "safety_blocked",
                    "category": pre_safety['category']
                })

            return jsonify({
                "response": crisis_response,
                "session_id": session_id,
                "approved": False,
                "workflow": {
                    "safety_status": "blocked",
                    "category": pre_safety['category']
                }
            })

        print(f"   ✅ Input is safe")

        # STEP 2: Router
        print("\n🔀 Step 2: Intelligent Routing")
        routing = router.process(user_message)
        specialist_type = routing["specialist"]
        print(f"   → Routed to: {specialist_type.upper()}")

        # STEP 3: Specialist Response
        print(f"\n🧠 Step 3: {specialist_type.title()} Specialist")

        if specialist_type == "anxiety":
            specialist_result = anxiety_specialist.process(user_message)
            bot_response = specialist_result["response"]
        elif specialist_type == "crisis":
            bot_response = _handle_crisis(user_message, llm_client)
        else:
            bot_response = _handle_general(user_message, llm_client)

        print(f"   → Generated response ({len(bot_response)} chars)")

        # STEP 4: Judge Evaluation
        print("\n⚖️  Step 4: Quality Evaluation")
        evaluation = judge.process(user_message, bot_response)
        judge_score = evaluation["scores"]["overall"]
        approved = evaluation["approved"]

        print(f"   → Score: {judge_score}/10")
        print(f"   → Decision: {'APPROVED' if approved else 'NEEDS REVISION'}")

        # STEP 5: Post-Safety Gate
        print("\n🛡️  Step 5: Post-Safety Check")
        post_safety = llm_client.check_safety(bot_response)

        if not post_safety["is_safe"]:
            print(f"   ⚠️  UNSAFE RESPONSE: {post_safety['category']}")
            bot_response = "I apologize, but I need to rephrase my response to ensure it's safe. Please ask again."
            approved = False
        else:
            print(f"   ✅ Response is safe")

        # Final decision
        print(f"\n{'='*60}")
        print(
            f"{'✅ APPROVED - Delivering to user' if approved else '⚠️  NEEDS REVISION'}"
        )
        print(f"{'='*60}\n")

        # Store in database
        workflow_data = {
            "routing": specialist_type,
            "judge_score": judge_score,
            "approved": approved,
            "safety_passed": pre_safety["is_safe"] and post_safety["is_safe"]
        }

        _store_chat(session_id, user_message, bot_response, workflow_data)

        return jsonify({
            "response": bot_response,
            "session_id": session_id,
            "approved": approved,
            "workflow": workflow_data
        })

    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/api/history/<session_id>', methods=['GET'])
def get_history(session_id):
    """Get chat history for a session"""
    try:
        if HAS_DB:
            history = []
            for key in db.keys():
                if key.startswith(f"chat_{session_id}_"):
                    history.append(db[key])
            history.sort(key=lambda x: x.get("timestamp", ""))
        else:
            history = sessions.get(session_id, [])

        return jsonify({"history": history, "session_id": session_id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    try:
        if HAS_DB:
            total_chats = len([k for k in db.keys() if k.startswith("chat_")])
            unique_sessions = len(
                set(
                    k.split("_")[1] for k in db.keys()
                    if k.startswith("chat_")))
        else:
            total_chats = sum(len(v) for v in sessions.values())
            unique_sessions = len(sessions)

        return jsonify({
            "total_conversations": total_chats,
            "unique_sessions": unique_sessions,
            "status": "operational",
            "system": "CompanionAI Multi-Agent"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Helper functions
def _generate_crisis_response(safety_result):
    """Generate appropriate response for unsafe input"""
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
        return "I'm not able to provide support for this type of concern. Please consult with an appropriate professional or trusted resource."


def _handle_crisis(user_input, llm):
    """Handle crisis situations"""
    crisis_prompt = """You are a crisis counselor. The user is in distress. Respond with:
1. Immediate empathy and validation
2. Crisis resources (hotlines, emergency contacts)
3. Encouragement to seek immediate professional help
Keep response brief and focused on immediate safety."""

    return llm.generate_response(user_input,
                                 system_prompt=crisis_prompt,
                                 max_tokens=300,
                                 temperature=0.5)


def _handle_general(user_input, llm):
    """Handle general mental health queries"""
    general_prompt = """You are a supportive mental health assistant. Provide general guidance, validate feelings, and suggest appropriate next steps. Be warm and non-judgmental."""

    return llm.generate_response(user_input,
                                 system_prompt=general_prompt,
                                 max_tokens=400,
                                 temperature=0.7)


def _store_chat(session_id, user_msg, bot_msg, workflow):
    """Store chat in database"""
    chat_entry = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "user_message": user_msg,
        "bot_response": bot_msg,
        "workflow": workflow
    }

    if HAS_DB:
        db_key = f"chat_{session_id}_{datetime.now().timestamp()}"
        db[db_key] = chat_entry
    else:
        if session_id not in sessions:
            sessions[session_id] = []
        sessions[session_id].append(chat_entry)


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 Starting CompanionAI Server")
    print("=" * 60)
    print(f"Backend: http://0.0.0.0:3000")
    print(f"Frontend: http://0.0.0.0:5000")
    print("=" * 60 + "\n")

    app.run(host='0.0.0.0', port=3000, debug=True)
