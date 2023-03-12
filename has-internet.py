#!/bin/env python3

import os
import requests
import subprocess
from datetime import datetime

requests.packages.urllib3.disable_warnings()

res = requests.get("https://google.com", verify=False)
last_url = res.history[-1].url

if "https://myits-app.its.ac.id/internet" not in last_url:
    exit(0)

print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]")
print("Requesting internet access...")

for h in res.history:
    print(h.url)

login_script = f"{os.getcwd()}/main.py"
p = subprocess.Popen(login_script, stdout=subprocess.PIPE, shell=True)
# stdout,_ = p.communicate()
# print(stdout.decode())
