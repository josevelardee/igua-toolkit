#include <Wire.h>
#include "U8glib.h"  

int pos_up;
int pos_dw;
int display = 1;  
int x = 0;
int size_def=31;
int data [31];
int size_array;
int y_1 = 15;
int y_2 = 35;
int x_in = 6;
int x_dif= 6;
int t=0;


U8GLIB_ST7920_128X64_1X u8g(6, 5, 4 ,7); //Enable, RW, RS, RESET  

void u8g_prepare() 
{  
  u8g.setFont(u8g_font_6x10);  
  u8g.setFontRefHeightExtendedText();  
  u8g.setDefaultForegroundColor();  
  u8g.setFontPosTop();  
}  
   
void u8g_Tela1() 
{
/*  
pos_up=6;

   for (int i=1; i < 20 ; i++){
    if (i<20) {
    u8g.setPrintPos(pos_up, 15);
    u8g.print(char(data[i]));
    }
    pos_up=pos_up+6;
   }

*/

pos_up=x_in;
pos_dw=x_in;

size_array=sizeof(data)/ sizeof(int);

 if ((data[0]>1)&&(size_array==size_def)){

   for (int i=1; i < size_array ; i++){

    t=i+((size_array)/2) - 1;
    
    if (i<(size_array)/2) {
    u8g.setPrintPos(pos_up, y_1);
    u8g.print(char(data[i]));
    }

    if (t<=size_def) {
    
    u8g.setPrintPos(pos_dw, y_2);
    u8g.print(char(data[t]));
    //Serial.print(char(data[t]));
    }
    
    pos_dw=pos_dw+x_dif;
    pos_up=pos_up+x_dif;
     
   }
  }



}  

void draw() //Rotina Desenho  
{
  u8g_prepare();  
  switch(display) //Carrega a tela correspondente  
  {
   case 1:  
    u8g_Tela1();  
    break;  
  }  
} 

void setup()
{
  Wire.begin(5);                // join i2c bus with address #4
  Wire.onReceive(receiveEvent); // register event
  //Serial.begin(9600);           // start serial for output
  u8g.setFont(u8g_font_unifont);  
}



void loop()
{
   u8g.firstPage();   
    do 
    {  
    draw();  
    } 
    while( u8g.nextPage() );  
   
  delay(100);
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany)
{
  while(0 < Wire.available()) // loop through all but the last
  {
   int c = Wire.read(); // receive byte as a character

      if (c==int('&'))
    {x=0;
    //Serial.println("");
    }
    
   
    data[x]=c;
    x++;

  
  }
 


}
