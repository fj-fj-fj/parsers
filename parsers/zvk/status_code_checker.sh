#!/bin/bash
# HTTP responce status code checker
# makes requests use random ip

SELF=$(readlink -f "${BASH_SOURCE[0]}")
BASENAME=$(basename "$SELF")
PARENT_PATH=$(dirname "$SELF")
PARSED_FILE="$PARENT_PATH/data/_parsed_data_default"
PROXIES="$(PWD)/proxies.txt"

echo "$BASENAME is starting ..."

while read -r url
do

ip_address=$(shuf -n 1 "$PROXIES")
status_code=$(curl -LI --header "X-Forwarded-For: $ip_address" $url -o /dev/null -w '%{http_code}\n' -s)

if (( $status_code == 404 )); then
    echo $url >> "$PARENT_PATH/data/404"
fi

echo $status_code $url | sed 's/https:\/\/zvk.ru\/catalog//g'

done < "$PARSED_FILE"

echo "Program finished."
