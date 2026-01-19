import requests

URL = "https://neel-uo71.onrender.com/"

try:
    r = requests.get(URL)
    print(f"Status: {r.status_code}")
    print("Headers:")
    for k, v in r.headers.items():
        print(f"  {k}: {v}")
    print(f"Body: {r.text[:200]}")
except Exception as e:
    print(f"Error: {e}")
