#!/usr/bin/env python3
"""
🤖 CompanionAI Unified System Runner
Allows choosing between Web Interface or Terminal CLI mode
"""

import sys
import os
import subprocess
import time
import signal
from pathlib import Path
from typing import Optional

# Add demo directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Color codes for terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header():
    """Print ASCII art header"""
    header = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║         🤖 CompanionAI - Multi-Agent Counselling System 🤖       ║
║                                                                   ║
║          Choose your interaction mode: Web or Terminal            ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.END}
"""
    print(header)

def print_menu():
    """Print main menu"""
    print(f"\n{Colors.BOLD}Select Mode:{Colors.END}\n")
    print(f"{Colors.BLUE}1){Colors.END} {Colors.GREEN}🌐 Web Interface{Colors.END}")
    print(f"   - Beautiful React UI with animations")
    print(f"   - 3 quick-action cards")
    print(f"   - Real-time chat + workflow visualization")
    print(f"   - Access via browser on http://localhost:5000\n")
    
    print(f"{Colors.BLUE}2){Colors.END} {Colors.CYAN}💬 Terminal CLI{Colors.END}")
    print(f"   - Direct text-based interaction")
    print(f"   - No browser required")
    print(f"   - Simple and fast")
    print(f"   - Great for testing/debugging\n")
    
    print(f"{Colors.BLUE}3){Colors.END} {Colors.YELLOW}⚙️  Run Both (Web + CLI Backend){Colors.END}")
    print(f"   - Start backend on port 3000")
    print(f"   - Start frontend on port 5000")
    print(f"   - You can interact via web\n")
    
    print(f"{Colors.BLUE}4){Colors.END} {Colors.RED}❌ Exit{Colors.END}\n")

def mode_web_interface():
    """Start web interface (backend + frontend)"""
    print(f"\n{Colors.GREEN}🌐 Starting Web Interface...{Colors.END}\n")
    print(f"{Colors.YELLOW}This will start:{Colors.END}")
    print(f"  - Backend (Flask) on port 3000")
    print(f"  - Frontend (Vite) on port 5000")
    print(f"  - Open browser to: http://localhost:5000\n")
    
    print(f"{Colors.BOLD}Starting backend...{Colors.END}")
    backend_proc = subprocess.Popen(
        ["python", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    time.sleep(5)  # Wait for backend to initialize
    
    print(f"{Colors.BOLD}Starting frontend...{Colors.END}")
    frontend_proc = subprocess.Popen(
        ["bash", "-c", "cd frontend && npm run dev"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    time.sleep(3)  # Wait for frontend to start
    
    print(f"\n{Colors.GREEN}✅ Services started!{Colors.END}\n")
    print(f"{Colors.BOLD}Web Interface URLs:{Colors.END}")
    print(f"  🌐 Frontend: {Colors.CYAN}http://localhost:5000{Colors.END}")
    print(f"  🔌 Backend API: {Colors.CYAN}http://localhost:3000/api{Colors.END}\n")
    
    print(f"{Colors.YELLOW}Press Ctrl+C to stop services{Colors.END}\n")
    
    try:
        backend_proc.wait()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Stopping services...{Colors.END}")
        backend_proc.terminate()
        frontend_proc.terminate()
        time.sleep(1)
        backend_proc.kill()
        frontend_proc.kill()
        print(f"{Colors.GREEN}✅ Services stopped{Colors.END}")

def mode_terminal_cli():
    """Start terminal CLI mode"""
    print(f"\n{Colors.CYAN}💬 Terminal CLI Mode{Colors.END}\n")
    
    try:
        from demo.core.llm_client import LLMClient
        from demo.agents.router_agent import RouterAgent
        from demo.agents.anxiety_specialist import AnxietySpecialistAgent
        from demo.agents.judge_agent import JudgeAgent
    except ImportError as e:
        print(f"{Colors.RED}❌ Error importing modules: {e}{Colors.END}")
        return
    
    print(f"{Colors.GREEN}🚀 Initializing CompanionAI Multi-Agent System...{Colors.END}\n")
    
    try:
        llm_client = LLMClient()
        router = RouterAgent(llm_client)
        anxiety_specialist = AnxietySpecialistAgent(llm_client)
        judge = JudgeAgent(llm_client)
        print(f"{Colors.GREEN}✅ Multi-Agent System Ready!{Colors.END}\n")
    except Exception as e:
        print(f"{Colors.RED}❌ Error initializing system: {e}{Colors.END}")
        return
    
    # Check for Replit DB
    try:
        from replit import db
        HAS_DB = True
        print(f"{Colors.GREEN}✅ Replit Database connected{Colors.END}\n")
    except ImportError:
        HAS_DB = False
        print(f"{Colors.YELLOW}⚠️  Running without Replit DB (using in-memory storage){Colors.END}\n")
        db = {}
    
    sessions = {}
    session_id = None
    
    print(f"{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.CYAN}Welcome to CompanionAI Terminal Interface!{Colors.END}")
    print(f"{Colors.BOLD}{'='*70}{Colors.END}\n")
    
    print(f"{Colors.YELLOW}Commands:{Colors.END}")
    print(f"  • Type your message and press Enter to chat")
    print(f"  • Type {Colors.BOLD}'new'{Colors.END} to start a new conversation")
    print(f"  • Type {Colors.BOLD}'history'{Colors.END} to see chat history")
    print(f"  • Type {Colors.BOLD}'stats'{Colors.END} to see system stats")
    print(f"  • Type {Colors.BOLD}'help'{Colors.END} for more options")
    print(f"  • Type {Colors.BOLD}'exit'{Colors.END} or {Colors.BOLD}'quit'{Colors.END} to exit\n")
    
    print(f"{Colors.BOLD}{'='*70}{Colors.END}\n")
    
    def _handle_crisis(user_input, llm):
        """Handle crisis situations"""
        crisis_prompt = """You are a crisis counselor. The user is in distress. Respond with:
1. Immediate empathy and validation
2. Crisis resources (hotlines, emergency contacts)
3. Encouragement to seek immediate professional help
Keep response brief and focused on immediate safety."""
        return llm.generate_response(user_input, system_prompt=crisis_prompt, max_tokens=300, temperature=0.5)
    
    def _handle_general(user_input, llm):
        """Handle general mental health queries"""
        general_prompt = """You are a supportive mental health assistant. Provide general guidance, validate feelings, and suggest appropriate next steps. Be warm and non-judgmental."""
        return llm.generate_response(user_input, system_prompt=general_prompt, max_tokens=400, temperature=0.7)
    
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
    
    chat_history = []
    
    # Main chat loop
    while True:
        try:
            user_input = input(f"{Colors.BOLD}{Colors.BLUE}You: {Colors.END}").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() == 'exit' or user_input.lower() == 'quit':
                print(f"\n{Colors.CYAN}Thank you for using CompanionAI. Take care! 👋{Colors.END}\n")
                break
            
            elif user_input.lower() == 'new':
                session_id = None
                chat_history = []
                print(f"{Colors.GREEN}✅ New conversation started{Colors.END}\n")
                continue
            
            elif user_input.lower() == 'history':
                if not chat_history:
                    print(f"{Colors.YELLOW}No chat history yet{Colors.END}\n")
                else:
                    print(f"\n{Colors.BOLD}Chat History:{Colors.END}")
                    for i, msg in enumerate(chat_history, 1):
                        print(f"{Colors.BLUE}{i}. You:{Colors.END} {msg['user']}")
                        print(f"{Colors.CYAN}   Bot:{Colors.END} {msg['bot'][:100]}...")
                    print()
                continue
            
            elif user_input.lower() == 'stats':
                print(f"\n{Colors.BOLD}System Statistics:{Colors.END}")
                print(f"  Total messages: {len(chat_history)}")
                print(f"  Session ID: {session_id or 'Not set'}")
                print(f"  Database: {'Replit DB' if HAS_DB else 'In-memory'}\n")
                continue
            
            elif user_input.lower() == 'help':
                print(f"\n{Colors.BOLD}Available Commands:{Colors.END}")
                print(f"  • {Colors.BOLD}new{Colors.END} - Start new conversation")
                print(f"  • {Colors.BOLD}history{Colors.END} - Show chat history")
                print(f"  • {Colors.BOLD}stats{Colors.END} - Show system statistics")
                print(f"  • {Colors.BOLD}help{Colors.END} - Show this help message")
                print(f"  • {Colors.BOLD}exit/quit{Colors.END} - Exit the application\n")
                continue
            
            # Process message
            print(f"\n{Colors.YELLOW}Processing...{Colors.END}")
            
            # STEP 1: Pre-Safety Gate
            pre_safety = llm_client.check_safety(user_input)
            
            if not pre_safety["is_safe"]:
                print(f"{Colors.RED}[Safety Alert] Input flagged as unsafe: {pre_safety['category']}{Colors.END}\n")
                crisis_response = _generate_crisis_response(pre_safety)
                print(f"{Colors.CYAN}Bot: {Colors.END}{crisis_response}\n")
                chat_history.append({"user": user_input, "bot": crisis_response})
                continue
            
            # STEP 2: Router
            routing = router.process(user_input)
            specialist_type = routing["specialist"]
            
            # STEP 3: Specialist Response
            if specialist_type == "anxiety":
                specialist_result = anxiety_specialist.process(user_input)
                bot_response = specialist_result["response"]
                print(f"{Colors.BOLD}[Routed to: Anxiety Specialist]{Colors.END}")
            elif specialist_type == "crisis":
                bot_response = _handle_crisis(user_input, llm_client)
                print(f"{Colors.BOLD}[Routed to: Crisis Handler]{Colors.END}")
            else:
                bot_response = _handle_general(user_input, llm_client)
                print(f"{Colors.BOLD}[Routed to: General Support]{Colors.END}")
            
            # STEP 4: Judge Evaluation
            evaluation = judge.process(user_input, bot_response)
            judge_score = evaluation["scores"]["overall"]
            approved = evaluation["approved"]
            
            print(f"{Colors.BOLD}[Quality Score: {judge_score}/10 - {'Approved ✓' if approved else 'Review ⚠'}]{Colors.END}\n")
            
            # STEP 5: Post-Safety Gate
            post_safety = llm_client.check_safety(bot_response)
            
            if not post_safety["is_safe"]:
                print(f"{Colors.RED}[Safety Alert] Response flagged as unsafe{Colors.END}")
                bot_response = "I apologize, but I need to rephrase my response to ensure it's safe. Please ask again."
                approved = False
            
            # Display response
            print(f"{Colors.CYAN}Bot: {Colors.END}{bot_response}\n")
            
            # Store in history
            chat_history.append({"user": user_input, "bot": bot_response})
        
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Interrupted by user{Colors.END}\n")
            break
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.END}\n")

def mode_both():
    """Start both web interface and backend"""
    print(f"\n{Colors.YELLOW}⚙️  Starting Both Services...{Colors.END}\n")
    print(f"{Colors.GREEN}Backend: Flask on port 3000{Colors.END}")
    print(f"{Colors.GREEN}Frontend: Vite on port 5000{Colors.END}\n")
    
    print(f"{Colors.BOLD}Starting backend...{Colors.END}")
    backend_proc = subprocess.Popen(
        ["python", "app.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    time.sleep(5)
    
    print(f"{Colors.BOLD}Starting frontend...{Colors.END}")
    frontend_proc = subprocess.Popen(
        ["bash", "-c", "cd frontend && npm run dev"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    time.sleep(3)
    
    print(f"\n{Colors.GREEN}✅ Both services started!{Colors.END}\n")
    print(f"{Colors.BOLD}Access URLs:{Colors.END}")
    print(f"  🌐 Web UI: {Colors.CYAN}http://localhost:5000{Colors.END}")
    print(f"  🔌 API: {Colors.CYAN}http://localhost:3000/api{Colors.END}\n")
    print(f"{Colors.YELLOW}Press Ctrl+C to stop both services{Colors.END}\n")
    
    try:
        backend_proc.wait()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Stopping services...{Colors.END}")
        backend_proc.terminate()
        frontend_proc.terminate()
        time.sleep(1)
        backend_proc.kill()
        frontend_proc.kill()
        print(f"{Colors.GREEN}✅ Services stopped{Colors.END}\n")

def main():
    """Main function"""
    print_header()
    
    while True:
        print_menu()
        
        choice = input(f"{Colors.BOLD}Enter your choice (1-4): {Colors.END}").strip()
        
        if choice == "1":
            mode_web_interface()
        elif choice == "2":
            mode_terminal_cli()
        elif choice == "3":
            mode_both()
        elif choice == "4":
            print(f"\n{Colors.CYAN}Thank you for using CompanionAI! Goodbye! 👋{Colors.END}\n")
            sys.exit(0)
        else:
            print(f"{Colors.RED}❌ Invalid choice. Please try again.{Colors.END}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}System interrupted by user{Colors.END}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Unexpected error: {e}{Colors.END}\n")
        sys.exit(1)
