/*--------------------------------------------------------------------------------------

Serial Read and Display.

This project is designed to Read inputs from Serial and Display the input on a 
Freetronic 32x16 Dot Matrix Display.

To wipe your existing String simply input a Tilda (~) into your Serial Command.

Note, for debugging purposes, Serial.print has been used in both the Stop Display
and Write Display loops. These can be removed.

--------------------------------------------------------------------------------------*/

/*--------------------------------------------------------------------------------------
  Includes
--------------------------------------------------------------------------------------*/
#include <SPI.h>        //SPI.h must be included as DMD is written by SPI (the IDE complains otherwise)
#include <DMD.h>        //
#include <TimerOne.h>   //
#include "SystemFont5x7.h"
#include "Arial_black_16.h"

//Fire up the DMD library as dmd
#define DISPLAYS_ACROSS 3
#define DISPLAYS_DOWN 1
DMD dmd(DISPLAYS_ACROSS, DISPLAYS_DOWN);

char inData[255]; // Allocate some space for the string
char inChar; // Where to store the character read
byte index = 0; // Index into array; where to store the character

void ScanDMD(){ 
    dmd.scanDisplayBySPI();
}

void setup(void){
    Serial.begin(9600);
    Serial.write("Power On");

   //initialize TimerOne's interrupt/CPU usage used to scan and refresh the display
    Timer1.initialize( 5000 );           //period in microseconds to call ScanDMD. Anything longer than 5000 (5ms) and you can see flicker.
    Timer1.attachInterrupt( ScanDMD );   //attach the Timer1 interrupt to ScanDMD which goes to dmd.scanDisplayBySPI()

   //clear/init the DMD pixels held in RAM
   dmd.clearScreen( true );   //true is normal (all pixels off), false is negative (all pixels on)
   dmd.selectFont(Arial_Black_16);
}

void loop(void){
    while(Serial.available() == 0){ //check to see if data on Serial
        if (index > 0){ // if index is greater than 0, data must exist in inData, so display text. Otherwise do nothing.
            display_text();
        }else{
            break;
        }
    }
    while(Serial.available() > 0){
        inChar = Serial.read(); // Read a character
            if (inChar == '~') { // ~ is the command to stop display of any text and to wipe the inData String.
                  cancel_text();
                  break;
            }else{
                  write_text(); // This will write your Serial text to a String. Note if you do not ~ before typing a new string, this will append your new string to the previous one.
                  break;
            }
    }
}

   // Command to Stop Display and wipe InData String/Reset index.
void cancel_text(){
    index = 0;
    *inData = 0;
    Serial.println("Cancel");
}
  // Read Serial and Write to String to be Displayed.
void write_text(){
    inData[index] = inChar; // Store it
    index++; // Increment where to write next
    while(Serial.available() > 0){
         if(index < 254){
              inChar = Serial.read(); // Read a character
              inData[index] = inChar; // Store it
              // delay(200);
              index++; // Increment where to write next
              inData[index] = 0; // Null terminate the string
         }
     }
}

// Scrolling Text the inData string on a 32x16 DMD 
void display_text(){
    // Serial.println(inData);
    // dmd.drawMarquee(inData,index,(32*1)-1,0); // This uses the Freeduino 32x16 DMD
    // dmd.drawString( 0,0, "Hello,", 5, GRAPHICS_NORMAL );
    dmd.drawString( 0,0, inData, 16, GRAPHICS_NORMAL );
    long start=millis();
    long timer=start;
    boolean ret=false;
    delay(100);
  
    /*
    while(!ret){
        if ((timer+30) < millis()) {  //Speed of Marquee Text
             // ret=dmd.stepMarquee(-1,0);
   //          ret=dmd.stepMarquee(-10,0);
             timer=millis();
        }
      
    }
      */
}
