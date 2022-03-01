import subprocess
from pathlib import Path
import os

proc = subprocess.Popen(
    ["python", "fastapi_app.py"],
    close_fds=True,
    cwd=Path.cwd(),
    stdout=open(os.devnull, 'w'),
    stderr=open(os.devnull, 'w')
)
