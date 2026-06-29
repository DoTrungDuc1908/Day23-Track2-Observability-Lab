import urllib.request
import json
for _ in range(50):
    try:
        urllib.request.urlopen(urllib.request.Request('http://localhost:8000/predict', json.dumps({'prompt':'hello', 'fail':True}).encode('utf-8'), {'Content-Type': 'application/json'}))
    except Exception:
        pass
