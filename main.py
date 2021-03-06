#!/bin/env python3

import json
import requests as r
from urllib.parse import parse_qs, parse_qsl, urlparse
import subprocess as sp

import config


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
    pubkey_path = "./pubkey.pem"
    out = run(
        f"echo -n '{data}' | openssl rsautl -encrypt -pubin -inkey {pubkey_path} | base64 -w 0"
    )

    if out["stderr"]:
        return None

    return out["stdout"]


def main():
    s = r.Session()
    res = s.get("https://my.its.ac.id")

    for h in res.history:
        log(h.url, "redirect")

    raw_query = urlparse(res.url).query
    query = parse_qsl(raw_query)

    log(raw_query, "query")

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

    post_data = {}
    for pd_key in post_data_keys:
        v = [q[1] for q in query if q[0] == pd_key]
        post_data[pd_key] = v[0] if len(v) else ""

    raw_content = json.dumps(
        {"u": config.username, "p": config.decode_pw(), "dm": "", "ps": "true"},
        separators=(",", ":"),
    )

    content = encrypt(raw_content)

    post_data["password_state"] = "true"
    post_data["content"] = content

    res = s.post("https://my.its.ac.id/signin", data=post_data)

    for h in res.history:
        log(h.url, "redirect")

    log(res.url, "url")

    if "redirect_uri_mismatch" in res.content.decode():
        return log("Failed, Try Again", "ERROR")
    if "myITS ID or password is incorrect!" in res.content.decode():
        return log("Incorrect credentials", "ERROR")
    if "myITS ID atau kata sandi anda salah!" in res.content.decode():
        return log("Incorrect credentials", "ERROR")

    # TODO: Check external internet acces
    # res = r.get("https://google.com")
    # if "Selamat datang di kampus ITS" in res.content.decode():
    #     return print("Failed geming")

    print("Success")

    print("--Data--")
    cookies = s.cookies.get_dict()

    for key in cookies:
        print(f"{key}:{cookies[key]}")
        
    print("")
    log("Copy TVMSESSID cookie value to use the session.")
    log("Writing to ./cookie.txt")
    f = open("./cookie.txt", "w")
    f.write(f"TVMSESSID={cookies['TVMSESSID']}")
    log("Cookie written")
    

if __name__ == "__main__":
    main()
