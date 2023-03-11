#!/bin/env python3

import os
import requests
import subprocess

requests.packages.urllib3.disable_warnings()

res = requests.get("https://google.com", verify=False)
last_url = res.history[-1].url

for h in res.history:
    print(h.url)

if "https://google.com" in last_url:
    print("Has Internet Access!")
    exit(0)

login_script = f"{os.getcwd()}/main.py"
p = subprocess.Popen(login_script, stdout=subprocess.PIPE, shell=True)
stdout,_ = p.communicate()
print(stdout.decode())
