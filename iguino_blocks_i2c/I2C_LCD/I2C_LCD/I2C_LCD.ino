/*
  LiquidCrystal Library - Serial Input
 Demonstrates the use a 16x2 LCD display.  The LiquidCrystal
 library works with all LCD displays that are compatible with the
 Hitachi HD44780 driver. There are many of them out there, and you
 can usually tell them by the 16-pin interface.
 This sketch displays text sent over the serial port
 (e.g. from the Serial Monitor) on an attached LCD.
 The circuit:
 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to ground
 * 10K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)
 Library originally added 18 Apr 2008
 by David A. Mellis
 library modified 5 Jul 2009
 by Limor Fried (http://www.ladyada.net)
 example added 9 Jul 2009
 by Tom Igoe
 modified 22 Nov 2010
 by Tom Igoe
 modified 7 Nov 2016
 by Arturo Guadalupi
 This example code is in the public domain.
 http://www.arduino.cc/en/Tutorial/LiquidCrystalSerialDisplay
*/

// include the library code:
#include <LiquidCrystal.h>
#include <Wire.h>

//Slave Address for the Communication
#define SLAVE_ADDRESS 0x05

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to

LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

char mensaje;
int number=8;
char number2[50];

String stringOne;
int state = 0;
volatile boolean sendStuff;
String a;

void setup() {
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // initialize the serial communications:
  Serial.begin(9600);
   Wire.begin(SLAVE_ADDRESS);
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  lcd.clear();
}

void loop() {


switch (number) {
  case 0:
     lcd.clear();
     lcd.setCursor(0, 0);
     lcd.print("mAs agua pura...");
     lcd.setCursor(0, 2);
     lcd.print("para Todos!!!");
     break;
  case 1:
     lcd.clear();
     lcd.setCursor(0, 0);
     lcd.print("cuida tu salud..");
     lcd.setCursor(0, 2);
     lcd.print("y la del planeta!");
     break;
   case 2:
     lcd.clear();
     lcd.setCursor(0, 0);
     lcd.print("mejor agua y...");
     lcd.setCursor(0, 2);
     lcd.print("menos plAstico");
     break;
  case 3:
     lcd.clear();
     lcd.setCursor(0, 0);
     lcd.print("f/aguaigua");
     lcd.setCursor(0, 2);
     lcd.print("http://igua.pe");
     break;
  case 4:
     lcd.clear();
     lcd.setCursor(0, 0);
     lcd.print("Hola mundo!!");
     lcd.setCursor(0, 2);
     lcd.print("Hola igua!!");
     break;
  case 5:
     lcd.clear();
     lcd.setCursor(0, 0);
     lcd.print("agua igua,");
     lcd.setCursor(0, 2);
     lcd.print("salud!");
     break;
  default:
   lcd.clear();
   lcd.setCursor(0, 0);
   lcd.print("HOLI...");

}



delay (100);

} // end loop


void receiveData(int byteCount) {

int i = 0;
  while (Wire.available()) {
    number = Wire.read();
  }
  Serial.print(number);
 lcd.print(number);
  
}
