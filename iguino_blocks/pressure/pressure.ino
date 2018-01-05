//A0 = Verde = S1 = salida UF
//A1 = Blanco = 
//A2 = Azul = S3 = salida carbon
//A3 = Amarillo = S4 = Entrada

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  int sensorVal = analogRead(A0);
  float sensorVal1 = 0;
  for(int i=0;i<5000;i++)
    {
      sensorVal = analogRead(A0);
      sensorVal1 = sensorVal + sensorVal1;
    }
  sensorVal1 = sensorVal1/5000;
  float voltage = (sensorVal1*5.0)/1024.0;
  float psi = (3.0*((float)voltage-0.48))*14.5;
  Serial.print("Entrada: ");
  Serial.print(voltage);
  Serial.print(" Voltios - Presion = ");
  Serial.print(psi);
  Serial.print(" psi // ");

  sensorVal = analogRead(A2);
  sensorVal1 = 0;
  for(int i=0;i<5000;i++)
    {
      sensorVal = analogRead(A2);
      sensorVal1 = sensorVal + sensorVal1;
    }
  sensorVal1 = sensorVal1/5000;
  voltage = (sensorVal1*5.0)/1024.0;
  psi = (3.0*((float)voltage-0.53))*14.5;
  Serial.print("Carbon: ");
  Serial.print(voltage);
  Serial.print(" Voltios - Presion = ");
  Serial.print(psi);
  Serial.print(" psi // ");

  sensorVal = analogRead(A3);
  sensorVal1 = 0;
  for(int i=0;i<5000;i++)
    {
      sensorVal = analogRead(A3);
      sensorVal1 = sensorVal + sensorVal1;
    }
  sensorVal1 = sensorVal1/5000;
  voltage = (sensorVal1*5.0)/1024.0;
  psi = (3.0*((float)voltage-0.47))*14.5;
  Serial.print("UF: ");
  Serial.print(voltage);
  Serial.print(" Voltios - Presion = ");
  Serial.print(psi);
  Serial.println(" psi // ");
  
  delay(1000);
}
