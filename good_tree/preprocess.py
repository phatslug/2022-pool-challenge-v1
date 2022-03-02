import subprocess
import requests
import time

proc = subprocess.Popen(["python", "flask_prep.py"])

while True:
    try:
        time.sleep(1)
        resp = requests.get("http://localhost:5112/started")
        time.sleep(4)
        break
    except Exception as e:
        pass