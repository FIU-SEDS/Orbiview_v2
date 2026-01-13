#include <Arduino.h>
#include <Wire.h>

void setup() {
  // put your setup code here, to run once:
  Serial1.begin(115200); // Initializing Serial communication
  delay(1000);
  Serial1.println("AT+MODE=0");
  delay(1000);
  Serial1.println("AT+NETWORKID=8");
  delay(1000);
  Serial1.println("AT+ADDRESS=2"); // transmitter address 1, ground station address 2
  delay(1000);
  Serial1.println("AT+BAND=915000000"); //setting frequency band to 915 MHz
  delay(1000);
  Serial1.println("AT+IPR=115200"); //setting baud rate 
  delay(1000);
}

void loop() {
  delay(1000);
  Serial1.println("AT+SEND=1,2,HI");
  delay(1000);
}
