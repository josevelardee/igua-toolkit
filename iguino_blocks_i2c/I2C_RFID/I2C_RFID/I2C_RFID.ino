#include <SPI.h>
#include <MFRC522.h>
#include <Wire.h>
#define SLAVE_ADDRESS 0x04
#define RST_PIN  9    //Pin 9 para el reset del RC522
#define SS_PIN  10   //Pin 10 para el SS (SDA) del RC522

volatile byte leArray[4];
volatile boolean sendStuff;

MFRC522 mfrc522(SS_PIN, RST_PIN); //Creamos el objeto para el RC522

int aux[4] = {0,0,0,0};

void setup() {
  Serial.begin(9600); //Iniciamos la comunicación  serial
  SPI.begin();        //Iniciamos el Bus SPI
  Wire.begin(SLAVE_ADDRESS);

  Wire.onRequest(sendData);
  mfrc522.PCD_Init(); // Iniciamos  el MFRC522
  //Serial.println("Lectura del UID");
}

void loop() {

if ( mfrc522.PICC_IsNewCardPresent()) 
        {  
       
    if ( mfrc522.PICC_ReadCardSerial()) 
            {
              
                  for (byte i = 0; i < mfrc522.uid.size; i++) {
                      
                          //Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
                          //Serial.print(mfrc522.uid.uidByte[i], HEX);  
                          aux[i]=mfrc522.uid.uidByte[i];
                     
                  } 
                  
                  mfrc522.PICC_HaltA();         

  leArray[0] = aux[0];
  leArray[1] = aux[1];
  leArray[2] = aux[2];
  leArray[3] = aux[3];

  sendStuff = true;
            
            }
        

  //delay(2000);
        }

 
  
} // end loop


void sendData() {
  if(sendStuff)
  {
    Wire.write((byte*)leArray, 4);
  }
  sendStuff= false;
  

}
