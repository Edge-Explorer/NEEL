import requests

URL = "https://neel-uo71.onrender.com/"

print(f"Checking {URL} phase...")
try:
    r = requests.get(URL, timeout=10)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"Version: {data.get('version')}")
        print(f"Message: {data.get('message')}")
    else:
        print(f"Body: {r.text[:100]}")
except Exception as e:
    print(f"Error: {e}")