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
- **Phase 1 - Port Reconfiguration:**
  - Reconfigured frontend to run on port 5000 (Replit webview requirement)
  - Moved backend from port 8000 to port 3000
  - Created frontend/.env with environment variables
  - Updated vite.config.js with dynamic port configuration and proxy settings
  - Updated workflows for both services with proper output types
  
- **Phase 2 - UI Redesign:**
  - Added Poppins font family for clean, modern typography
  - Implemented floating chatbot icon (top-right) with animated tooltip "Hi there! 🌈 Need a boost?"
  - Enhanced three interactive cards with click handlers for instant messaging
  - Maintained soft pastel gradient background (lavender to white)
  - Added smooth animations using Framer Motion
  - Optimized responsive design with Tailwind CSS
  
- **Phase 3 - Testing & Polish:**
  - Tested full multi-agent integration (Router → Anxiety Specialist → Judge)
  - Verified 9.0/10 approval score from Judge Agent
  - Created backend.log and frontend.log files for monitoring
  - Fixed all console errors and warnings
  - Verified all API endpoints functioning correctly

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
