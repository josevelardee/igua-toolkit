#include <Wire.h>
#include <LiquidCrystal.h>
#include "U8glib.h"

U8GLIB_ST7920_128X64_1X u8g(8, 9, 10, 11, 4, 5, 6, 7, 1, 2, 3);   // 8Bit Com: D0..D7: 8,9,10,11,4,5,6,7 en=1, di=2,rw=3

int data [4];
int yPos = 0;

int x = 0;
int flag=0;
int suma= 0;
int saldo=0;
int a=0;
//LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

void setup() {                                 

Serial.begin(9600);
u8g.setFont(u8g_font_unifont);
u8g.setColorIndex(1);                
Wire.begin(0x05);                          
Wire.onReceive(receiveData);               //callback for i2c. Jump to void recieveData() function when pi sends data
//lcd.begin(16, 2);
//lcd.clear();
}

void loop() {
  // picture loop
  u8g.firstPage();  
  do {
    draw();
  } while( u8g.nextPage() );

   // if(data[0]==0){
   //   a=1
   //   delay(100);
   //   x=0;
   //   }

    if(yPos < 83){
    // if it's too slow, you could increment y by a greater number
    yPos++;  }
  else{
    // When the yPos is off the screen, reset to 0.
    yPos = 0;
  }  
      
  // rebuild the picture after some delay
  delay(1000);
}


void draw (void) {
 
 u8g.drawStr( 0, yPos, "Hello World"); 


}

void receiveData(int byteCount) { 

   while(Wire.available()) {               //Wire.available() returns the number of bytes available for retrieval with Wire.read(). Or it returns TRUE for values >0.
       data[x]=Wire.read();
       x++;
     }
  
}


