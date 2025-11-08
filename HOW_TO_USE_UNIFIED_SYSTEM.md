# 🚀 How to Use run_unified_system.py

## Quick Start

```bash
python run_unified_system.py
```

Or:

```bash
./run_unified_system.py
```

---

## 📋 Main Menu Options

When you run the script, you'll see this menu:

```
╔═══════════════════════════════════════════════════════════════════╗
║         🤖 CompanionAI - Multi-Agent Counselling System 🤖       ║
║          Choose your interaction mode: Web or Terminal            ║
╚═══════════════════════════════════════════════════════════════════╝

Select Mode:

1) 🌐 Web Interface
   - Beautiful React UI with animations
   - 3 quick-action cards
   - Real-time chat + workflow visualization
   - Access via browser on http://localhost:5000

2) 💬 Terminal CLI
   - Direct text-based interaction
   - No browser required
   - Simple and fast
   - Great for testing/debugging

3) ⚙️  Run Both (Web + CLI Backend)
   - Start backend on port 3000
   - Start frontend on port 5000
   - You can interact via web

4) ❌ Exit
```

---

## 🌐 Option 1: Web Interface

**What it does:**
- Starts Flask backend on port 3000
- Starts Vite frontend on port 5000
- Opens the full web UI

**How to use:**
1. Select option `1`
2. Wait for startup messages
3. Open browser to `http://localhost:5000`
4. Click cards or type messages
5. Press `Ctrl+C` to stop services

**Perfect for:**
- Interactive testing with UI
- Demonstrations
- User experience testing
- Production-like environment

---

## 💬 Option 2: Terminal CLI

**What it does:**
- Runs the multi-agent system directly in terminal
- No web interface needed
- Direct command-line interaction

**How to use:**
1. Select option `2`
2. Wait for system initialization (first time takes longer - loading LLM models)
3. Type your message and press Enter
4. See bot response immediately
5. Use special commands (see below)

**Perfect for:**
- Quick testing without browser
- Debugging
- API validation
- Server environments without GUI

### Terminal CLI Commands

Once you're in the CLI, you can use these commands:

```
Type your message and press Enter to chat
- Type 'new' to start a new conversation
- Type 'history' to see chat history
- Type 'stats' to see system stats
- Type 'help' for more options
- Type 'exit' or 'quit' to exit
```

#### Command Examples

```
You: I'm feeling anxious about my exam

[Routed to: Anxiety Specialist]
[Quality Score: 8.5/10 - Approved ✓]

Bot: I understand that exams can feel overwhelming...

---

You: history

1. You: I'm feeling anxious about my exam
   Bot: I understand that exams can feel overwhelming...

---

You: stats

System Statistics:
  Total messages: 1
  Session ID: 550e8400-e29b-41d4-a716-446655440000
  Database: In-memory

---

You: new

✅ New conversation started
```

---

## ⚙️ Option 3: Run Both

**What it does:**
- Starts both backend and frontend
- Everything runs in the background
- You can access the web interface

**How to use:**
1. Select option `3`
2. Both services start automatically
3. Open browser to `http://localhost:5000`
4. Use the web interface normally
5. Press `Ctrl+C` to stop both

**Perfect for:**
- Complete system testing
- Development work
- End-to-end testing
- Full feature demonstration

---

## 🎯 Usage Scenarios

### Scenario 1: Quick API Testing
```bash
python run_unified_system.py
→ Select 2 (Terminal CLI)
→ Type test messages
→ Verify responses
```

### Scenario 2: Web UI Testing
```bash
python run_unified_system.py
→ Select 1 (Web Interface)
→ Click cards in browser
→ Test form submission
```

### Scenario 3: Full System Test
```bash
python run_unified_system.py
→ Select 3 (Run Both)
→ Test web UI
→ Watch backend logs
```

### Scenario 4: Debugging
```bash
python run_unified_system.py
→ Select 2 (Terminal CLI)
→ Type specific test cases
→ Watch console output
→ See routing, scoring, safety checks
```

---

## 📊 What You See in Terminal CLI

### Successful Message Processing

```
You: I'm feeling stressed about work

Processing...

[Routed to: General Support]
[Quality Score: 8/10 - Approved ✓]

Bot: I understand work stress can feel overwhelming. Here are some strategies...

```

### Safety Alert (Harmful Input)

```
You: I want to hurt myself

Processing...

[Safety Alert] Input flagged as unsafe: S11

Bot: I'm really concerned about what you've shared. Your safety is the most important thing...
[Crisis resources...]

```

### System Statistics

```
You: stats

System Statistics:
  Total messages: 5
  Session ID: 550e8400-e29b-41d4-a716-446655440000
  Database: Replit DB
```

---

## 🛠️ Features by Mode

| Feature | Web Interface | Terminal CLI | Both |
|---------|---------------|--------------|------|
| Visual UI | ✅ Yes | ❌ No | ✅ Yes |
| Quick Testing | ⚠️ Slower | ✅ Fast | ⚠️ Moderate |
| No Browser Required | ❌ No | ✅ Yes | ❌ No |
| Built-in Commands | ❌ No | ✅ Yes | ✅ (API) |
| Chat History Display | ✅ Yes | ✅ Yes | ✅ Yes |
| Workflow Visualization | ✅ Yes | ⚠️ Text | ✅ Yes |
| Easy Debugging | ⚠️ Via Console | ✅ Direct | ✅ Direct |

---

## 🔄 Flow Diagram

```
python run_unified_system.py
    ↓
┌───────────────────────────────────────────┐
│ Select Mode (1/2/3/4)                    │
└───────────────────────────────────────────┘
    ↓        ↓         ↓
    │        │         │
    ↓        ↓         ↓
┌─────────┐ ┌──────────┐ ┌────────────────────┐
│ Option 1│ │ Option 2│ │   Option 3         │
│Web UI   │ │Terminal │ │ Both Services      │
└─────────┘ └──────────┘ └────────────────────┘
    ↓        ↓         ↓
Backend   CLI Loop  Backend +
+ Frontend → (Chat) Frontend
 Running   Exit    Running
```

---

## ⌨️ Keyboard Shortcuts

### In Terminal CLI
- `Ctrl+C` - Exit current mode
- `↑/↓` - Command history (if supported)
- `Enter` - Send message

### In Web Interface
- `F12` - Open Developer Tools
- `Ctrl+R` - Refresh page
- `Ctrl+Shift+Delete` - Clear browser cache

---

## 🐛 Troubleshooting

### Issue: "Address already in use"
**Solution:** Old processes still running
```bash
pkill -9 python
pkill -9 node
# Then run again
python run_unified_system.py
```

### Issue: Terminal CLI shows "Error importing modules"
**Solution:** Dependencies not installed
```bash
pip install -r requirements.txt
cd frontend && npm install && cd ..
```

### Issue: Web Interface not responding
**Solution:** Backend may be loading (first time is slow)
- Wait 10+ seconds for LLM models to load
- Check browser console (F12) for errors

### Issue: No visible output in CLI mode
**Solution:** Messages may be getting lost
- Try typing `help` to see if system responds
- Check that GROQ_API_KEY is set in .env

---

## 💡 Tips & Tricks

### Tip 1: Mix Modes
You can run multiple instances:
```bash
Terminal 1: python run_unified_system.py → Option 1 (Web)
Terminal 2: python run_unified_system.py → Option 2 (CLI)
```

### Tip 2: Quick Testing
```bash
python run_unified_system.py << EOF
2
I'm feeling anxious
help
exit
EOF
```

### Tip 3: Test Multiple Scenarios
```bash
Terminal CLI → Type different test messages
→ See routing, scoring, safety checks
→ Perfect for QA
```

### Tip 4: Monitor Backend
```bash
Terminal 1: python run_unified_system.py → Option 3
Terminal 2: tail -f backend.log
→ Watch both web UI and backend logs
```

---

## 📝 Example Session

```bash
$ python run_unified_system.py

╔═══════════════════════════════════════════════════════════════════╗
║         🤖 CompanionAI - Multi-Agent Counselling System 🤖       ║
║          Choose your interaction mode: Web or Terminal            ║
╚═══════════════════════════════════════════════════════════════════╝

Select Mode:

1) 🌐 Web Interface
2) 💬 Terminal CLI
3) ⚙️  Run Both
4) ❌ Exit

Enter your choice (1-4): 2

💬 Terminal CLI Mode

🚀 Initializing CompanionAI Multi-Agent System...

✅ Multi-Agent System Ready!
✅ Replit Database connected

══════════════════════════════════════════════════════════════════

Welcome to CompanionAI Terminal Interface!

══════════════════════════════════════════════════════════════════

Commands:
  • Type your message and press Enter to chat
  • Type 'new' to start a new conversation
  • Type 'history' to see chat history
  • Type 'stats' to see system stats
  • Type 'help' for more options
  • Type 'exit' or 'quit' to exit

══════════════════════════════════════════════════════════════════

You: I'm feeling anxious about my upcoming interview

Processing...

[Routed to: Anxiety Specialist]
[Quality Score: 9/10 - Approved ✓]

Bot: I can understand how interviews can trigger anxiety. Here are some evidence-based strategies...

You: Can you give me a breathing exercise?

Processing...

[Routed to: Anxiety Specialist]
[Quality Score: 8.5/10 - Approved ✓]

Bot: Absolutely! Try the 4-7-8 breathing technique...

You: exit

Thank you for using CompanionAI. Take care! 👋

$
```

---

## 🎓 Next Steps

1. **First Time?**
   - Read this guide
   - Run Option 2 (Terminal CLI) first
   - Test with simple messages

2. **Want to See UI?**
   - Run Option 1 (Web Interface)
   - Open browser to http://localhost:5000
   - Click the cards

3. **Full Testing?**
   - Run Option 3 (Both)
   - Test both CLI and Web simultaneously
   - Check backend logs

4. **Ready for Production?**
   - Option 1 for deployment
   - Monitor logs continuously
   - Use load testing tools

---

**Enjoy using CompanionAI! 🎉**

For more information, see:
- `README_FIRST.md` - Project overview
- `TROUBLESHOOT_CARDS_AND_MESSAGES.md` - Debugging guide
- `ANALYSIS_AND_SOLUTION.md` - Technical details
