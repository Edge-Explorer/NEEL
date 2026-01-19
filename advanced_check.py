import requests

URL = "https://neel-uo71.onrender.com/"

print(f"Checking {URL}...")
try:
    # Try GET
    r = requests.get(URL, timeout=10)
    print(f"GET / : {r.status_code}")
    print(f"Server: {r.headers.get('Server')}")
    print(f"Body: {r.text[:50]}")
    
    # Try HEAD
    h = requests.head(URL, timeout=10)
    print(f"HEAD / : {h.status_code}")
    
    # Try Health
    health = requests.get(URL + "api/health", timeout=10)
    print(f"GET /api/health : {health.status_code}")
    if health.status_code == 200:
        print(f"Result: {health.json()}")

except Exception as e:
    print(f"Error: {e}")
