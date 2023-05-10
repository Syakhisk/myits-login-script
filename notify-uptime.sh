#!/bin/env bash

TOKEN="1zajgP8VFg9Aus6TKyGKx51vzztPQXuS8x24dN2lG0D"
IP="$(hostname --ip-address)"

# notification
curl -v \
	-X POST \
	-H "Authorization: Bearer $TOKEN" \
	-F "message=PROXMOX UPTIME-- IP: $IP -- Date: $(date) -- Uptime: $(uptime -p)" \
	https://notify-api.line.me/api/notify
