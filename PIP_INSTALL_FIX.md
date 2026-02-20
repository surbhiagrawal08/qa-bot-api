# Fix for pip install Issues

## Problem
`pip install -r requirements.txt` doesn't install all packages due to:
- Version conflicts between packages
- Missing dependencies
- Installation order issues
- Compatibility problems

## Solutions

### Solution 1: Use Fixed Installation Script (Recommended)
```bash
./install_fixed.sh
```

This script installs packages in the correct order:
1. Base packages (FastAPI, Pydantic, etc.)
2. LangChain packages
3. Other dependencies
4. Test packages

### Solution 2: Install Packages Individually
If the script fails, install packages one by one:

```bash
source venv/bin/activate

# Base packages
pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 python-multipart==0.0.6
pip install pydantic==2.5.2 python-dotenv==1.0.0

# LangChain (try without strict versions first)
pip install langchain langchain-openai langchain-community langchain-core

# Vector DB and document processing
pip install chromadb==0.4.22 pypdf==3.17.4

# OpenAI
pip install "openai>=1.0.0,<2.0.0" tiktoken

# Testing
pip install pytest==7.4.3 pytest-asyncio==0.21.1 httpx==0.25.2
```

### Solution 3: Use Updated requirements.txt
The `requirements.txt` has been updated with:
- More flexible version ranges
- Missing dependencies added (numpy, typing-extensions)
- Better compatibility

Try installing again:
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Solution 4: Install Without Version Constraints
If version conflicts persist:

```bash
# Remove version pins temporarily
pip install fastapi uvicorn[standard] python-multipart
pip install langchain langchain-openai langchain-community langchain-core
pip install chromadb pypdf openai tiktoken
pip install pydantic python-dotenv
pip install pytest pytest-asyncio httpx
```

### Solution 5: Use Separate Requirements Files
Install from separate files in order:

```bash
pip install -r requirements-base.txt
pip install -r requirements-langchain.txt
pip install -r requirements-other.txt
pip install -r requirements-test.txt
```

## Common Issues and Fixes

### Issue: "No matching distribution found"
**Fix**: Upgrade pip first
```bash
pip install --upgrade pip setuptools wheel
```

### Issue: Version conflicts
**Fix**: Install without version pins or use compatible versions
```bash
pip install langchain --upgrade
```

### Issue: LangChain packages fail
**Fix**: Install core LangChain first, then extensions
```bash
pip install langchain-core
pip install langchain
pip install langchain-openai langchain-community
```

### Issue: ChromaDB installation fails
**Fix**: Install system dependencies first (Linux/Mac)
```bash
# On macOS
brew install cmake

# Then install chromadb
pip install chromadb
```

### Issue: Some packages install but imports fail
**Fix**: Check for missing sub-dependencies
```bash
pip install --upgrade --force-reinstall <package-name>
```

## Verification

After installation, verify with:
```bash
python3 check_imports.py
```

Or check manually:
```bash
python3 -c "import fastapi; import langchain; import chromadb; print('✓ Core packages OK')"
```

## If All Else Fails

1. **Clean reinstall**:
   ```bash
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   ./install_fixed.sh
   ```

2. **Check Python version** (needs 3.8+):
   ```bash
   python3 --version
   ```

3. **Use conda instead**:
   ```bash
   conda create -n zania python=3.9
   conda activate zania
   pip install -r requirements.txt
   ```

## Updated Requirements Structure

The project now has multiple requirements files for better control:
- `requirements.txt` - Main file with all packages
- `requirements-base.txt` - Core web framework packages
- `requirements-langchain.txt` - LangChain packages only
- `requirements-other.txt` - Other dependencies
- `requirements-test.txt` - Testing packages

This allows installing packages in the correct order to avoid dependency conflicts.
