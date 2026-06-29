import urllib.request, json
req = urllib.request.Request('http://localhost:8000/predict', data=b'{"prompt":"hello"}', headers={'Content-Type': 'application/json'})
res = urllib.request.urlopen(req)
print('trace_id:', json.loads(res.read()).get('trace_id'))
