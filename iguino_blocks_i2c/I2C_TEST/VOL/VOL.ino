#include <Wire.h>

#define SLAVE_ADDRESS 0x04

volatile byte leArray[6];
volatile boolean sendStuff;
volatile byte someByte1 = 0x2A;
volatile byte someByte2 = 0x2B;
volatile byte someByte3 = 0x2C;
volatile byte someByte4 = 0x1A;
volatile byte someByte5 = 0x1B;
volatile byte someByte6 = 0x1C;

void setup()
{
  Wire.begin(SLAVE_ADDRESS);    // join i2c
  Wire.onRequest(requestEvent); // register event
}

void loop()
{
  
  fillArray();
  sendStuff = true;
  delay(2000);
}

void fillArray()
{
  leArray[0] = someByte1;
  leArray[1] = someByte2;
  leArray[2] = someByte3;
  leArray[3] = someByte4;

}
void requestEvent()
{  
  /*if(sendStuff)
  {
    Wire.write((byte*)leArray, 4);
  }
  sendStuff= false;
*/
Wire.write(1);

}
