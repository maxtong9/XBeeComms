#!/bin/bash

cd "/home/pi"

#Create the new folder
FOLDER="XBEE_SCAN"
i=0
while [[ -d "$FOLDER-$i" ]] ; do
	let i++
done
FOLDER="$FOLDER-$i"
mkdir $FOLDER

ls -l /dev/serial/by-id > "$FOLDERdevice_names.log"
#Start the Python scripts for the receivers
python3 ~/digi_xbee/xbee_read.py "$FOLDER/xbee0.csv" "/dev/ttyUSB0"&
python3 ~/digi_xbee/xbee_read.py "$FOLDER/xbee1.csv" "/dev/ttyUSB1"&

echo "Starting Drone Logger $FOLDER"
killall -9 telemetry-saver
~/DroneSDK/build/bin/telemetry-saver "UserConfig.txt" "$FOLDER/drone.log"&

