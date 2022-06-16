#!/bin/bash

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

#get user data
read -p "Username: " USER
read -s -p "Password: " PASS
echo ""

# UNC_CONTENT="{\"u\":\"${USER}\",\"p\":\"${PASS}\",\"dm\":\"\",\"ps\":\"true\"}"
# CONTENT=$(echo -n $UNC_CONTENT | openssl rsautl -encrypt -pubin -inkey $SCRIPTPATH/pubkey.pem | base64 -w 0 | sed 's/+/%2B/g')
# echo $UNC_CONTENT
# echo $CONTENT
# exit 0

if [ ! -f "${SCRIPTPATH}/cookie.txt" ]; then
  curl -c $SCRIPTPATH/cookie.txt -Ls -o /dev/null -w "" https://id.its.ac.id/internetaccess/auth.php
fi

sleep 1

RESPONSE=$(curl -c $SCRIPTPATH/cookie.txt -b $SCRIPTPATH/cookie.txt -Ls -o /dev/null -w %{url_effective} https://id.its.ac.id/internetaccess/auth.php)

CLIENT_ID=$(echo $RESPONSE | sed -n 's/.*client_id=\([^&]*\).*/\1/p')
SCOPE=$(echo $RESPONSE | sed -n 's/.*scope=\([^&]*\).*/\1/p' | sed 's/+/%2B/g')
STATE=$(echo $RESPONSE | sed -n 's/.*state=\([^&]*\).*/\1/p')
RESPONSE_TYPE=$(echo $RESPONSE | sed -n 's/.*response_type=\([^&]*\).*/\1/p')
PROMPT=""
NONCE=$(echo $RESPONSE | sed -n 's/.*nonce=\([^&]*\).*/\1/p')
PASSWORD_STATE="true"
DEVICE_METHOD=""

UNC_CONTENT="{\"u\":\"${USER}\",\"p\":\"${PASS}\",\"dm\":\"\",\"ps\":\"true\"}"
CONTENT=$(echo -n $UNC_CONTENT | openssl rsautl -encrypt -pubin -inkey $SCRIPTPATH/pubkey.pem | base64 -w 0 | sed 's/+/%2B/g')
#echo -n $CONTENT

sleep 1

curl -v -b $SCRIPTPATH/cookie.txt -L -d "client_id=${CLIENT_ID}" -d "scope=${SCOPE}" -d "state=${STATE}" \
-d "response_type=${RESPONSE_TYPE}" -d "prompt=${PROMPT}" -d "nonce=${NONCE}" -d "password_state=${PASSWORD_STATE}" \
-d "device_method=${DEVICE_METHOD}" -d "content=${CONTENT}" -d "redirect_uri=https%3A%2F%2Fmy.its.ac.id%2Fsso%2Fauth"\
-H "Referer: ${RESPONSE}"\
-c $SCRIPTPATH/cookie.txt $RESPONSE > $SCRIPTPATH/response.txt

if [ $(grep -c "redirect_uri_mismatch" $SCRIPTPATH/response.txt) -ge 1 ]; then
  echo "Failed, Try Again"
elif [ $(grep -c "myITS ID or password is incorrect!" $SCRIPTPATH/response.txt) -ge 1 ]; then
  echo "Failed, Incorrect Password"
elif [ $(grep -c "myITS ID atau kata sandi anda salah!" $SCRIPTPATH/response.txt) -ge 1 ]; then
  echo "Failed, Incorrect Password"
elif [ $(curl -L google.com | grep -c "Selamat datang di Kampus ITS") -ge 1 ]; then
  echo "Failed, Try Again"
else
  echo "Success"
fi

rm $SCRIPTPATH/response.txt
