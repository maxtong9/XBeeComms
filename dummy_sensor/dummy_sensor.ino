#include <Time.h>
#include <TimeLib.h>
#include <SoftwareSerial.h>

#define TEENSY_LED 13
#define MAX_PAYLOAD 16

SoftwareSerial xbee(0, 1);  // RX, TX
int pingPong = 1;

char id = 'A';
unsigned long seq_num = 0;

void setup() {
  // Initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  Serial.println("Teensy started sending bytes via XBee");

  // Set the data rate for the SoftwareSerial port
  xbee.begin(9600);

  // Initialize LED pin as output
  pinMode(TEENSY_LED, OUTPUT);

  randomSeed(analogRead(0));
}

void loop() {
  // Generate random payload value
  float sudo_val = random(50) + ((float)random(9999)/10000);
  /*
   * To parse the time intervals for the XBees, 
   * Choose the time interval you'd like, and include all higher instances
   * (Since they'd be on the same interval, but would be marked higher)
   * Workaround for this would be to use prime numbers, Or choose numbers that aren't multiples
   * 
   */
  // Determine time interval
  int time_int;
  if ((seq_num % 600) == 0) {
    // 60s interval
    time_int = 60000;
  } else if ((seq_num % 300) == 0) {
    // 30s interval
    time_int = 30000;
  } else if ((seq_num % 150) == 0) {
    // 15s interval
    time_int = 15000;
  } else if ((seq_num % 100) == 0) {
    //10s interval
    time_int = 10000;
  } else if ((seq_num % 50) == 0) {
    // 5s interval
    time_int = 5000;
  } else if ((seq_num % 10) == 0) {
    // 1s interval
    time_int = 1000;
  } else {
    // 500ms interval
    time_int = 500;
  }

  // Get current time
  time_t t = now();

  // Print identifier, time interval, sensor value
  xbee.print(id);
  
  xbee.print(",");
  xbee.print(seq_num);
  xbee.print(",");
  xbee.print(time_int);
  xbee.print(",");
  xbee.print(sudo_val,4);
  xbee.print(",");
  xbee.print(t);
  Serial.print(id);
  Serial.print(",");
  Serial.print(seq_num);
  Serial.print(",");
  Serial.print(time_int);
  Serial.print(",");
  Serial.print(sudo_val, 4);
  Serial.print(",");
  Serial.print(t);
  Serial.print("\n");
  seq_num++;
  
  // Flip the LED on Teensy
  if (pingPong == 0) {
    digitalWrite(TEENSY_LED, LOW);
  } else {
    digitalWrite(TEENSY_LED, HIGH);
  }
  pingPong = 1 - pingPong;

  // Delay in between writes for stability
  delay(100);
}
