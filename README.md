# myITS Login Script and Internet access request

This script can be used for:

- Automating myITS SSO login, will generate a `TVMSESSID` cookie
- Automating [internet access request](https://myits-app.its.ac.id/internet/index.php) when using ITS internal network

## Usage

1. Copy `config.sample.py` to `config.py`
2. Run `config.py` and enter the output to password in `config.py`
3. Run `main.py`

## TODO

- [ ] Make script more portable, create one copy-paste-able file
- [ ] Make `config.py` optional

## Credit

- Credit to Suhu [dslite](https://github.com/dslite) for creating the source bash script.
