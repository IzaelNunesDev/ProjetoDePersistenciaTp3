#!/usr/bin/env python3
"""
Test script to verify FastAPI application startup
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from main import app
    print("✅ FastAPI application imported successfully!")
    print(f"📝 Application title: {app.title}")
    print(f"📝 Application version: {app.version}")
    print(f"📝 Application description: {app.description}")
    print("🎉 All Pydantic v2 compatibility issues resolved!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1) 