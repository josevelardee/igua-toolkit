/*
temp lights LM35 and leds
*/

int tempPin = A0;
int tdsPin = A2;
float tdsVolt;
float tdsVolt1;
float Temp;


void setup() {
  Serial.begin(9600);

  pinMode (tempPin, INPUT);
  pinMode (tdsPin, INPUT);
}

  void loop() {
    //Tempeatura
    Temp = analogRead(tempPin);
   Temp = log(((10240000/Temp) - 10000));
   Temp = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * Temp * Temp ))* Temp );


       if (Temp > 220){
       Temp= Temp - 187.265;
      }
      else if (Temp < 220) {
        Temp= Temp - 195.265; 
        }

    //TDS
    tdsVolt=analogRead(tdsPin);
   tdsVolt1=tdsVolt*3.4248;
    

    //Monitoreo
   
    Serial.print(Temp);
    Serial.print(" ");
    Serial.print(tdsVolt1);
    Serial.println(" ");
    delay(1000);
    

}
