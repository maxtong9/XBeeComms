# XBeeComms
 - Passively listens and logs received messages and corresponding RSSI
 - General setup consisted of two XBee modules connected via explorer board to a Raspberry Pi.
   - This Pi was then hooked up to our Drone and served as our receiver in our experiments.
 - We also had 4 Teensy boards on the ground hooked up to an XBee, each through the Teensy Adapter Board.
   - These Teensy boards served as our mock sensors, transmitting through their respective XBees.

## Equipment
- Raspberry Pi (x1)

- Teensy Board (x4)

- XBee3 Module (x6)

- Teensy Adapter Board (x4)

- XBee Explorer Board (x2)

## Hardware Configuration

### XBee3

1. Download and install [Digi XCTU](https://www.digi.com/resources/documentation/digidocs/90001526/tasks/t_download_and_install_xctu.htm?tocpath=Set%20up%20%20your%20XBee%20devices%7CDownload%20and%20install%20XCTU%7C_____0 "Digi's XCTU")

2. Plug your XBee into one of the XBee Explorer modules and plug into your computer via USB.

3. Open XCTU and click *Discover devices*

<img src="https://github.com/rmallensb/XBeeComms/blob/master/images/tutorial/xctu_discover.png" width="300"/>

4. Select the port to be scanned. Then select the settings as shown below:

<img src="https://github.com/rmallensb/XBeeComms/blob/master/images/tutorial/xctu_discover_ports.png" width="300"/>

5. Your device should appear on *Devices discovered* list. Click *Add selected devices*.

<img src="https://github.com/rmallensb/XBeeComms/blob/master/images/tutorial/xctu_add_device.png" width="300"/>

6. With the gear icon selected, click the radio-module on the left and verify that the XBee is running 802.15.4 firmware. Select *Update firmware* and update if necessary.

<img src="https://github.com/rmallensb/XBeeComms/blob/master/images/tutorial/xctu_firmware.png" width="400"/>

7. Now, still with the gear icon selected, you should see a long list of settings on the right.

<img src="https://github.com/rmallensb/XBeeComms/blob/master/images/tutorial/xctu_settings.png" width="500"/>

8. Under *Networking* pick a channel (between 0x0B and 01A) for the XBee radios to communicate over. **Note that all XBees need to be on the same channel.**

9. Again under *Networking*, pick a Network PAN ID. **Note that all XBees need to share the same id.**

10. Optional: You can assign your XBee a name under Node Identifier.

11. For the reading XBee (attached to Pi), scroll down to the *UART Interface* and set API Enable to *API Mode Without Escapes*. For the writing XBee (attached to Teensy), set API Enable to *Transparent Mode*.

12. Click *Write* to save the configuration.

13. Unplug the XBee and repeat steps 2-12 for all other XBee modules.

### Teensy

1. Download and install the [Arduino IDE](https://www.arduino.cc/en/Main/Software "Arduino IDE").

2. Plug in one of your Teensy boards into your computer via USB and open `dummy_sensor.ino` with the Arduino IDE. **Note: Make sure your USB allows for data flow and not just power.**

3. Change `char id = ` to a unique character. **Note: make sure to record which Teensy has which ID so you can tell them apart during analysis.**

4. Under *Tools* verify the following settings and that you select the correct port.

<img src="https://github.com/rmallensb/XBeeComms/blob/master/images/tutorial/teensy_port.png" width="500"/>

5. Compile and upload the code to the Teensy Board.

6. Unplug the Teensy and repeat steps 2-5 for all other Teensy boards.

## Software Configuration

### Requirements
 - python3
 ```
 apt-get install python3
 ```
 - hexdump
 ```
 pip3 install hexdump
 ```
 - digi-xbee
 ```
 pip3 install digi-xbee
 ```

### Setup
#### In xbee_read.py:
 - Alter xbee COM port to correct path
 - Alter baud_rate to desired value
 - Alter logfile in to desired logfile path
#### LED Lights
 - To Run the new scripts with the integrated LED LIGHTS:
 - Connect the lights to GPIO pins 17 and 18
### To Run on Bootup
 - If done with sudo, adding the following line to your `/etc/rc.local` will work
 ```
 bash /home/pi/xbee_scan.sh
 ```
 - If done without sudo, add the following cronjob
 ```
 @reboot bash /home/pi/xbee_scan.sh
 ```
 
 
 ## Notes
 - In order power the Teensy boards in the field, we used external battery packs. However, most battery packs require enough current to prevent them from falling asleep. It was our finding that these Teensy/XBee configurations do not meet this threshold for more battery packs. In order to combat this we would either plug another battery enabled device into the battery pack (if it had multiple ports) or we would plug a Raspberry Pi into the battery pack and use the Pi to forward power to the Teensy/XBee (by plugging the Teensy into the Pi).
