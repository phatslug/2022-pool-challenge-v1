import subprocess
from pathlib import Path
import os
import requests
import time

nothing = open(os.devnull, 'w')
proc = subprocess.Popen(
    ["python", "fastapi_app.py"],
    stdout=nothing,
    stderr=nothing
)

for trial in range(10):
    try:
        time.sleep(5)
        requests.get('http://127.0.0.1:8000/szarosapi')
        time.sleep(5)
    except:
        print(f"Server is not running at trial {trial}")
