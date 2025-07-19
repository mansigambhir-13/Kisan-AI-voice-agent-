#!/usr/bin/env python3
"""
Check API connectivity and configuration
"""

import os
import asyncio
import aiohttp
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from utils.config import ConfigManager

async def check_openai():
    """Check OpenAI API connectivity"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return False, "API key not found"
    
    try:
        import openai
        openai.api_key = api_key
        
        response = await openai.Model.alist()
        return True, "Connected successfully"
    except Exception as e:
        return False, f"Error: {e}"

async def check_elevenlabs():
    """Check ElevenLabs API connectivity"""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        return False, "API key not found"
    
    try:
        async with aiohttp.ClientSession() as session:
            headers = {"xi-api-key": api_key}
            async with session.get("https://api.elevenlabs.io/v1/voices", headers=headers) as response:
                if response.status == 200:
                    return True, "Connected successfully"
                else:
                    return False, f"HTTP {response.status}"
    except Exception as e:
        return False, f"Error: {e}"

async def check_deepgram():
    """Check Deepgram API connectivity"""
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        return False, "API key not found"
    
    try:
        from deepgram import Deepgram
        dg = Deepgram(api_key)
        
        # Simple test - get available models
        response = await dg.models.get_all()
        return True, "Connected successfully"
    except Exception as e:
        return False, f"Error: {e}"

async def main():
    """Main API checker function"""
    print("🔍 Checking API Connectivity...")
    print("=" * 40)
    
    # Load configuration
    try:
        config = ConfigManager()
        print("✅ Configuration loaded successfully")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return
    
    # Check each API
    apis = [
        ("OpenAI", check_openai),
        ("ElevenLabs", check_elevenlabs),
        ("Deepgram", check_deepgram)
    ]
    
    results = []
    for name, check_func in apis:
        print(f"\n🔌 Checking {name}...")
        try:
            success, message = await check_func()
            if success:
                print(f"✅ {name}: {message}")
                results.append((name, True))
            else:
                print(f"❌ {name}: {message}")
                results.append((name, False))
        except Exception as e:
            print(f"❌ {name}: Unexpected error - {e}")
            results.append((name, False))
    
    # Summary
    print(f"\n📊 SUMMARY")
    print("-" * 20)
    working_apis = sum(1 for _, success in results if success)
    total_apis = len(results)
    
    print(f"Working APIs: {working_apis}/{total_apis}")
    
    if working_apis == total_apis:
        print("🎉 All APIs working! Ready for production system.")
    elif working_apis > 0:
        print("⚠️  Some APIs working. System will use fallback modes for missing APIs.")
    else:
        print("❌ No APIs working. System will run in full demo mode.")
    
    print(f"\n💡 To run:")
    print(f"   Full system: python src/main_system.py")
    print(f"   Demo mode: python src/demo_system.py")

if __name__ == "__main__":
    asyncio.run(main())