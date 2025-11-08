# 🚀 CompanionAI Chatbot - Setup & Run Guide

## Project Overview
CompanionAI is a multi-agent mental health counselling chatbot with:
- **Router Agent**: Intelligently routes queries to appropriate specialists
- **Anxiety Specialist**: Handles anxiety-related concerns
- **Judge Agent**: Evaluates response quality
- **Safety Gates**: Pre and post-processing safety checks
- **Frontend UI**: Beautiful React/Vite dashboard

---

## 📋 Prerequisites

### Required Files
- `.env` - API keys and model configuration
- `requirements.txt` - Python dependencies
- `frontend/package.json` - Node.js dependencies

### Check if Already Installed
```bash
python --version  # Should be 3.9+
node --version    # Should be 16+
npm --version     # Should be 8+
```

---

## 🔧 Step 1: Environment Setup

### 1.1 Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 1.2 Verify `.env` File
Your `.env` file should contain:
```
GROQ_API_KEY=your_groq_api_key
LLAMA_INSTRUCT_MODEL=llama-3.3-70b-versatile
LLAMA_GUARD_MODEL=meta-llama/llama-guard-4-12b
CRISIS_THRESHOLD=0.85
SAFETY_SCORE_MIN=0.7
```

**Get API Key:**
- Sign up at https://console.groq.com
- Create an API key
- Add it to `.env` as `GROQ_API_KEY`

### 1.3 Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

---

## 🎯 Step 2: Run the Project

### Option A: Run Both Backend & Frontend (Recommended)

#### Terminal 1 - Start Backend (Port 3000)
```bash
python app.py
```

Expected output:
```
🚀 Initializing CompanionAI Multi-Agent System...
✅ Multi-Agent System Ready!
✅ Running on http://0.0.0.0:3000
```

#### Terminal 2 - Start Frontend (Port 5000)
```bash
cd frontend
npm run dev
```

Expected output:
```
VITE v4.x.x ready in xxx ms
➜ Local: http://localhost:5000
```

### Option B: Run Individually

**Backend Only:**
```bash
python app.py
# Then access API at http://localhost:3000/api/health
```

**Frontend Only:**
```bash
cd frontend && npm run dev
# Then navigate to http://localhost:5000
```

---

## 💬 Step 3: Interact with the Chatbot

### Via Web UI (Recommended)
1. Open browser to `http://localhost:5000`
2. Click one of the quick action cards:
   - 😊 "I feel anxious" - Get anxiety support
   - 🔒 "I'm doing okay" - General chat
   - ⚠️ "I need help now" - Crisis resources
3. Or type directly in the message input at the bottom

### Via API (Command Line)
```bash
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I am feeling anxious"}'
```

**Response includes:**
- `response` - Bot's reply
- `session_id` - Conversation ID
- `approved` - Quality check result
- `workflow` - System workflow details

---

## 🧪 Step 4: Test the System

### 4.1 Health Check Endpoint
```bash
curl http://localhost:3000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "system": "CompanionAI Multi-Agent",
  "models": {
    "instruct": "llama-3.3-70b-versatile",
    "guard": "meta-llama/llama-guard-4-12b"
  }
}
```

### 4.2 Test Chat Endpoint
```bash
# Test 1: General message
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'

# Test 2: Anxiety-related
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I am feeling anxious about my presentation tomorrow"}'

# Test 3: With session continuity
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me more", "session_id": "your-session-id"}'
```

### 4.3 Get Chat History
```bash
curl http://localhost:3000/api/history/your-session-id
```

### 4.4 Get System Stats
```bash
curl http://localhost:3000/api/stats
```

---

## 📂 Project Structure

```
multi_agent_counselling/
├── app.py                          # ⭐ Main backend (START HERE)
├── .env                            # API keys & config
├── requirements.txt                # Python dependencies
├── demo/
│   ├── core/
│   │   ├── llm_client.py          # LLM integration (Groq)
│   │   └── safety_check.py        # Safety gates
│   └── agents/
│       ├── router_agent.py        # Routes queries
│       ├── anxiety_specialist.py  # Anxiety support
│       └── judge_agent.py         # Quality evaluation
├── frontend/                       # React/Vite UI
│   ├── package.json               # ⭐ Run: npm run dev
│   ├── vite.config.js             # Vite config (proxy to port 3000)
│   └── src/
│       ├── SerenityDashboard.jsx  # Main chatbot UI
│       └── App.jsx
└── SETUP_AND_RUN.md               # This file!
```

---

## 🔌 API Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Health check |
| `/api/chat` | POST | Send message to chatbot |
| `/api/history/<session_id>` | GET | Get conversation history |
| `/api/stats` | GET | Get system statistics |
| `/` | GET | Serve React frontend |

---

## ⚠️ Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask_cors'"
```bash
pip install flask-cors
```

### Issue: "Cannot connect to backend"
- Check if backend is running: `curl http://localhost:3000/api/health`
- Verify port 3000 is free: `lsof -i :3000`
- Check `.env` file has GROQ_API_KEY

### Issue: "npm not found"
```bash
# Install Node.js from https://nodejs.org/
# Or via package manager:
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install nodejs
```

### Issue: Frontend shows "Unable to connect to server"
- Ensure backend is running on port 3000
- Check CORS is enabled in `app.py` (it is)
- Verify proxy in `frontend/vite.config.js` points to `http://localhost:3000`

---

## 🚀 Quick Start Commands

```bash
# 1. Install all dependencies
pip install -r requirements.txt
cd frontend && npm install && cd ..

# 2. Terminal 1 - Start Backend
python app.py

# 3. Terminal 2 - Start Frontend
cd frontend && npm run dev

# 4. Open browser
# Navigate to http://localhost:5000

# 5. Test API
curl http://localhost:3000/api/health
```

---

## 📊 Understanding the Workflow

When you send a message:

```
User Message
    ↓
[Safety Check] - Llama Guard checks for harmful content
    ↓
[Router Agent] - Determines if anxiety, crisis, or general
    ↓
[Specialist Agent] - Generates appropriate response
    ↓
[Judge Agent] - Evaluates response quality (0-10)
    ↓
[Post-Safety Check] - Ensures response is safe
    ↓
Response to User
```

---

## 📝 Example Interactions

### Test 1: Basic Greeting
```
User: "Hi there!"
Expected: Friendly greeting and offer to help
```

### Test 2: Anxiety Support
```
User: "I'm feeling anxious"
Expected: 
- Routed to anxiety specialist
- Empathetic response with coping strategies
- Quality score 8-10
- Approved: true
```

### Test 3: Session Continuity
```
Message 1: "I'm stressed"
Message 2: "Can you help me relax?" (uses same session_id)
Expected: System remembers context from first message
```

---

## 🔍 Monitoring

### View Backend Logs
```bash
tail -f backend.log
```

### View Frontend Build Output
```bash
cd frontend
npm run dev  # Shows real-time dev server logs
```

### Check System Stats
```bash
curl http://localhost:3000/api/stats
```

---

## 📞 Support

For issues:
1. Check `.env` file is properly configured
2. Ensure both backend and frontend are running
3. Verify API key is valid
4. Check browser console for frontend errors
5. Check terminal for backend errors

---

**Happy Chatting! 🤖💬**
