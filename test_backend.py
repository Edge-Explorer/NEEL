#!/usr/bin/env python3
"""
Test script to verify the backend can be imported and started correctly.
Run this locally to test if there are any import errors.
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("NEEL Backend Import Test")
print("=" * 60)

print(f"\nPython version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path[:3]}")

try:
    print("\n1. Testing backend.main import...")
    from backend.main import app
    print("   ✅ backend.main imported successfully")
    
    print("\n2. Checking FastAPI app...")
    print(f"   App title: {app.title}")
    print(f"   App version: {app.version}")
    
    print("\n3. Checking routes...")
    routes = [r.path for r in app.routes if hasattr(r, 'path')]
    print(f"   Total routes: {len(routes)}")
    print(f"   Sample routes: {routes[:10]}")
    
    # Check for specific routes
    auth_routes = [r for r in routes if '/api/auth' in r]
    print(f"\n4. Auth routes found: {len(auth_routes)}")
    for route in auth_routes:
        print(f"   - {route}")
    
    print("\n✅ All tests passed! Backend should work on Render.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
