#!/bin/bash


while IFS= read -r line || [[ -n "$line" ]]; do
    # Debugging: Print the raw line
    echo "Raw Line: $line"

    # Skip empty lines or lines that don't contain ':'
    [[ -z "$line" || "$line" != *:* ]] && continue

    # Extract the key and value
    key=$(echo "$line" | cut -d':' -f1 | tr -d ' ')
    value=$(echo "$line" | cut -d':' -f2- | tr -d ' ' | tr -d '"')

    # Debugging: Print the key and value
    echo "Key: $key, Value: $value"

    # Assign the values to corresponding variables
    case "$key" in
        CLIENT_ID) client_id="$value" ;;
        CLIENT_SECRET) client_secret="$value" ;;
        USERNAME) bot_username="$value" ;;
        PASSWORD) bot_password="$value" ;;
        USER_AGENT) bot_user_agent="$value" ;;
        MASTER_USERNAME) bot_master="$value" ;;
        CACHE_DB_NAME) cache_db=$(echo "$value" | cut -d'=' -f2) ;;
    esac
done < "config.txt"

python run_bot.py <<EOF
$client_id 
$client_secret 
$bot_username
$bot_password 
$bot_user_agent 
$bot_master 
$cache_db
EOF

