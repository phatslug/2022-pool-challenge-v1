import requests
import time

for trial in range(10):
    try:
        requests.get("http://127.0.0.1:8080/kill_me")
        time.sleep(5)
        break
    except:
        print('Server is still running')