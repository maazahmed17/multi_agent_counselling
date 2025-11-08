# 🔧 Troubleshooting: Cards & Messages Not Working

## ✅ Current System Status (VERIFIED WORKING)

Your system should now be fully functional:
- ✅ Backend running on port 3000
- ✅ Frontend running on port 5000  
- ✅ API proxy configured
- ✅ Health check responds
- ✅ Chat endpoint works via curl
- ✅ Chat endpoint works through proxy

---

## 🧪 Step 1: Test Backend Directly (No Frontend)

### Test 1.1: Health Check
```bash
curl http://localhost:3000/api/health
```

**Expected:**
```json
{
  "status": "healthy",
  "system": "CompanionAI Multi-Agent",
  "models": {...}
}
```

**If fails:** Backend not running
```bash
python app.py  # In first terminal
```

---

### Test 1.2: Chat Endpoint
```bash
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello test"}'
```

**Expected:** Full response with `response`, `session_id`, `workflow`, `approved`

**If fails:** Backend API has an issue - check backend terminal for errors

---

## 🧪 Step 2: Test Proxy (Via Frontend Port)

### Test 2.1: Health Through Proxy
```bash
curl http://localhost:5000/api/health
```

**Expected:** Same as direct backend response

**If fails:** Vite proxy not working
- Kill frontend: `pkill -9 node`
- Restart: `cd frontend && npm run dev`

---

### Test 2.2: Chat Through Proxy
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Test through proxy"}'
```

**Expected:** Full chat response

**If fails:**
1. Check Vite config has proxy:
   ```bash
   cat frontend/vite.config.js | grep -A 5 "proxy"
   ```
   
2. Restart Vite:
   ```bash
   pkill -9 node
   cd frontend && npm run dev
   ```

---

## 🌐 Step 3: Test Frontend in Browser

### Test 3.1: Open Frontend
1. Open browser: `http://localhost:5000`
2. Open browser console: Press `F12`
3. Look for console messages starting with 🔧 or 🔵

**What you should see:**
```
🔧 API_BASE_URL: /api
🔧 VITE_BACKEND_URL: /api
```

**If you see errors:**
- Check for JavaScript errors in red
- Check Network tab for failed requests

---

### Test 3.2: Click Card in Browser
1. Refresh page: `Ctrl+R` or `Cmd+R`
2. Open Console: `F12 → Console`
3. Click "I feel anxious" card
4. Watch console for messages

**Expected console output:**
```
🔵 sendMessage called! I'm feeling anxious and could use some support
📍 API_BASE_URL being used: /api
```

**If nothing appears:**
- Card click not triggering
- Check: Is the card clickable? (cursor should change)
- Try clicking directly on the card text

---

### Test 3.3: Type Message Manually
1. Scroll to bottom of page
2. Type in message input box: "Hello test"
3. Press Enter or click Send button
4. Watch console and chat box

**Expected:**
- Message appears on right side (blue)
- Loading animation appears
- Bot response appears on left side (gray)

**If message doesn't appear:**
- Check if input is accepting text
- Check browser console for errors
- Verify message isn't empty/whitespace

---

## 🐛 Browser Developer Tools Debugging

### Open DevTools: Press F12

#### Console Tab
- Look for RED error messages
- Look for console.log output starting with 🔧 or 🔵
- Run this command:
  ```javascript
  fetch('/api/health').then(r => r.json()).then(data => console.log('Health:', data))
  ```

#### Network Tab
1. Click Network tab
2. Clear previous requests
3. Click a card
4. Look for request to `/api/chat`
5. Check:
   - Status: Should be 200
   - Response: Should contain JSON with `response`, `session_id`

If you see a 404 or 500 error:
- 404: Backend URL wrong - check proxy config
- 500: Backend error - check backend terminal

#### Application/Storage Tab
1. Click Application (or Storage in Firefox)
2. Look for any saved session data
3. You can see cookies and local storage

---

## 🔍 Common Issues & Solutions

### Issue 1: "Cannot connect to server" Message in Chat

**Cause:** Backend not responding or proxy misconfigured

**Solution:**
```bash
# 1. Check backend is running
curl http://localhost:3000/api/health

# 2. If not, start backend
python app.py

# 3. Check proxy through frontend port
curl http://localhost:5000/api/health

# 4. If that fails, restart frontend
pkill -9 node
cd frontend && npm run dev
```

---

### Issue 2: Cards Not Clickable / Not Responding

**Cause:** JavaScript not executing or React state issue

**Solution:**
1. Refresh page: `Ctrl+R`
2. Open Console: `F12`
3. Run this:
   ```javascript
   document.querySelectorAll('[class*="cursor-pointer"]').length
   ```
   Should return 3+ (the cards + icons)

4. If 0: Cards aren't loading - check for JavaScript errors above

---

### Issue 3: Message Sent But No Response

**Cause:** Backend issue or slow response time

**Solution:**
1. Check console for errors
2. Check Network tab:
   - Request shows in Network tab?
   - Status is 200?
   - Response has data?
3. Check backend terminal for error messages
4. Wait 10+ seconds (first request is slow while loading models)

---

### Issue 4: Frontend Shows "Unable to connect to server"

**Cause:** Proxy misconfigured or backend down

**Solution:**
```bash
# Terminal 1: Check backend
curl http://localhost:3000/api/health

# If not responding, restart:
python app.py

# Terminal 2: Check proxy
curl http://localhost:5000/api/health

# If not responding, restart frontend:
pkill -9 node
cd frontend && npm run dev

# Then refresh browser
```

---

## 🚀 Complete Reset (Start Fresh)

If nothing is working, do a complete reset:

```bash
# 1. Kill all processes
pkill -9 python
pkill -9 node

# 2. Wait
sleep 3

# 3. Verify ports are free
lsof -i :3000
lsof -i :5000

# 4. Start backend (Terminal 1)
python app.py

# 5. Start frontend (Terminal 2)
cd frontend && npm run dev

# 6. Open browser
# http://localhost:5000

# 7. Open DevTools (F12)
# Check console for messages

# 8. Try clicking card
```

---

## 📋 Full Debugging Checklist

- [ ] Backend running: `python app.py`
- [ ] Frontend running: `cd frontend && npm run dev`
- [ ] Port 3000 free: `lsof -i :3000` (shows nothing)
- [ ] Port 5000 free: `lsof -i :5000` (shows node process)
- [ ] Backend responds: `curl http://localhost:3000/api/health`
- [ ] Chat works directly: `curl -X POST http://localhost:3000/api/chat ...`
- [ ] Proxy works: `curl http://localhost:5000/api/health`
- [ ] Frontend loads: Browser shows page, no 404
- [ ] Console has 🔧 messages: `F12 → Console`
- [ ] Card is clickable: Can see hover effect
- [ ] Message input works: Can type in box
- [ ] Message sends: Press Enter, message appears
- [ ] Response received: Wait 5-10 seconds, bot response appears
- [ ] No red errors: F12 → Console shows no red errors

---

## 📞 Quick Commands Reference

```bash
# Start everything
echo "Backend:"; python app.py &
echo "Frontend:"; cd frontend && npm run dev &

# Test backend
curl http://localhost:3000/api/health
curl -X POST http://localhost:3000/api/chat -H "Content-Type: application/json" -d '{"message":"Test"}'

# Test proxy
curl http://localhost:5000/api/health
curl http://localhost:5000/api/chat -X POST -H "Content-Type: application/json" -d '{"message":"Test"}'

# Check status
ps aux | grep -E "(python|node|vite)" | grep -v grep

# Kill everything
pkill -9 python
pkill -9 node
```

---

## 🎯 Expected Behavior (Step by Step)

### When You Click "I feel anxious" Card:

1. **Browser logs** (F12 → Console):
   ```
   🔧 API_BASE_URL: /api
   🔧 VITE_BACKEND_URL: /api
   🔵 sendMessage called! I'm feeling anxious and could use some support
   📍 API_BASE_URL being used: /api
   ```

2. **Network Tab** shows:
   - Request: `POST /api/chat`
   - Status: `200`
   - Response: Contains `response`, `session_id`, `workflow`

3. **Chat UI** shows:
   - User message appears blue on right
   - Loading dots animation
   - Bot response appears gray on left
   - Workflow info shows in sidebar

---

## 🆘 If Still Not Working

**Provide these details:**

1. Run and paste output:
   ```bash
   echo "=== Backend Health ===" && curl http://localhost:3000/api/health
   echo "=== Proxy Health ===" && curl http://localhost:5000/api/health
   echo "=== Processes ===" && ps aux | grep -E "(python|node)" | grep -v grep
   ```

2. Browser console errors (F12 → Console, paste any red errors)

3. Backend terminal output (last 20 lines)

4. Frontend terminal output (check `frontend.log` or terminal)

---

**Status: Your system should now be fully working! 🎉**

Try clicking a card and watch the console with F12 open.

If you see the 🔵 and 📍 messages in the console, the frontend is working correctly.
