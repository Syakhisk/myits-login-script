# rename this file to config.py

from base64 import b64decode, b64encode
from getpass import getpass

username = "05311940000003"
password = "-" # run `python config.py` to get value


def decode_pw(str=password):
    return b64decode(str.encode() + b"==").decode().strip()


def encode_pw(str):
    return b64encode(str.encode()).decode().strip()


if __name__ == "__main__":
    input = getpass("Password: ")
    p = encode_pw(input)
    print(p)
    # p = decode_pw(p)
