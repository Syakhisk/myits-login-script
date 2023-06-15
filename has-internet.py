#!/bin/env python3

import os
import requests
import subprocess
from datetime import datetime

requests.packages.urllib3.disable_warnings()

script_path=os.path.dirname(os.path.realpath(__file__))

res = requests.get("https://google.com", verify=False)
last_url = res.history[-1].url

if last_url.startswith("https://google.com"):
    exit(0)

print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]")
print("Requesting internet access...")

for h in res.history:
    print(h.url)

login_script = f"cd {script_path} && ./main.py"
p = subprocess.Popen(login_script, stdout=subprocess.PIPE, shell=True)
