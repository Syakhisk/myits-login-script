#!/bin/env bash

TOKEN="1zajgP8VFg9Aus6TKyGKx51vzztPQXuS8x24dN2lG0D"
IP="$(hostname --ip-address)"
LAST_IP="$([[ -f /tmp/last_ip ]] && cat /tmp/last_ip || echo)"

echo "LAST_IP=$LAST_IP"

if [[ "$LAST_IP" != "$IP" ]]; then
	cd /root/myits-login-script
        python3 main.py

        # notification
        curl -v \
                -X POST \
                -H "Authorization: Bearer $TOKEN" \
                -F "message=IP changed from $LAST_IP to $IP" \
                https://notify-api.line.me/api/notify
fi

echo "$IP" > /tmp/last_ip
