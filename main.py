#!/bin/env python3

import json
import requests
import subprocess as sp
from urllib.parse import quote, parse_qsl, urlparse
from base64 import b64decode, b64encode
from getpass import getpass
from os import path

requests.packages.urllib3.disable_warnings()

script_dir = path.dirname(path.realpath(__file__))
secret_path = path.join(script_dir, "secret.txt")
pubkey_path = path.join(script_dir, "pubkey.pem")


def main():
    username, password = get_credentials()

    # Setup a session
    s = requests.Session()

    # Some random "ongko" value, idk what is this but required at the page js script
    random_cookie = quote(
        '{"ongko": "12850820230308011013$bc5dd754ba343195cd29c8025a4a6bc7"}')
    s.cookies.set("_idx", random_cookie)

    # Get initial cookies
    print("--Getting initial cookies--")
    res = s.get("https://myits-app.its.ac.id/internet/auth.php", verify=False)

    error_internal_network = "Akses internet hanya diperbolehkan dari alamat IP internal ITS 10.X.X.X"
    if error_internal_network in res.content.decode():
        log("You're not connected to internal network or make sure VPN is active", "ERROR")
        return

    # Print redirects
    for h in res.history:
        log(h.url, "redirect")

    # Parse query from my its
    # my.its.ac.id/authorize?response_type=....
    raw_queries = urlparse(res.url).query
    queries = parse_qsl(raw_queries)
    print("--Query--")
    print(queries)

    # Possible query params keys
    post_data_keys = [
        "client_id",
        "response_type",
        "scope",
        "state",
        "prompt",
        "redirect_uri",
        "nonce",
        "content",
        "password_state",
        "device_method",
    ]

    # Build post data to be sent
    post_data = {}

    # Build "content" post data from encryption
    raw_content = json.dumps(
        {"u": username, "p": password, "dm": "", "ps": "true"},
        separators=(",", ":"),
    )
    post_data["password_state"] = "true"
    post_data["content"] = encrypt(raw_content)

    # Append query params to post data
    for key in post_data_keys:
        query = list(filter(lambda tup: tup[0] == key, queries))
        if len(query) > 0:
            query = query.pop()
            post_data[key] = query[1]

    print("--Post Data--")
    print(post_data)

    # Login
    res = s.post("https://my.its.ac.id/signin", data=post_data, verify=False)

    for h in res.history:
        log(h.url, "redirect")

    if "redirect_uri_mismatch" in res.content.decode():
        return log("Failed, Try Again", "ERROR")
    if "myITS ID or password is incorrect!" in res.content.decode():
        return log("Incorrect credentials", "ERROR")
    if "myITS ID atau kata sandi anda salah!" in res.content.decode():
        return log("Incorrect credentials", "ERROR")

    # TODO: Check external internet access
    # res = r.get("https://google.com")
    # if "Selamat datang di kampus ITS" in res.content.decode():
    #     return print("Failed geming")

    print("--Login successful--")

    cookies = s.cookies.get_dict()
    print("--Cookies--")
    print(cookies)

    print("--Requesting internet access--")
    res = s.get("https://myits-app.its.ac.id/internet/auth.php", verify=False)

    # Print redirects
    for h in res.history:
        log(h.url, "redirect")


def log(msg, type="Log"):
    print(f"[{str.capitalize(type)}] {msg}\n")


def run(command):
    _out = sp.run(command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    return {
        "returncode": _out.returncode,
        "stdout": _out.stdout.decode().strip(),
        "stderr": _out.stderr.decode().strip(),
    }


def encrypt(data):
    out = run(
        f"echo -n '{data}' | openssl rsautl -encrypt -pubin -inkey {pubkey_path} | base64 -w 0"
    )

    print(f"WARN/ERR ON ENCRYPT FUNCTION: {out['stderr']}\n")

    return out["stdout"]


def decode_pw(str):
    return b64decode(str + b"==").decode().strip()


def encode_pw(str):
    return b64encode(str.encode()).decode().strip()


def get_credentials():
    username = None
    password = None

    if path.exists(secret_path):
        f = open(secret_path, "rb")
        username = (f.readline().strip()).decode()
        password = decode_pw(f.readline().strip())
        f.close()
    else:
        inputUsername = input("Username (NRP): ")
        inputPassword = getpass("Password: ")

        username = inputUsername
        password = inputPassword

        if input("Save password to secret.txt for automation? [y/n]") == "y":
            f = open("secret.txt", "w")
            f.write(username + "\n")
            f.write(encode_pw(password))
            f.close()

    return username, password


if __name__ == "__main__":
    main()
