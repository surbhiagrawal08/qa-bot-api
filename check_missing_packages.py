#!/usr/bin/env python3
"""Script to check which packages from requirements.txt are missing."""
import subprocess
import sys

REQUIRED_PACKAGES = {
    'fastapi': 'fastapi',
    'uvicorn': 'uvicorn',
    'langchain': 'langchain',
    'langchain_openai': 'langchain-openai',
    'langchain_community': 'langchain-community',
    'langchain_core': 'langchain-core',
    'chromadb': 'chromadb',
    'pypdf': 'pypdf',
    'pydantic': 'pydantic',
    'dotenv': 'python-dotenv',
    'pytest': 'pytest',
    'httpx': 'httpx',
    'openai': 'openai',
    'tiktoken': 'tiktoken',
    'numpy': 'numpy',
}

def check_package(module_name, package_name):
    """Check if a package is installed."""
    try:
        __import__(module_name)
        return True, None
    except ImportError as e:
        return False, str(e)

def get_installed_version(package_name):
    """Get installed version of a package."""
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'show', package_name],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith('Version:'):
                    return line.split(':', 1)[1].strip()
        return None
    except Exception:
        return None

def main():
    """Check all required packages."""
    print("🔍 Checking installed packages...")
    print("=" * 60)
    
    missing = []
    installed = []
    errors = []
    
    for module_name, package_name in REQUIRED_PACKAGES.items():
        is_installed, error = check_package(module_name, package_name)
        version = get_installed_version(package_name)
        
        if is_installed:
            status = "✓"
            version_str = f" (v{version})" if version else ""
            print(f"{status} {package_name:30} {version_str}")
            installed.append(package_name)
        else:
            status = "✗"
            print(f"{status} {package_name:30} MISSING")
            missing.append(package_name)
            if error:
                errors.append((package_name, error))
    
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"   Installed: {len(installed)}/{len(REQUIRED_PACKAGES)}")
    print(f"   Missing: {len(missing)}/{len(REQUIRED_PACKAGES)}")
    
    if missing:
        print(f"\n❌ Missing packages:")
        for pkg in missing:
            print(f"   - {pkg}")
        
        print(f"\n💡 To install missing packages, run:")
        print(f"   pip install {' '.join(missing)}")
        print(f"\n   Or use the fixed installation script:")
        print(f"   ./install_fixed.sh")
        
        if errors:
            print(f"\n⚠️  Import errors:")
            for pkg, error in errors:
                print(f"   {pkg}: {error}")
        
        return 1
    else:
        print(f"\n✅ All packages are installed!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
