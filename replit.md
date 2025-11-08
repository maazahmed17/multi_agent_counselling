# CompanionAI Anxiety Specialist

## Overview
A full-stack mental health support application featuring a multi-agent AI system powered by Groq's Llama 3.3 70B model. The application provides anxiety support using CBT principles through an intelligent routing system, specialized agents, and quality evaluation.

## Project Structure

### Backend (Python/Flask)
- `app.py` - Flask API server exposing multi-agent system endpoints
- `demo/agents/` - Multi-agent system components
  - `router_agent.py` - Routes user messages to appropriate specialists
  - `anxiety_specialist.py` - CBT-based anxiety support agent
  - `judge_agent.py` - Evaluates and approves responses for quality
  - `test_agents.py` - Testing script for agent functionality
- `demo/core/llm_client.py` - Direct HTTP client for Groq API (no SDK dependencies)

### Frontend (React/Vite)
- `frontend/src/` - React application
  - `SerenityDashboard.jsx` - Main chat interface with beautiful UI
  - `App.jsx` - Application entry point
- `frontend/vite.config.js` - Vite configuration with proxy to backend API

### ML Components (Training - Not Active)
- `anxiety.py` - Original training script for Llama fine-tuning
- `models/anxiety_specialist_v1/` - Trained LoRA adapter weights
- `eval_outputs/` - Evaluation metrics and results

## Recent Changes (November 8, 2025)

### **Complete UI Redesign to Match Reference Image**

**Backend Connectivity Fixes:**
- Backend reconfigured to run on 0.0.0.0:8000 (as specified)
- Frontend uses localhost:8000 with Vite proxy for API calls
- Replaced deprecated `onKeyPress` with `onKeyDown` for React 18 compatibility
- Removed conflicting old vanilla JavaScript files (app.js)
- Fixed index.html to properly load React app via main.jsx
- Backend running on port 8000, frontend on port 5000
- CORS properly configured for cross-origin requests

**UI Redesign - Matching Reference Image:**
- **Chatbot Mascot**: Large 128px robot emoji (🤖) with animated floating effect
- **Speech Bubble**: Positioned above mascot with "Hi there! 🌈 Need a boost?" message
- **Background**: Warmer lavender-to-purple gradient (#E8E9FF → #F5F3FF → #FCF5FF) with decorative radial orbs
- **Cards**: Glassmorphism design with backdrop-blur, larger emoji (5xl), larger text (2xl), generous spacing (gap-8)
- **Input Bar**: Fixed position at bottom, full-width pill design, gradient send button
- **Layout**: Centered hero design with maximum 5xl width, better vertical spacing
- **Sidebar**: Translucent glass effect (bg-white/40) with backdrop-blur
- **Animations**: Smooth Framer Motion transitions for all interactive elements

**Testing & Verification:**
- ✅ Full multi-agent workflow tested (Router → Anxiety Specialist → Judge)
- ✅ 9.0/10 approval score from Judge Agent
- ✅ Zero console errors or warnings
- ✅ Backend API endpoints fully functional
- ✅ Frontend-backend connectivity verified
- ✅ Architect tool reviewed and approved all changes

## Architecture

### Current Stack (Production)
- **Frontend**: React + Vite + Tailwind CSS + Framer Motion (Port 5000)
- **Backend**: Flask (Python) REST API (Port 3000)
- **LLM Provider**: Groq API (Llama 3.3 70B Versatile)
- **Multi-Agent System**: Router → Specialist → Judge workflow
- **UI Framework**: React Icons, Poppins font, responsive design
- **Design**: Calming pastel theme with floating chatbot, animated tooltips

### Multi-Agent Workflow
1. **Router Agent**: Analyzes user input and routes to appropriate specialist
2. **Anxiety Specialist Agent**: Generates CBT-based supportive responses
3. **Judge Agent**: Evaluates response quality (empathy, safety, clinical accuracy)
4. Response only sent to user if approved by Judge Agent

### Original ML Stack (Training Components - Inactive)
- **Base Model**: Meta Llama 3.1 8B Instruct
- **Fine-tuning Method**: QLoRA (4-bit quantization + LoRA)
- **Framework**: PyTorch, HuggingFace Transformers, PEFT
- **Training**: TRL (Transformer Reinforcement Learning)
- **Optimization**: BitsAndBytes 4-bit quantization

## Important Notes

### GPU Requirements
This project is designed for **GPU training** with CUDA support. The current Replit environment runs on CPU only, which means:
- ✅ Code can be viewed and edited
- ✅ Dependencies are installed
- ✅ Project structure can be explored
- ❌ Training cannot run (requires NVIDIA GPU with CUDA)
- ❌ Model inference will be extremely slow on CPU

### Running Locally
To run this project on a machine with NVIDIA GPU:
1. Set up a conda environment: `conda env create -f ai_env.yml`
2. Or install from requirements.txt: `pip install -r requirements.txt`
3. Ensure CUDA and cuDNN are properly installed
4. Run validation: `python validate_setup.py`
5. Start training: `python anxiety.py`

### Dataset Requirements
The training scripts expect datasets in `./data_lake/mentalchat16k/processed/` directory:
- `anxiety_sft_train.jsonl` - Training data
- `anxiety_sft_val.jsonl` - Validation data  
- `anxiety_sft_test.jsonl` - Test data

These are not included in the repository and need to be prepared separately.

## User Preferences
- Optimized for RTX 4060 8GB VRAM
- Conservative memory settings to prevent OOM errors
- Offline-first approach (uses local model cache)
- Focus on anxiety support using CBT methodology

## Development Environment
- Python 3.11.13
- PyTorch (CPU-only in Replit)
- No conda in Replit (using pip)
- Git version control enabled
