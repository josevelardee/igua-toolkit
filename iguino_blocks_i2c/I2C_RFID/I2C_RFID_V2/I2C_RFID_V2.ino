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

            
if ( ! mfrc522.PICC_IsNewCardPresent()) { //If a new PICC placed to RFID reader continue
    return 0;
  }
  if ( ! mfrc522.PICC_ReadCardSerial()) {   //Since a PICC placed get Serial and continue
    return 0;
  }
  // There are Mifare PICCs which have 4 byte or 7 byte UID care if you use 7 byte PICC
  // I think we should assume every PICC as they have 4 byte UID
  // Until we support 7 byte PICCs


  for ( uint8_t i = 0; i < 4; i++) {  //
    aux[i] = mfrc522.uid.uidByte[i];
    //Serial.print(readCard[i], HEX);
  }
  //Serial.println("");
  mfrc522.PICC_HaltA(); // Stop reading
        
  leArray[0] = aux[0];
  leArray[1] = aux[1];
  leArray[2] = aux[2];
  leArray[3] = aux[3];

  sendStuff = true;

  delay(500);

  
} // end loop


void sendData() {
  if(sendStuff)
  {
    Wire.write((byte*)leArray, 4);
  }
  sendStuff= false;
  

}
