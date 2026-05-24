import requests
base = "http://127.0.0.1:8000"
print(requests.get(f"{base}/health", timeout=5).json())
print(requests.get(f"{base}/resolve", params={"q": "Sony"}, timeout=5).json())
