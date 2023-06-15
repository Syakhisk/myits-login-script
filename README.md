# myITS Login Script and Internet access request

This script can be used for:

- Automating myITS SSO login, will generate a `TVMSESSID` cookie
- Automating [internet access request](https://myits-app.its.ac.id/internet/index.php) when using ITS internal network

## Usage

```
$ python3 main.py
```

or

```
$ ./main.py
```

## Files

### `main.py`
The login script.

### ❗ `secret.txt` ❗
a file containing your myITS username and password, separated by a newline. DO NOT store your password if you don't need to use this script in an **automation**.


### `has-internet.py`

Will try to access `https://google.com` to check the computer has internet access, if it doesn't it will run the `main.py` script.


### TODO

- [ ] Add a more secure way to store the password


## Credit

- [dslite](https://github.com/dslite) for creating a bash script to breakdown the authentication flow.
