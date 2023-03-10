#!/bin/env python3

import os
import requests
import subprocess

res = requests.get("https://google.com")
last_url = res.history[-1].url

if "https://google.com" not in last_url:
    print("Has Internet Access!")
    exit(0)

login_script = f"{os.getcwd()}/main.py"
p = subprocess.Popen(login_script, stdout=subprocess.PIPE, shell=True)
stdout,_ = p.communicate()
print(stdout.decode())
