#!/bin/bash
# 🚀 CompanionAI Quick Start Script
# Run this to start the chatbot system quickly

echo "════════════════════════════════════════════════════════════════"
echo "  🤖 CompanionAI - Multi-Agent Mental Health Counselling Bot  "
echo "════════════════════════════════════════════════════════════════"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo -e "${BLUE}[1/5] Checking Python installation...${NC}"
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.9+"
    exit 1
fi
echo -e "${GREEN}✓ Python found: $(python --version)${NC}"
echo ""

# Check Node.js
echo -e "${BLUE}[2/5] Checking Node.js installation...${NC}"
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 16+"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found: $(node --version)${NC}"
echo ""

# Install Python dependencies
echo -e "${BLUE}[3/5] Installing Python dependencies...${NC}"
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✓ Python dependencies installed${NC}"
echo ""

# Install Frontend dependencies
echo -e "${BLUE}[4/5] Installing Frontend dependencies...${NC}"
cd frontend
npm install > /dev/null 2>&1
cd ..
echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
echo ""

# Check .env file
echo -e "${BLUE}[5/5] Checking .env configuration...${NC}"
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    exit 1
fi

if ! grep -q "GROQ_API_KEY" .env; then
    echo -e "${YELLOW}⚠️  GROQ_API_KEY not set in .env${NC}"
else
    echo -e "${GREEN}✓ .env file configured${NC}"
fi
echo ""

echo "════════════════════════════════════════════════════════════════"
echo -e "${GREEN}✓ All checks passed!${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "🚀 Starting CompanionAI..."
echo ""
echo -e "${YELLOW}📌 IMPORTANT: Open 2 separate terminals and run:${NC}"
echo ""
echo -e "${BLUE}Terminal 1 (Backend - Port 3000):${NC}"
echo -e "${GREEN}  python app.py${NC}"
echo ""
echo -e "${BLUE}Terminal 2 (Frontend - Port 5000):${NC}"
echo -e "${GREEN}  cd frontend && npm run dev${NC}"
echo ""
echo -e "${YELLOW}Then open browser to: ${GREEN}http://localhost:5000${NC}"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "📝 For detailed instructions, see: SETUP_AND_RUN.md"
echo "════════════════════════════════════════════════════════════════"
