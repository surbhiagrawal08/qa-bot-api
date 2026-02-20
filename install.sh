#!/bin/bash
# Installation script for Zania QA Bot

set -e  # Exit on error

echo "🚀 Zania QA Bot - Installation Script"
echo "======================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
python3 --version || { echo "❌ Python 3 not found!"; exit 1; }

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo "📥 Installing dependencies..."
echo "This may take a few minutes..."
pip install -r requirements.txt

# Verify installation
echo ""
echo "✅ Verifying installation..."
python3 check_imports.py

# Set up environment variables
if [ ! -f .env ]; then
    echo ""
    echo "🔑 Setting up environment variables..."
    ./setup_env.sh
else
    echo "✓ .env file already exists"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "To start the server, run:"
echo "  ./run.sh"
echo ""
echo "Or manually:"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
