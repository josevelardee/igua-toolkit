/*  
GraphicsTest.pde  
>>> Before compiling: Please remove comment from the constructor of the   
>>> connected graphics display (see below).  
  
Universal 8bit Graphics Library, http://code.google.com/p/u8glib/  
  
Copyright (c) 2012, olikraus@gmail.com  
All rights reserved.  
 
Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions 
are met:  
 
* Redistributions of source code must retain the above copyright notice, 
  this list of conditions and the following disclaimer.  
     
* Redistributions in binary form must reproduce the above copyright 
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.  
  
  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND   
  CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,   
  INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF   
  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE   
  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR   
  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,   
  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT   
  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;   
  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER   
  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,   
  STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)   
  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF   
  ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.   
*/  
   
#include "U8glib.h"  
#include <Wire.h>
// A linha abaixo define as ligacoes e deve ser 
// ajustada conforme o display utilizado. 
U8GLIB_ST7920_128X64_1X u8g(6, 5, 4 ,7); //Enable, RW, RS, RESET  

int data [4];
int display = 1;  
int x = 0;
int flag=0;
int suma= 0;
int saldo=0;
int litros_p1=0;
int litros_p2=0;
int dis_l1=0;
int dis_l2=0;
int segundos=0;
const unsigned char rook_bitmap[] PROGMEM = {

   0x00, 0x00, 0x00, 0x00, 0xe0, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xfe, 0x3f, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80,
   0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0xc0, 0xff, 0xff, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf0, 0xff, 0xff, 0x03, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf8,
   0xff, 0xff, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0xf8, 0x0f, 0xf8, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xfc, 0x03, 0xf0, 0x1f, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xfe,
   0x01, 0xc0, 0x1f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0xfe, 0x00, 0xc0, 0x3f, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7f, 0x00, 0x80, 0x3f, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7f,
   0x00, 0x00, 0x3f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x3f, 0x00, 0x00, 0x7f, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f, 0x00, 0x00, 0x7f, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f,
   0x00, 0x00, 0x3e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x1c, 0x00, 0x00, 0x3e, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1e, 0x00, 0xfe, 0x07, 0x7c,
   0x00, 0x07, 0x80, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3e,
   0x80, 0xff, 0x1f, 0x7c, 0x80, 0x0f, 0xc0, 0x07, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x3f, 0xe0, 0xff, 0x3f, 0xfe, 0x80, 0x0f, 0xc0, 0x07,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f, 0xf0, 0xff, 0x7f, 0xfe,
   0x80, 0x0f, 0xe0, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f,
   0xf8, 0xff, 0x7f, 0xfe, 0x80, 0x0f, 0xe0, 0x0f, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x3f, 0xf8, 0xff, 0x7f, 0xfe, 0x80, 0x0f, 0xf0, 0x1f,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f, 0xfc, 0x07, 0x7e, 0xfe,
   0x80, 0x0f, 0xf0, 0x1f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f,
   0xfc, 0x01, 0x3c, 0xfe, 0x80, 0x0f, 0xf8, 0x3f, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x3f, 0xfe, 0x00, 0x00, 0xfe, 0x80, 0x0f, 0xf8, 0x3f,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f, 0xfe, 0x00, 0x00, 0xfe,
   0x80, 0x0f, 0xfc, 0x3f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f,
   0x7e, 0x00, 0x00, 0xfe, 0x80, 0x0f, 0xfc, 0x7f, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x3f, 0x7e, 0xc0, 0x3f, 0xfe, 0x80, 0x0f, 0xfe, 0x7e,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f, 0x7e, 0xe0, 0x7f, 0xfe,
   0x80, 0x0f, 0x7e, 0xfe, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f,
   0x7e, 0xe0, 0x7f, 0xfe, 0x80, 0x0f, 0x7e, 0xfc, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x3f, 0x7e, 0xf0, 0x7f, 0xfe, 0x80, 0x0f, 0xff, 0xff,
   0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f, 0xfe, 0xe0, 0x7f, 0xfe,
   0x80, 0x0f, 0xff, 0xff, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f,
   0xfe, 0xe1, 0x7f, 0xfe, 0xc0, 0x8f, 0xff, 0xff, 0x03, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x3f, 0xfc, 0x03, 0x7e, 0xfc, 0xc1, 0x8f, 0xff, 0xff,
   0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f, 0xfc, 0x0f, 0x7f, 0xfc,
   0xf3, 0xcf, 0xff, 0xff, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f,
   0xf8, 0xff, 0x7f, 0xfc, 0xff, 0xcf, 0xef, 0xff, 0x07, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x3f, 0xf0, 0xff, 0x7f, 0xf8, 0xff, 0xc7, 0x0f, 0xf0,
   0x0f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f, 0xe0, 0xff, 0x7f, 0xf8,
   0xff, 0xe3, 0x07, 0xe0, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3f,
   0xc0, 0xff, 0x3f, 0xf0, 0xff, 0xc1, 0x07, 0xe0, 0x07, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x3e, 0x00, 0xff, 0x0f, 0xc0, 0xff, 0xc0, 0x03, 0xc0,
   0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1c, 0x00, 0xfc, 0x03, 0x00,
   0x3f, 0x80, 0x01, 0x80, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0xc0, 0x03, 0x00, 0xc0, 0x07, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc0, 0x07, 0x00, 0xe0,
   0x0f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0xc0, 0x07, 0x00, 0xe0, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0xc0, 0x0f, 0x00, 0xe0, 0x07, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc0, 0x0f, 0x00, 0xf0,
   0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0xc0, 0x1f, 0x00, 0xf0, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x80, 0x1f, 0x00, 0xf8, 0x03, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x3f, 0x00, 0xf8,
   0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0xff, 0x00, 0xfe, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0xfe, 0x83, 0xff, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xfc, 0xff, 0xff,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0xf8, 0xff, 0x3f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0xf0, 0xff, 0x1f, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xe0, 0xff, 0x0f,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0xff, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
   0x00, 0x00, 0x00, 0x00 };

void u8g_prepare() 
{  
  u8g.setFont(u8g_font_6x10);  
  u8g.setFontRefHeightExtendedText();  
  u8g.setDefaultForegroundColor();  
  u8g.setFontPosTop();  
}  
   
void u8g_Tela1()  //Tela 1 - Arduino e Cia - Retangulos  
{
  //u8g.setFont(u8g_font_unifont);  
  //u8g.drawStr( 11, 35, "Arduino e Cia");  
  //u8g.drawStr( 12, 35, "Arduino e Cia");
  u8g.drawXBMP( 0, 0, 128, 64, rook_bitmap);  
  //u8g.drawFrame(0,0,128,64);  
  //u8g.drawFrame(2,2,124,60);   
}  
   
void u8g_Tela2() //Tela 2 - Moldura e relógio  
{
  u8g.setFont(u8g_font_unifont);  
  u8g.drawStr( 11, 20, "Tu saldo es: ");  
  u8g.setPrintPos(11, 40);
  u8g.print(saldo);
}  
   
void u8g_Tela3() //Tela 3 - Caracteres Ascii - Pag. 1  
{
  dis_l2=(litros_p1%10)*100+litros_p2;
  dis_l1=litros_p1/10;
  
  u8g.setFont(u8g_font_unifont);  
  u8g.drawStr( 11, 20, "Quedan:");  
  u8g.setPrintPos(66, 20);
  u8g.print(dis_l1);
  u8g.drawStr( 72, 20, ".");  
  u8g.setPrintPos(78, 20);
  u8g.print(dis_l2);
  u8g.drawStr( 102, 20, "L");  

  u8g.drawStr( 0, 40, "Aun tienes:");  
  u8g.setPrintPos(90, 40);
    u8g.print(segundos);
  u8g.drawStr( 110, 40, "s");  

}  
   
void u8g_Tela4()  //Tela 3 - Caracteres Ascii - Pag. 2  
{
  u8g.setFont(u8g_font_unifont);  
  u8g.drawStr( 11, 20, "Gracias!!");  

}  
   
void u8g_Tela5() //Tela 5 - Arduino e Cia - Retangulo preenchido  
{
  u8g.setFont(u8g_font_unifont);  
  u8g.drawBox(0,0,128,64);  
  u8g.drawBox(2,2,124,60);   
  u8g.setColorIndex(0);  
  u8g.drawStr( 11, 35, "Arduino e Cia");  
  u8g.drawStr( 12, 35, "Arduino e Cia");  
  u8g.drawFrame(2,2,124,60);  
}   
   
void u8g_Tela6()  //Tela 6 - Arduino e Cia em 0, 90 e 270 graus  
{
  u8g.setFont(u8g_font_helvB08);  
  u8g.drawStr(50,31, " Arduino");  
  u8g.drawStr90(50,31, " e");  
  u8g.drawStr270(50,31, " Cia");  
}  
   
void u8g_Tela7() //Tela 7 - Fontes diferentes  
{
  u8g.setFont(u8g_font_robot_de_niro);  
  u8g.drawStr(5,13, "Arduino e Cia !");  
  u8g.setFont(u8g_font_helvB08);  
  u8g.drawStr(5,25, "Arduino e Cia !");  
  u8g.drawBox(5,31, 118,11);  
  u8g.setColorIndex(0);  
  u8g.setFont(u8g_font_8x13);  
  u8g.drawStr(5,41, "Arduino e Cia !");  
  u8g.setColorIndex(1);  
  u8g.setFont(u8g_font_ncenB10);  
  u8g.drawStr(5,60, "Arduino e Cia !");  
}  
   
void draw() //Rotina Desenho  
{
  u8g_prepare();  
  switch(display) //Carrega a tela correspondente  
  {
   case 1:  
    u8g_Tela1();  
    break;  
   case 2:  
    u8g_Tela2();  
    break;  
   case 3:  
    u8g_Tela3();  
    break;  
   case 4:  
    u8g_Tela4();  
    break;  
   case 5:  
    u8g_Tela5();  
    break;  
   case 6:  
    u8g_Tela6();  
    break;  
   case 7:  
    u8g_Tela7();  
    break;  
  }  
}  
   
void setup() 
{  
  // flip screen, if required  
  //u8g.setRot180();  
   
  // assign default color value  
  if ( u8g.getMode() == U8G_MODE_R3G3B2 )   
   u8g.setColorIndex(255);   // white  
  else if ( u8g.getMode() == U8G_MODE_GRAY2BIT )  
   u8g.setColorIndex(1);     // max intensity  
  else if ( u8g.getMode() == U8G_MODE_BW )  
   u8g.setColorIndex(1);     // pixel on  
   Serial.begin(9600);
    Wire.begin(0x05);                          
Wire.onReceive(receiveData); 
  //u8g.setContrast(0x30);  
}  
   
void loop() 
{  
  // picture loop   

    
    u8g.firstPage();   
    do 
    {  
    draw();  
    } 
    while( u8g.nextPage() );  
    
    if(data[0]==0){
     Serial.println("1");
    // IGUA LOGO
    display=1;
     delay(100);
     x=0;
      }

      else if(data[0]==1){
    Serial.println("2");
    // IGUA LOGO
    saldo=data[1];
    display=2;
     delay(100);
     x=0;
      }

      else if(data[0]==2){
     Serial.println("3");
     litros_p1=data[1];
     litros_p2=data[2];
     segundos=data[3];
    display=3;
     delay(100);
     x=0;
      }

     else if(data[0]==3){
     Serial.println("4");
    display=4;
     delay(100);
     x=0;
      }
    delay(100);
}    

void receiveData(int byteCount) { 

   while(Wire.available()) {               //Wire.available() returns the number of bytes available for retrieval with Wire.read(). Or it returns TRUE for values >0.
       data[x]=Wire.read();
       x++;
     }
  
}
