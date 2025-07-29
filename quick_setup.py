#!/usr/bin/env python3
"""
Quick Setup Script for Voice Agent System
Installs dependencies and runs basic tests
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detected. Python 3.8+ required.")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_basic_deps():
    """Install basic dependencies"""
    basic_deps = [
        "pydantic>=2.0.0",
        "aiohttp>=3.8.0", 
        "aiofiles>=23.0.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.0",
        "asyncio"
    ]
    
    for dep in basic_deps:
        if not run_command(f"pip install {dep}", f"Installing {dep}"):
            return False
    
    return True

def create_directories():
    """Create necessary directories"""
    dirs = [
        "data/output/audio_files",
        "data/output/call_logs", 
        "data/output/reports",
        "data/temp",
        "demo_output/audio_files",
        "demo_output/call_logs",
        "demo_output/reports",
        "demo_output/temp"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("✅ Created necessary directories")
    return True

def test_imports():
    """Test basic system imports"""
    print("🧪 Testing system imports...")
    
    test_script = '''
import sys
sys.path.append("src")

try:
    from models.data_models import FarmerProfile, EducationLevel, IncomeLevel
    print("✅ Data models imported")
except Exception as e:
    print(f"❌ Data models failed: {e}")

try:
    from utils.helpers import generate_call_id
    print("✅ Helper utilities imported")
except Exception as e:
    print(f"❌ Helper utilities failed: {e}")

try:
    from components.audio_processor import AudioProcessor
    print("✅ Audio processor imported")
except Exception as e:
    print(f"❌ Audio processor failed: {e}")
'''
    
    try:
        exec(test_script)
        return True
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not Path(".env").exists():
        print("📝 Creating .env file from template...")
        try:
            with open(".env.example", "r") as src:
                content = src.read()
            
            with open(".env", "w") as dst:
                dst.write(content)
            
            print("✅ .env file created from template")
            print("⚠️  Please add your API keys to .env file")
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("✅ .env file already exists")
    
    return True

def main():
    """Main setup function"""
    print("🚀 Voice Agent System - Quick Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install basic dependencies
    if not install_basic_deps():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("❌ Failed to create directories")
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        print("❌ Failed to setup environment")
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        print("❌ Import tests failed")
        sys.exit(1)
    
    print("\n🎉 Quick setup completed successfully!")
    print("=" * 50)
    print("Next steps:")
    print("1. Add your API keys to .env file")
    print("2. Run: python3 demo_voice_system.py")
    print("3. Or run: python3 src/main_voice_system.py")
    print("\nFor mock mode (no API keys needed):")
    print("   python3 demo_voice_system.py")

if __name__ == "__main__":
    main()