/*
  I2C Pinouts
  SDA -> A4
  SCL -> A5
*/

//Import the library required
#include <Wire.h>

//Slave Address for the Communication
#define SLAVE_ADDRESS 0x03

#include <Arduino.h>
//#include <SoftwareSerial.h>
//SoftwareSerial mySerial(2,3); // RX, TX
int secondsRemaining = 0;

char number[50];
int numero;
int state = 0;
byte incomingByte;
byte i;

//Code Initialization
void setup() {
  // initialize i2c as slave
  Serial.begin(4800);
  //mySerial.begin(4800);
  Wire.begin(SLAVE_ADDRESS);
  // define callbacks for i2c communication
  //Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
}

void loop(){


delay (100);
  }


void sendData() {


    if (Serial.available()>0) {
      i=Serial.read();
      if (i != 255) {
            Wire.write(i);
            }
    
   } 

}


