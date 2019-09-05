#!/bin/bash

cd "/home/pi"
#sleep 30

FOLDER="XBEE_SCAN"
i=0
while [[ -d "$FOLDER-$i" ]] ; do
    let i++
done
FOLDER="$FOLDER-$i"
mkdir $FOLDER

python3 /home/pi/xbee_read.py "$FOLDER/xbee.csv" &

echo "Starting Drone Logger $FOLDER"
