import requests
urls = [
    "http://localhost:8000/healthz",
    "http://localhost:8000/metrics",
    "http://localhost:9090/-/healthy",
    "http://localhost:3000/api/health",
    "http://localhost:9093/-/healthy",
    "http://localhost:3100/ready",
    "http://localhost:16686/",
    "http://localhost:8888/metrics"
]

for url in urls:
    print(f"Checking {url} ...")
    try:
        r = requests.get(url, timeout=3)
        print(f"  OK {r.status_code}")
    except Exception as e:
        print(f"  ERROR: {e}")
