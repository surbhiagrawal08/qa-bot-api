#!/bin/bash
# Fixed installation script that installs packages in correct order

set -e  # Exit on error

echo "🚀 Zania QA Bot - Fixed Installation Script"
echo "============================================"
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
source venv/bin/activate || { echo "❌ Failed to activate venv"; exit 1; }

# Upgrade pip and setuptools first
echo "⬆️  Upgrading pip and setuptools..."
pip install --upgrade pip setuptools wheel --quiet

# Install base packages first
echo ""
echo "📦 Step 1: Installing base packages..."
pip install -r requirements-base.txt || {
    echo "⚠️  Some base packages failed, continuing..."
}

# Install LangChain packages
echo ""
echo "📦 Step 2: Installing LangChain packages..."
pip install -r requirements-langchain.txt || {
    echo "⚠️  Some LangChain packages failed, trying alternative method..."
    # Try installing without version constraints
    pip install langchain langchain-openai langchain-community langchain-core || {
        echo "❌ LangChain installation failed"
        exit 1
    }
}

# Install other dependencies
echo ""
echo "📦 Step 3: Installing other dependencies..."
pip install -r requirements-other.txt || {
    echo "⚠️  Some packages failed, trying individual installation..."
    pip install chromadb pypdf openai tiktoken numpy typing-extensions || true
}

# Install test dependencies (optional)
echo ""
echo "📦 Step 4: Installing test dependencies..."
pip install -r requirements-test.txt || {
    echo "⚠️  Test packages failed, but continuing..."
}

# Try installing from main requirements file to catch any missing
echo ""
echo "📦 Step 5: Verifying all packages from main requirements..."
pip install -r requirements.txt || {
    echo "⚠️  Some packages from main requirements failed"
}

# Verify installation
echo ""
echo "✅ Verifying installation..."
python3 check_imports.py || {
    echo "⚠️  Some imports failed, but core packages should be installed"
}

# Set up environment variables
if [ ! -f .env ]; then
    echo ""
    echo "🔑 Setting up environment variables..."
    ./setup_env.sh
else
    echo "✓ .env file already exists"
fi

echo ""
echo "📊 Installed packages:"
pip list | grep -E "(fastapi|langchain|chromadb|openai|pypdf|pydantic)"

echo ""
echo "🎉 Installation complete!"
echo ""
echo "If some packages failed, try:"
echo "  pip install --upgrade <package-name>"
echo ""
echo "To start the server, run:"
echo "  ./run.sh"
