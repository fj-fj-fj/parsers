#!/bin/bash
# require jq (apt install jq)
# Usage:
#   script <N>
#   where N is the key in ./parsers/parsers/user_parsers/youtube/playlists


PLAYLIST_KEY=.\"$1\"
DESTINATION_KEY=.\"$1'_mv_to'\"
PLAYLIST__KEY_N__VALUE_ID="$PROJECT_DIR"/parsers/user_parsers/youtube/playlists
PLAYLIST_ID=$(jq -r "$PLAYLIST_KEY" "$PLAYLIST__KEY_N__VALUE_ID")
SOURCES="$PROJECT_DIR"/data/youtube/"$PLAYLIST_ID"
DESTINATION_DIR=$(jq -r "$DESTINATION_KEY" "$PLAYLIST__KEY_N__VALUE_ID")

mv "$SOURCES"/* "$DESTINATION_DIR"
echo 'https://www.youtube.com/playlist?list='"$PLAYLIST_ID" > "$DESTINATION_DIR"url.txt

ls "$DESTINATION_DIR"
