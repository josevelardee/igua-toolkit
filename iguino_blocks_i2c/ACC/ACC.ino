#include <Arduino.h>
#include <SoftwareSerial.h>

SoftwareSerial mySerial(2,3); // RX, TX

int secondsRemaining = 0;
void setup() {
    // Open serial communications and wait for port to open:
    Serial.begin(4800);
 //   Serial.println("Coin Acceptor Ready!");

    // set the data rate for the SoftwareSerial port
    //mySerial.begin(4800);

    pinMode(13, OUTPUT);

    }

void loop() {
    byte i;
    unsigned long lastMillis = millis();

   
        // any input coming from coin acceptor?
        if (Serial.available()) {
            // read input, which is a 1 byte integer
            i=Serial.read();
            // ignore any 255 amounts
            if (i != 255) {
                // increment time based on coin amount
                secondsRemaining = secondsRemaining + i * 60;
                //Serial.print("Received ammount is ");
                Serial.print(i);
                //Serial.println(" peruvian nuevos soles... ");
                }
            }
        if ((millis() - lastMillis) > 1000UL) {
            // decrement the time remaining by 1 sec
            lastMillis = millis();
            if (secondsRemaining > 0) {
                secondsRemaining = secondsRemaining - 1;
                }
            if (secondsRemaining > 0)
                digitalWrite(13, HIGH);
            else
                digitalWrite(13, LOW);
            // Serial.print("Time is ");
            // Serial.print(secondsRemaining);
            // Serial.println(" remaining");
            }
        } // while

    }
