from digi.xbee.devices import XBeeDevice
from hexdump import hexdump
import time, sys

default_port = "/dev/ttyUSB0"
baud_rate    = 9600
logfile      = "/home/pi/logfile.csv"

def log(msg, rssi, output_log):

    lf = open(output_log, "a")
    lf.write("{}, {}, {}\n".format(time.time(), msg.data.decode(), rssi.hex()))
    lf.close()

def main():
    if len(sys.argv) < 2:
        output_log = logfile
        xbee_port  = default_port
    elif len(sys.argv) < 3:
        output_log = sys.argv[1]
        xbee_port  = default_port
    else:
        output_log = sys.argv[1]
        xbee_port  = sys.argv[2]

    device = XBeeDevice(xbee_port, baud_rate)
    device.open()

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

                '''
                # DEBUG
                print("Received: {}\nFrom: {}".format(data, remote_device))
                hexdump(data)
                print("RSSI: {}".format(rssi))
                hexdump(rssi)
                print("\n")
                '''

        except KeyboardInterrupt:
            break

    device.close()


if __name__ == "__main__":
    main()
