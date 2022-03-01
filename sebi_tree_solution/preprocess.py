import subprocess
from pathlib import Path
import os
import requests
import time

proc = subprocess.Popen(
    ["python", "fastapi_app.py"],
    close_fds=True,
    cwd=Path.cwd(),
    stdout=open(os.devnull, 'w'),
    stderr=open(os.devnull, 'w')
)

for trial in range(100):
    try:
        time.sleep(5)
        requests.get('http://127.0.0.1:8000/szarosapi')
        time.sleep(5)
    except:
        print(f"Server is not running at trial {trial}")
