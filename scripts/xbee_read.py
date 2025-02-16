from digi.xbee.devices import XBeeDevice
from hexdump import hexdump
import time, sys
import RPi.GPIO as GPIO
from signaler import Signaler

#Receiver Setup
default_port = "/dev/ttyUSB0"
baud_rate    = 9600
logfile      = "/home/pi/logfile.csv"
#Pin Light Indicator Setup
#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

#Initialize System Level Args
if len(sys.argv) < 2:
    output_log = logfile
    xbee_port = default_port
elif len(sys.argv) < 3:
    output_log = sys.argv[1]
    xbee_port = default_port
else:
    output_log = sys.argv[1]
    xbee_port = sys.argv[2]


# Decide if Left Light or Right light
print("xbee_port:", xbee_port, "\n")
if xbee_port[-1] is "0":
    print("USB 0, potpin 17")
    # Pin = 17
    potpin = 17
else:
    print("USB 1, potpin 18")
    # Pin = 18
    potpin = 18
signaler = Signaler(potpin)

#GPIO.setup(potpin, GPIO.OUT)

# Turns on the LED Light
def ledOn():
    GPIO.output(potpin, GPIO.HIGH)
# Turns off the LED Light
def ledOff():
    GPIO.output(potpin, GPIO.LOW)

def log(msg, rssi, output_log):
    signaler.enforcePacketRec()
    lf = open(output_log, "a")
    lf.write("{}, {}, {}\n".format(time.time(), msg.data.decode(), rssi.hex()))
    lf.close()

def main():
    device = XBeeDevice(xbee_port, baud_rate)
    if device.open():
        print("ERROR. DEVICE DID NOT OPEN")
    num = 0
    #signaler.ledOff() #TO assure that it is not left on from the last run
    while True:
        try:
            # Returns an object
            # .remote_device
            # .data
            # .is_broadcast
            # .timestamp
            xbee_msg = device.read_data()
            if (xbee_msg):
                remote_device = xbee_msg.remote_device
                data          = xbee_msg.data
                
                # We also want RSSI info
                rssi = device.get_parameter("DB")
                
                log(xbee_msg, rssi, output_log)
                
                # DEBUG
                '''
                print("Received: {}\nFrom: {}".format(data, remote_device))
                hexdump(data)
                print("RSSI: {}".format(rssi))
                hexdump(rssi)
                print("\n")
                '''
                print("received \n")
        except KeyboardInterrupt:
            print("KeyboardInterrupt..... ")
            break
            
        
    device.close()
    signaler.ledOff()


if __name__ == "__main__":
    main()
    signaler.ledOff()
    exit(0)

