# 🚀 CompanionAI Deployment Guide

This guide covers multiple deployment options for your CompanionAI Multi-Agent Counseling System with **chat memory** functionality.

---

## 🌟 New Features in streamlit_demo.py

✨ **Chat Memory & Conversation Context**
- Remembers the last 3 conversation exchanges
- Context-aware responses that reference previous messages
- User profile tracking (topics discussed, interaction count)
- Session management with unique IDs
- Export conversation functionality

---

## Option 1: 🎯 Local Streamlit (Recommended for Testing)

### Quick Start

```bash
# Run the new demo with memory
streamlit run streamlit_demo.py
```

The app will open automatically at `http://localhost:8501`

### Features
- ✅ Full conversation memory
- ✅ Context-aware responses
- ✅ Beautiful gradient UI
- ✅ Session statistics
- ✅ Quick action buttons
- ✅ Export conversations
- ✅ Multi-agent workflow visualization

---

## Option 2: ☁️ Streamlit Cloud (FREE - Recommended for Demo)

### Why Streamlit Cloud?
- **100% FREE** for public apps
- No credit card required
- Automatic HTTPS
- Easy sharing with custom URL
- Auto-deploy from GitHub

### Setup Steps

#### 1. Prepare Your Repository

```bash
# Make sure you have these files
ls streamlit_demo.py
ls streamlit_requirements.txt
ls .streamlit/config.toml
ls .env
```

#### 2. Push to GitHub

```bash
git add streamlit_demo.py streamlit_requirements.txt .streamlit/
git commit -m "Add Streamlit demo with chat memory"
git push origin main
```

#### 3. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select:
   - Repository: `your-username/multi_agent_counselling`
   - Branch: `main`
   - Main file: `streamlit_demo.py`
5. Click "Deploy!"

#### 4. Add Secrets (Environment Variables)

In Streamlit Cloud dashboard:
1. Click "Settings" → "Secrets"
2. Add your `.env` contents:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
HUGGINGFACE_TOKEN = "your_huggingface_token_here"
```

#### 5. Share Your App

You'll get a URL like: `https://your-app-name.streamlit.app`

### Advantages
- ✅ FREE forever (for public apps)
- ✅ Professional URL
- ✅ HTTPS by default
- ✅ No server management
- ✅ Auto-restarts on code push

---

## Option 3: 🐳 Vercel (For Next.js/React Frontend)

If you prefer Vercel, you'll need to:

1. Keep the React frontend in `frontend/`
2. Deploy Flask backend separately (Render/Railway)
3. Update API endpoints

### Setup for Vercel

```bash
cd frontend
npm run build

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

**Note:** Vercel is better suited for static/Next.js apps. For your multi-agent system, **Streamlit Cloud is much easier**.

---

## Option 4: 🌐 Render (Full Stack)

Free tier available with automatic deploys.

### Backend (Flask)

Create `render.yaml`:

```yaml
services:
  - type: web
    name: companionai-backend
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python app.py"
    envVars:
      - key: GROQ_API_KEY
        sync: false
      - key: HUGGINGFACE_TOKEN
        sync: false
```

### Frontend (Streamlit)

1. Go to [render.com](https://render.com)
2. New → Web Service
3. Connect GitHub repo
4. Configure:
   - **Build Command:** `pip install -r streamlit_requirements.txt`
   - **Start Command:** `streamlit run streamlit_demo.py --server.port=$PORT`
5. Add environment variables

---

## Option 5: 🚂 Railway (Simple & Fast)

Railway offers free $5 credit monthly.

### Deploy Steps

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize
railway init

# Deploy
railway up
```

Add environment variables in Railway dashboard.

---

## 📊 Comparison Table

| Platform | Cost | Ease | Chat Memory | Best For |
|----------|------|------|-------------|----------|
| **Streamlit Cloud** | FREE | ⭐⭐⭐⭐⭐ | ✅ | **Quick demos, sharing** |
| Local | FREE | ⭐⭐⭐⭐⭐ | ✅ | Testing, development |
| Render | Free tier | ⭐⭐⭐⭐ | ✅ | Production apps |
| Railway | $5/mo free | ⭐⭐⭐⭐ | ✅ | Fast deployment |
| Vercel | FREE | ⭐⭐⭐ | ⚠️ | Static/Next.js only |

---

## 🎯 Recommended: Streamlit Cloud

For your real estate counseling system demo, I **strongly recommend Streamlit Cloud** because:

1. ✅ **100% Free** - No credit card, no hidden costs
2. ✅ **Chat Memory Works** - Full session state support
3. ✅ **Easy Sharing** - Get a professional URL instantly
4. ✅ **Zero Configuration** - Just push to GitHub and deploy
5. ✅ **Beautiful UI** - Built-in styling and components
6. ✅ **No Backend Setup** - Everything in one Python file

---

## 🔧 Testing Locally First

Before deploying, test locally:

```bash
# 1. Install dependencies
pip install -r streamlit_requirements.txt

# 2. Set up environment variables
# Make sure .env has:
# GROQ_API_KEY=your_key
# HUGGINGFACE_TOKEN=your_token

# 3. Run the app
streamlit run streamlit_demo.py

# 4. Test chat memory
# - Send a message about anxiety
# - Send a follow-up message referring to the first
# - Verify the AI remembers the context
```

---

## 🐛 Troubleshooting

### Chat Memory Not Working
- ✅ **Fixed in new version!** (`streamlit_demo.py`)
- Uses `st.session_state.conversation_history`
- Context passed to all agents

### "Module not found" errors
```bash
pip install -r streamlit_requirements.txt
```

### GROQ API errors
- Check `.env` file has correct `GROQ_API_KEY`
- Verify key at [console.groq.com](https://console.groq.com)

### Port already in use
```bash
streamlit run streamlit_demo.py --server.port 8502
```

---

## 📝 Quick Deployment Checklist

- [ ] Test locally with `streamlit run streamlit_demo.py`
- [ ] Verify chat memory works (send multiple related messages)
- [ ] Check `.env` has API keys
- [ ] Push code to GitHub
- [ ] Deploy to Streamlit Cloud
- [ ] Add secrets in Streamlit dashboard
- [ ] Test deployed version
- [ ] Share your URL! 🎉

---

## 🚀 Next Steps

Once deployed, you can:
1. **Customize UI** - Edit CSS in `streamlit_demo.py`
2. **Add More Agents** - Extend the multi-agent system
3. **Integrate Other Features** - Add price prediction, property recommendation
4. **Add Authentication** - Use Streamlit's auth (paid) or custom
5. **Analytics** - Track usage with Google Analytics

---

## 💡 Pro Tips

1. **For Demos**: Use Streamlit Cloud (free, instant)
2. **For Production**: Consider Render or Railway (more control)
3. **Chat Memory**: Always works in Streamlit's `session_state`
4. **Scaling**: Streamlit can handle moderate traffic; for high traffic, use distributed backend

---

## 📞 Support

If you encounter issues:
1. Check the logs in Streamlit Cloud dashboard
2. Test locally first
3. Verify environment variables are set
4. Check [Streamlit docs](https://docs.streamlit.io)

---

**Ready to deploy? Start with Streamlit Cloud! 🚀**

Your app URL will be: `https://[your-app-name].streamlit.app`
