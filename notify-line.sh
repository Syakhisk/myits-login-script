#!/bin/env bash

TOKEN="----------"
IP="$(hostname --ip-address)"
LAST_IP="$([[ -f /tmp/last_ip ]] && cat /tmp/last_ip || echo)"

if [[ "$LAST_IP" != "$IP" ]]; then
        python3 /root/myits-login-script/main.py

        # notification
        curl -v \
                -X POST \
                -H "Authorization: Bearer $TOKEN" \
                -F "message=IP changed from $LAST_IP to $IP" \
                https://notify-api.line.me/api/notify
fi

echo "$IP" > /tmp/last_ip
