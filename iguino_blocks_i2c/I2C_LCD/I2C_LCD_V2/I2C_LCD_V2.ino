#include <Wire.h>
#include <LiquidCrystal.h>

int data [4];
int x = 0;
int flag=0;
int suma= 0;
int saldo=0;
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

void setup() {                                 

Serial.begin(9600);                        
Wire.begin(0x05);                          
Wire.onReceive(receiveData);               //callback for i2c. Jump to void recieveData() function when pi sends data
lcd.begin(16, 2);
lcd.clear();
}

void loop () {
 
    if(data[0]==0){
     lcd.clear();
     lcd.setCursor(0, 0);
     lcd.print("mAs agua pura...");
     lcd.setCursor(0, 2);
     lcd.print("para Todos!!!");
     delay(100);
     x=0;
      }
    
    else if(data[0]==1){
       if (data[1]==0){
        lcd.clear();
        suma=data[2];
        imprimir_soles(suma);
        delay(100);
        }
       else if (data[1]!=flag){
          suma=suma+data[2];
          imprimir_soles(suma);      
          delay(100);;
          flag=data[1];
          }
         x=0;
        }

     else if(data[0]==2){
      lcd.clear();
      saldo=data[1];
      imprimir_soles(saldo);
      x=0;
      
      }

     else if(data[0]==3){
      lcd.clear();
      lcd.print("...ozonizando...");
      delay(1000);
      x=0;
      
      }
       else if(data[0]==4){
      lcd.clear();

        lcd.setCursor(0, 0);
        lcd.print("Quedan: ");
        lcd.print(data[1]/10);
        lcd.print(".");
        lcd.print(data[1]%10);
        lcd.print("L");

        
        lcd.setCursor(0, 1);
        lcd.print("Aun tienes: ");
        lcd.print(data[2]);
        lcd.print("seg");
        
      
      x=0;
      }
       else if(data[0]==5){
      lcd.clear();
      lcd.print("...gracias!!!...");
      x=0;
      }
    delay(100);                            //Delay 0.1 seconds. Something for the arduino to do when it is not inside the reciveData() function. This also might be to prevent data collisions.

}

void receiveData(int byteCount) { 

   while(Wire.available()) {               //Wire.available() returns the number of bytes available for retrieval with Wire.read(). Or it returns TRUE for values >0.
       data[x]=Wire.read();
       x++;
     }
  
}

void imprimir_soles(int a){
  
        lcd.setCursor(0, 0);
        lcd.print("Tu saldo es: ");
        lcd.setCursor(0, 1);
        lcd.print("S/ ");
        lcd.print(a/10);
        lcd.print(".");
        lcd.print(a%10);
        
        /*if  (a/10==1){
        lcd.println(" sol          "); 
          }
        else{
        lcd.println(" soles        ");
        }*/
  }

  void lcd_intro(){
    
     lcd.clear();
     lcd.setCursor(0, 0);
     lcd.print("mAs agua pura...");
     lcd.setCursor(0, 2);
     lcd.print("para Todos!!!");
     delay(4000);
     lcd.clear();
     lcd.setCursor(0, 0);
     lcd.print("cuida tu salud..");
     lcd.setCursor(0, 2);
     lcd.print("y la del planeta!");
     delay(4000);
     lcd.clear();
     lcd.setCursor(0, 0);
     lcd.print("mejor agua y...");
     lcd.setCursor(0, 2);
     lcd.print("menos plAstico");
     delay(4000);
     lcd.clear();
     lcd.setCursor(0, 0);
     lcd.print("f/aguaigua");
     lcd.setCursor(0, 2);
     lcd.print("http://igua.pe");
     delay(4000);
     lcd.clear();
     lcd.setCursor(0, 0);
     lcd.print("Hola mundo!!");
     lcd.setCursor(0, 2);
     lcd.print("Hola igua!!");
     delay(4000);
     lcd.clear();
     lcd.setCursor(0, 0);
     lcd.print("agua igua,");
     lcd.setCursor(0, 2);
     lcd.print("salud!");
     delay(4000);
     x=0;
    
    }
