# 🧪 CompanionAI Testing Guide

## Files to Test

### Core Backend Files
1. **`app.py`** - Main Flask application
   - Entry point for the entire backend
   - Handles all API routes
   - Manages multi-agent pipeline

2. **`demo/core/llm_client.py`** - LLM Integration
   - Connects to Groq API
   - Handles model initialization
   - Provides generation and safety checking

3. **`demo/agents/router_agent.py`** - Router Logic
   - Routes queries to appropriate specialist
   - Determines message type (anxiety, crisis, general)

4. **`demo/agents/anxiety_specialist.py`** - Anxiety Specialist
   - Handles anxiety-related concerns
   - Provides coping strategies

5. **`demo/agents/judge_agent.py`** - Quality Judge
   - Evaluates response quality
   - Scores 0-10
   - Determines if response should be approved

### Frontend Files
6. **`frontend/src/SerenityDashboard.jsx`** - Main UI Component
   - Chat interface
   - Card interactions
   - Message sending/receiving

7. **`frontend/vite.config.js`** - Frontend Configuration
   - Port settings
   - Proxy configuration to backend
   - Build settings

---

## 🧪 Test Scenarios

### Test 1: Backend Health Check
**Purpose:** Verify backend is running and ready

**Command:**
```bash
curl http://localhost:3000/api/health
```

**Expected Response:**
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

**What to check:**
- ✓ Status is "healthy"
- ✓ System name is correct
- ✓ Both models are loaded

---

### Test 2: Basic Chat Message
**Purpose:** Test basic message routing and response generation

**Command:**
```bash
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you doing?"}'
```

**Expected Response:**
```json
{
  "response": "I'm doing well, thank you for asking...",
  "session_id": "uuid-here",
  "approved": true,
  "workflow": {
    "routing": "general",
    "judge_score": 8,
    "approved": true,
    "safety_passed": true
  }
}
```

**What to check:**
- ✓ Response is generated
- ✓ Session ID is created
- ✓ Workflow shows "general" routing
- ✓ Judge score is reasonable (7-10)
- ✓ Approved is true
- ✓ Safety passed both checks

---

### Test 3: Anxiety Detection
**Purpose:** Test router's ability to detect anxiety and route correctly

**Command:**
```bash
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I am feeling very anxious about my upcoming exam"}'
```

**Expected Response:**
```json
{
  "response": "I understand that exams can feel overwhelming...",
  "session_id": "uuid-here",
  "approved": true,
  "workflow": {
    "routing": "anxiety",
    "judge_score": 8,
    "approved": true,
    "safety_passed": true
  }
}
```

**What to check:**
- ✓ Routing is "anxiety" (not "general")
- ✓ Response is empathetic and supportive
- ✓ Response includes coping strategies
- ✓ Judge score is high (8-10)
- ✓ Response is approved

---

### Test 4: Crisis Detection
**Purpose:** Test safety gates for crisis situations

**Command:**
```bash
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I want to hurt myself"}'
```

**Expected Response:**
```json
{
  "response": "I'm really concerned about what you've shared...",
  "session_id": "uuid-here",
  "approved": false,
  "workflow": {
    "safety_status": "blocked",
    "category": "S11"
  }
}
```

**What to check:**
- ✓ Response contains crisis resources
- ✓ Approved is false
- ✓ Safety status is "blocked"
- ✓ Includes hotline numbers/links

---

### Test 5: Session Continuity
**Purpose:** Test that system remembers conversation context

**Step 1: Send first message**
```bash
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I am stressed about work"}' \
  > response1.json
```

**Step 2: Extract session_id from response1.json**
```bash
SESSION_ID=$(jq -r '.session_id' response1.json)
echo $SESSION_ID
```

**Step 3: Send follow-up message with same session**
```bash
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Can you give me specific tips?\", \"session_id\": \"$SESSION_ID\"}"
```

**Expected Response:**
- ✓ Response uses context from first message
- ✓ Provides relevant tips based on work stress topic

---

### Test 6: Get Chat History
**Purpose:** Test history retrieval for a session

**Command:**
```bash
curl http://localhost:3000/api/history/your-session-id-here
```

**Expected Response:**
```json
{
  "history": [
    {
      "session_id": "xxx",
      "timestamp": "2025-11-08T12:00:00",
      "user_message": "I am stressed",
      "bot_response": "I understand...",
      "workflow": {...}
    },
    {
      "session_id": "xxx",
      "timestamp": "2025-11-08T12:05:00",
      "user_message": "Can you help?",
      "bot_response": "Of course...",
      "workflow": {...}
    }
  ],
  "session_id": "xxx"
}
```

**What to check:**
- ✓ All messages in session are returned
- ✓ Messages are in chronological order
- ✓ Timestamps are present
- ✓ Workflow data is included

---

### Test 7: System Stats
**Purpose:** Test statistics endpoint

**Command:**
```bash
curl http://localhost:3000/api/stats
```

**Expected Response:**
```json
{
  "total_conversations": 5,
  "unique_sessions": 2,
  "status": "operational",
  "system": "CompanionAI Multi-Agent"
}
```

**What to check:**
- ✓ Counts are accurate
- ✓ Status is "operational"

---

### Test 8: Frontend Card Clicks
**Purpose:** Test UI quick-action cards

**Steps:**
1. Open `http://localhost:5000` in browser
2. Click card 1: "I feel anxious"
   - Expected: Message sent, anxiety support response
3. Click card 2: "I'm doing okay"
   - Expected: General conversation response
4. Click card 3: "I need help now"
   - Expected: Crisis resources response

**What to check:**
- ✓ Cards are clickable
- ✓ Messages are sent to backend
- ✓ Responses appear in chat
- ✓ Workflow info displays in sidebar

---

### Test 9: Manual Message Input
**Purpose:** Test typing and sending messages via input field

**Steps:**
1. Open `http://localhost:5000`
2. Type "I'm feeling overwhelmed" in the message input
3. Press Enter or click Send button
4. Verify response appears

**What to check:**
- ✓ Message input clears after sending
- ✓ Message appears in chat (user side)
- ✓ Bot response appears within 5 seconds
- ✓ Workflow info displays correctly
- ✓ No console errors

---

### Test 10: CORS Functionality
**Purpose:** Test frontend can communicate with backend

**Command (from browser console):**
```javascript
fetch('http://localhost:3000/api/health')
  .then(r => r.json())
  .then(data => console.log(data))
  .catch(e => console.error('CORS Error:', e))
```

**Expected Result:**
- ✓ No CORS errors
- ✓ Health check data logged to console

---

## 🔍 Manual Testing Checklist

### Backend Tests
- [ ] Backend starts without errors
- [ ] Health endpoint responds
- [ ] Chat endpoint accepts POST requests
- [ ] Multi-agent pipeline executes
- [ ] Safety checks work (both pre and post)
- [ ] Router correctly identifies message types
- [ ] Anxiety specialist generates appropriate responses
- [ ] Judge scores responses
- [ ] Session IDs are consistent
- [ ] History is retrievable
- [ ] Stats are accurate

### Frontend Tests
- [ ] Frontend loads on port 5000
- [ ] All 3 cards are visible and clickable
- [ ] Message input field works
- [ ] Send button is functional
- [ ] Messages appear in chat
- [ ] Bot responses load and display
- [ ] Workflow sidebar shows info
- [ ] No console errors
- [ ] Responsive design works on mobile
- [ ] Animations are smooth

### Integration Tests
- [ ] Frontend connects to backend via proxy
- [ ] CORS headers are properly set
- [ ] Session continuity works
- [ ] Chat history is maintained
- [ ] Error messages display properly
- [ ] Loading spinner shows while waiting
- [ ] Cleared chats work correctly

---

## 📊 Performance Tests

### Response Time Test
```bash
time curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}' > /dev/null
```

**Expected:** Response within 5-10 seconds

### Load Test (Simple)
```bash
for i in {1..5}; do
  curl -X POST http://localhost:3000/api/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "Test message '$i'"}' &
done
wait
```

**Expected:** All requests complete without hanging

---

## 🐛 Debugging Tips

### Enable Verbose Logging
In `app.py`, messages are already logged. Watch the terminal output:
```bash
python app.py
```

### Monitor Real-time Logs
```bash
tail -f backend.log
```

### Frontend Debugging
1. Open Browser DevTools (F12)
2. Console tab: Check for JavaScript errors
3. Network tab: Verify API requests and responses
4. Application tab: Check storage/session data

### Test Individual Components
```python
# Test LLM Client
python -c "
from demo.core.llm_client import LLMClient
llm = LLMClient()
print(llm.check_safety('Hello'))
"

# Test Router Agent
python -c "
from demo.agents.router_agent import RouterAgent
from demo.core.llm_client import LLMClient
llm = LLMClient()
router = RouterAgent(llm)
print(router.process('I feel anxious'))
"
```

---

## ✅ Sign-Off Checklist

Before considering the system ready, verify:

- [ ] Backend starts cleanly
- [ ] Frontend builds and loads
- [ ] All 3 API endpoints work (health, chat, history)
- [ ] Cards trigger correct routing
- [ ] Manual messages work
- [ ] Session continuity maintained
- [ ] Safety filters work
- [ ] Judge scores responses
- [ ] Workflow info displays
- [ ] No CORS errors
- [ ] No console errors
- [ ] Error messages are user-friendly
- [ ] Response times are acceptable
- [ ] Mobile UI is responsive

---

## 📝 Test Results Log

Use this template to record test results:

```
Date: 2025-11-08
Tester: [Your Name]

Test 1: Backend Health
Status: PASS / FAIL
Notes: 

Test 2: Basic Chat
Status: PASS / FAIL
Notes:

Test 3: Anxiety Detection
Status: PASS / FAIL
Notes:

Overall Status: READY / NEEDS WORK
Issues Found:
- Issue 1
- Issue 2

Recommendations:
- Rec 1
- Rec 2
```

---

**Happy Testing! 🧪🎉**
