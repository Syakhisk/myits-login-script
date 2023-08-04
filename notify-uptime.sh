#!/bin/env bash

# Notify uptime using uptime-kuma

IP="$(hostname --ip-address)"
curl -v "https://uptime-pve.up.railway.app/api/push/ESB1uvlcmN?status=up&msg=$IP&ping="
