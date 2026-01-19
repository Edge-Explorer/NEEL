import requests
import sys

URL = "https://neel-uo71.onrender.com/"
DOCS = URL + "docs"

def check():
    print(f"Checking NEEL Backend at : {URL}")
    try:
        r = requests.get(URL, timeout=10)
        print(f"Root endpoint: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"✅ Backend is reachable! Version: {data.get('version')}")
            if data.get('version') == "1.0.3":
                print("🌟 SUCCESS: Version 1.0.3 is LIVE!")
            else:
                print(f"⏳ Waiting for version 1.0.3 (Current: {data.get('version')})")
        else:
            print(f"❌ Backend returned error code: {r.status_code}")
            
        d = requests.get(DOCS, timeout=10)
        print(f"Docs endpoint: {d.status_code}")
        
        h = requests.get(URL + "api/health", timeout=10)
        print(f"Health endpoint: {h.status_code}")
        if h.status_code == 200:
            print(f"✅ Health Check PASSED: {h.json()}")
        
    except Exception as e:
        print(f"❌ Failed to reach backend: {str(e)}")

if __name__ == "__main__":
    check()
