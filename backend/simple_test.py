#!/usr/bin/env python3
"""
Simple test script to check if Python is working
"""

print("Python is working!")
print("Testing basic imports...")

try:
    import asyncio
    print("✅ asyncio imported successfully")
except ImportError as e:
    print(f"❌ asyncio import failed: {e}")

try:
    import os
    print("✅ os imported successfully")
except ImportError as e:
    print(f"❌ os import failed: {e}")

try:
    import sys
    print("✅ sys imported successfully")
except ImportError as e:
    print(f"❌ sys import failed: {e}")

try:
    from datetime import datetime
    print("✅ datetime imported successfully")
except ImportError as e:
    print(f"❌ datetime import failed: {e}")

try:
    from bson import ObjectId
    print("✅ bson.ObjectId imported successfully")
except ImportError as e:
    print(f"❌ bson.ObjectId import failed: {e}")

print("\nTest completed!") 