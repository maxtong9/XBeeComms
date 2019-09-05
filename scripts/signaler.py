import RPi.GPIO as GPIO
import time
import threading


class Signaler(threading.Thread):
    def GPIOSetup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.potpin_, GPIO.OUT)
        #GPIO.setup(self.potpin_, GPIO.IN)
    def __init__(self, potpin):
        self.potpin_ = potpin
        self.GPIOSetup()
        self.pin_state_ = GPIO.input(self.potpin_)
        self.currentThread_ = None
        self.ledOff() # Assure LED in OFF state at start
        self.packetRecvd_ = False
        #Start Probing
        self.probe_thread_ = threading.Thread(target=self.probe_packets, daemon=True)
        self.probe_thread_.start()

    def ledOn(self):
        GPIO.output(self.potpin_, GPIO.HIGH)
    
    def ledOff(self):
        GPIO.output(self.potpin_, GPIO.LOW)
    
    def createThread(self):
        self.currentThread_ = threading.Thread(target=self.five_sec_probe, daemon=True)
        self.currentThread_.start()
    
    def enforcePacketRec(self):
        self.ledOn()
        self.packetRecvd_ = True

    def five_sec_probe(self):
        print("5 sec probe")
        time.sleep(3) # Give 1 sec leeway to receive a packet
        if self.packetRecvd_:
            self.packetRecvd_ = False
        else:
            self.ledOff()
            print("LED TURNED OFF")
   
    def probe_packets(self):
        while True:
            print("probing_packet thread creation")
            self.createThread()
            self.currentThread_.join() 



