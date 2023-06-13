from base64 import b64decode, b64encode
from getpass import getpass
from os import path


def decode_pw(str):
    return b64decode(str.encode() + b"==").decode().strip()


def encode_pw(str):
    return b64encode(str.encode()).decode().strip()


def main():
    # check if secret.txt exists in script directory
    # if not create them

    inputUsername = input("Username (NRP): ")
    inputPassword = getpass("Password: ")

    print("Username: " + inputUsername)
    print("Password: " + encode_pw(inputPassword))


if __name__ == "__main__":
    main()


# if __name__ == "__main__":
#     input = getpass("Password: ")
#     p = encode_pw(input)
#     print(p)
