#!/bin/bash
# Entroplain Setup Script for macOS/Linux
# Usage: curl -sSL https://raw.githubusercontent.com/entroplain/entroplain/main/scripts/setup.sh | bash

set -e

echo "=============================================================="
echo "  ENTROPAIN SETUP - macOS/Linux"
echo "=============================================================="

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "   Install with: brew install python3 (macOS) or sudo apt install python3 (Linux)"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    exit 1
fi

# Install entroplain
echo ""
echo -e "${BLUE}Installing entroplain...${NC}"
pip3 install --upgrade entroplain

# Verify installation
if python3 -c "import entroplain" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} entroplain installed successfully"
else
    echo "❌ Installation failed"
    exit 1
fi

# Check for API keys
echo ""
echo "=============================================================="
echo "  API KEY SETUP"
echo "=============================================================="

PROVIDERS=""
if [ -n "$OPENAI_API_KEY" ]; then
    echo -e "${GREEN}✓${NC} OPENAI_API_KEY is set"
    PROVIDERS="$PROVIDERS openai"
fi
if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo -e "${GREEN}✓${NC} ANTHROPIC_API_KEY is set"
    PROVIDERS="$PROVIDERS anthropic"
fi
if [ -n "$NVIDIA_API_KEY" ]; then
    echo -e "${GREEN}✓${NC} NVIDIA_API_KEY is set"
    PROVIDERS="$PROVIDERS nvidia"
fi
if [ -n "$GOOGLE_API_KEY" ]; then
    echo -e "${GREEN}✓${NC} GOOGLE_API_KEY is set"
    PROVIDERS="$PROVIDERS google"
fi

if [ -z "$PROVIDERS" ]; then
    echo ""
    echo "⚠️  No API keys found. Set at least one:"
    echo ""
    echo "   export OPENAI_API_KEY='your-key'"
    echo "   export ANTHROPIC_API_KEY='your-key'"
    echo "   export NVIDIA_API_KEY='your-key'"
    echo "   export GOOGLE_API_KEY='your-key'"
    echo ""
    echo "   Add to ~/.bashrc or ~/.zshrc to persist"
fi

# Usage examples
echo ""
echo "=============================================================="
echo "  QUICK START"
echo "=============================================================="
echo ""
echo "  # Analyze entropy:"
echo "  entroplain analyze \"Your prompt here\""
echo ""
echo "  # Stream with early exit:"
echo "  entroplain stream --exit-on-converge \"Your prompt here\""
echo ""
echo "  # Start proxy with dashboard:"
echo "  entroplain-proxy --port 8765 --provider openai"
echo "  # Then open http://localhost:8765/dashboard"
echo ""
echo "=============================================================="
echo -e "${GREEN}Setup complete!${NC}"
