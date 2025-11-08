# 📖 CompanionAI - Documentation Index

## 🎯 Quick Navigation

Start here to understand how to run and test your chatbot project!

---

## 📚 Documentation Files

### 1. **SETUP_AND_RUN.md** ⭐ START HERE
Complete guide for setting up and running the entire project.

**What it covers:**
- Prerequisites and environment setup
- Step-by-step instructions to run backend and frontend
- API endpoint reference
- Troubleshooting common issues
- Understanding the workflow
- Example interactions

**When to use:** First time setup, deployment, or reference

---

### 2. **TESTING_GUIDE.md** 🧪
Comprehensive testing guide with 10 test scenarios.

**What it covers:**
- Files to test and their purposes
- 10 detailed test scenarios (health check, anxiety detection, crisis detection, etc.)
- Manual testing checklist
- Performance tests
- Debugging tips
- Sign-off checklist

**When to use:** Before launching, QA testing, debugging issues

---

### 3. **QUICK_START.sh** 🚀
Bash script to quickly check system and guide you through startup.

**What it does:**
- Checks Python and Node.js installation
- Installs all dependencies
- Verifies .env configuration
- Displays startup instructions

**How to use:**
```bash
bash QUICK_START.sh
```

---

## 🚀 30-Second Quick Start

```bash
# Terminal 1: Start Backend
python app.py

# Terminal 2: Start Frontend  
cd frontend && npm run dev

# Then open browser: http://localhost:5000
```

---

## 📂 Project Structure Overview

```
multi_agent_counselling/
├── app.py                    ← Main backend file (run this first!)
├── .env                      ← Your API keys
├── requirements.txt          ← Python dependencies
├── SETUP_AND_RUN.md          ← Full setup guide
├── TESTING_GUIDE.md          ← How to test everything
├── QUICK_START.sh            ← Quick setup checker
├── demo/
│   ├── core/
│   │   ├── llm_client.py     ← Groq API integration
│   │   └── safety_check.py   ← Safety gates
│   └── agents/
│       ├── router_agent.py   ← Routes messages
│       ├── anxiety_specialist.py
│       └── judge_agent.py    ← Quality evaluator
└── frontend/
    ├── src/SerenityDashboard.jsx  ← Main UI
    └── vite.config.js             ← Frontend config
```

---

## 🎯 What Each File Does

### Backend (`app.py`)
- Main Flask application
- Handles API requests
- Manages multi-agent pipeline
- Runs on **port 3000**

### Frontend (`frontend/src/SerenityDashboard.jsx`)
- Beautiful React UI
- 3 quick-action cards
- Chat interface
- Displays workflow info
- Runs on **port 5000**

### Core Agents (`demo/agents/`)
- **Router Agent**: Routes to anxiety specialist or general support
- **Anxiety Specialist**: Provides anxiety-specific support
- **Judge Agent**: Evaluates response quality (0-10 score)

### LLM Integration (`demo/core/llm_client.py`)
- Uses Groq API for fast LLM access
- Handles safety checking via Llama Guard
- Manages model initialization

---

## ✅ Getting Started Checklist

- [ ] Clone/download the project
- [ ] Have API key ready (from https://console.groq.com)
- [ ] Update `.env` file with your API key
- [ ] Read **SETUP_AND_RUN.md**
- [ ] Run backend: `python app.py`
- [ ] Run frontend: `cd frontend && npm run dev`
- [ ] Open browser to `http://localhost:5000`
- [ ] Test by clicking a card or typing a message
- [ ] Use **TESTING_GUIDE.md** for detailed testing

---

## 🔌 Main API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | System health check |
| `/api/chat` | POST | Send message & get response |
| `/api/history/<id>` | GET | Get chat history |
| `/api/stats` | GET | System statistics |

---

## 💬 What Your Chatbot Does

1. **Receives Message** from user
2. **Safety Check** - Uses Llama Guard to detect harmful content
3. **Intelligent Routing** - Determines if anxiety, crisis, or general
4. **Specialist Response** - Routes to appropriate specialist
5. **Quality Judgment** - Judge agent scores 0-10
6. **Post-Safety Check** - Ensures response is safe
7. **Sends Response** to user with metadata

---

## 🧪 Quick Test

After starting both services, test with:

```bash
# Test 1: Health check
curl http://localhost:3000/api/health

# Test 2: Send a message
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, I am feeling anxious"}'
```

---

## ⚠️ Common Issues

### Issue: "Connection refused" or "Cannot connect to backend"
**Solution:** Make sure backend is running in Terminal 1:
```bash
python app.py
```

### Issue: "ModuleNotFoundError: flask_cors"
**Solution:** Install missing dependency:
```bash
pip install flask-cors
```

### Issue: "npm command not found"
**Solution:** Install Node.js from https://nodejs.org/

### Issue: "GROQ_API_KEY not set"
**Solution:** Add your API key to `.env`:
```
GROQ_API_KEY=your_key_here
```

---

## 📊 Testing Priority

1. **Priority 1** (Must Work):
   - Backend starts without errors
   - Frontend loads on port 5000
   - Health endpoint responds
   - Chat endpoint works

2. **Priority 2** (Should Work):
   - Cards trigger appropriate routing
   - Anxiety detection works
   - Responses are appropriate
   - Judge scores are reasonable

3. **Priority 3** (Nice to Have):
   - Session continuity
   - History retrieval
   - Performance optimization

---

## 📞 Documentation Guide

| Document | Read When | Time |
|----------|-----------|------|
| **SETUP_AND_RUN.md** | First time setup | 15 min |
| **TESTING_GUIDE.md** | Before launch, during QA | 20 min |
| **QUICK_START.sh** | Want quick dependency check | 2 min |

---

## 🚀 Next Steps

1. **Read**: `SETUP_AND_RUN.md` (full guide)
2. **Setup**: Follow the environment setup steps
3. **Run**: Start backend and frontend
4. **Test**: Use `TESTING_GUIDE.md` for comprehensive testing
5. **Deploy**: Once all tests pass, you're ready!

---

## 💡 Tips

- Keep 2 terminals open: one for backend, one for frontend
- Backend takes ~5-10 seconds to initialize models
- Frontend auto-refreshes during development
- Check browser console (F12) for frontend errors
- Check terminal output for backend logs
- Use `curl` commands to test API directly

---

**Status:** ✅ System is ready to use!

For detailed information, see the appropriate documentation file above.

---

*Last Updated: 2025-11-08*
