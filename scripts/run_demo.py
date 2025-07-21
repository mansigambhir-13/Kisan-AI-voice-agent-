#!/usr/bin/env python3
"""
Quick demo runner script
"""

import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from demo_system import main

if __name__ == "__main__":
    print("🚀 Starting Voice Agent Demo...")
    asyncio.run(main())