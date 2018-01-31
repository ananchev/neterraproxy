#!/usr/bin/python
#saved as greeting-client.py
import time
import requests
import urllib3
urllib3.disable_warnings()

start = time.time()
r = requests.get("https://e-fibank.bg/EBank/")
print(r.text).encode('utf-8')
end = time.time()
print(end - start)
