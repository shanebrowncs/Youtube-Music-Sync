#!/bin/bash

if [ "$(id -u)" != "0" ]; then
    echo "Root required to install files" 1>&2
    exit 1
fi

cp mp3tags.py /usr/local/bin/mp3tags
cp youtube-sync.py /usr/local/bin/youtube-sync

echo "Youtube-Music-Sync Installed, type \"youtube-sync\" to execute it"
