import subprocess
import time
import urllib.request
import json

print("Step 1: kill app container")
subprocess.run(["docker", "stop", "day23-app"], check=True)

print("Step 2: wait 90s for ServiceDown alert to fire")
for i in range(1, 19):
    time.sleep(5)
    try:
        req = urllib.request.Request("http://localhost:9093/api/v2/alerts")
        with urllib.request.urlopen(req) as res:
            alerts = json.loads(res.read())
            active_count = sum(1 for a in alerts if a.get("state") == "active")
            if active_count > 0:
                print(f"  alert fired (after {i*5}s)")
                break
    except Exception as e:
        print(e)
    print(f"  no alert yet ({i*5}s)")

print("Step 3: restart app")
subprocess.run(["docker", "start", "day23-app"], check=True)

print("Step 4: wait 60s for alert to resolve")
for i in range(1, 13):
    time.sleep(5)
    try:
        req = urllib.request.Request("http://localhost:9093/api/v2/alerts")
        with urllib.request.urlopen(req) as res:
            alerts = json.loads(res.read())
            active_count = sum(1 for a in alerts if a.get("state") == "active")
            if active_count == 0:
                print("  alert resolved")
                exit(0)
    except Exception as e:
        print(e)

print("alert did not resolve within 60s")
exit(1)
