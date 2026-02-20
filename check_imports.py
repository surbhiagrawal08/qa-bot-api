#!/usr/bin/env python3
"""Script to check for import issues without installing all dependencies."""
import sys

def check_imports():
    """Check if all required modules can be imported."""
    errors = []
    
    # Check standard library imports
    try:
        import json
        import os
        import tempfile
        print("✓ Standard library imports OK")
    except ImportError as e:
        errors.append(f"Standard library: {e}")
    
    # Check third-party imports
    modules_to_check = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "uvicorn"),
        ("langchain", "langchain"),
        ("langchain_openai", "langchain_openai"),
        ("langchain_community", "langchain_community"),
        ("chromadb", "chromadb"),
        ("pypdf", "pypdf"),
        ("pydantic", "pydantic"),
        ("dotenv", "python-dotenv"),
    ]
    
    missing = []
    for module_name, package_name in modules_to_check:
        try:
            __import__(module_name)
            print(f"✓ {package_name} OK")
        except ImportError:
            missing.append(package_name)
            print(f"✗ {package_name} NOT FOUND")
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return 1
    else:
        print("\n✅ All imports successful!")
        return 0

if __name__ == "__main__":
    sys.exit(check_imports())
