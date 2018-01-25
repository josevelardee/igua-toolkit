/*
Liquid flow rate sensor -DIYhacking.com Arvind Sanjeev

Measure the liquid/water flow rate using this code. 
Connect Vcc and Gnd of sensor to arduino, and the 
signal line to arduino digital pin 2.
 
 */
 
 // 1 balde = 4 litros = 4:30 min
 
 // 1 litro = 270 segundos / 4
 // 1 litro = 67.5 segundos
 // 0.x litros = 60 segundos
 
 // x = 60 / 67.6 = 0.88 l/min
 
int losMililitros = 0;
byte statusLed    = 13;

byte sensorInterrupt = 0;  // 0 = digital pin 2
byte sensorPin       = 2;

// The hall-effect flow sensor outputs approximately 4.5 pulses per second per
// litre/minute of flow.
float calibrationFactor = 4.5;

volatile byte pulseCount;
int modo = 0;
int orden = 0;
int b1 = 1; int b1_old = 1;
int b2 = 1; int b2_old = 1;
int b3 = 1; int b3_old = 1;
int b4 = 1; int b4_old = 1;
int b5 = 1; int b5_old = 1;


float flowRate;
unsigned int flowMilliLitres;
unsigned long totalMilliLitres;
unsigned long oldTotalMillilitres;
unsigned long before;

unsigned long oldTime;

void setup()
{
  
  // Initialize a serial connection for reporting values to the host
  Serial.begin(9600);
   
  // Set up the status LED line as an output
  pinMode(statusLed, OUTPUT);
  digitalWrite(statusLed, HIGH);  // We have an active-low LED attached
  
  pinMode(sensorPin, INPUT_PULLUP);
  pinMode(8, INPUT_PULLUP);
  pinMode(9, INPUT_PULLUP);
  pinMode(10, INPUT_PULLUP);
  pinMode(11, INPUT_PULLUP);
  pinMode(12, INPUT_PULLUP);
  
  digitalWrite(sensorPin, HIGH);

  pulseCount        = 0;
  flowRate          = 0.0;
  flowMilliLitres   = 0;
  totalMilliLitres  = 0;
  oldTotalMillilitres = 0;
  oldTime           = 0;
  before = millis();
  

  // The Hall-effect sensor is connected to pin 2 which uses interrupt 0.
  // Configured to trigger on a FALLING state change (transition from HIGH
  // state to LOW state)
  attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
}

/**
 * Main program loop
 */
void loop()
{
    int mililitros = int(losMililitros);
    String mensaje1 = "maquina: 1  servido: " + String(mililitros);
    String mensaje2 = " modo: " + String(modo);
    b1_old = b1; b1 = digitalRead(8); if(b1-b1_old == -1) {Serial.println(mensaje1+mensaje2); delay(50);modo=0; orden = 100; totalMilliLitres=0; digitalWrite(13, HIGH); }
    b2_old = b2; b2 = digitalRead(9); if(b2-b2_old == -1) {Serial.println(mensaje1+mensaje2); delay(50);modo=1; orden = 200; totalMilliLitres=0; digitalWrite(13, HIGH); }
    b3_old = b3; b3 = digitalRead(10); if(b3-b3_old == -1) {Serial.println(mensaje1+mensaje2); delay(50);modo=2; orden = 300; totalMilliLitres=0; digitalWrite(13, HIGH); }
    b4_old = b4; b4 = digitalRead(11); if(b4-b4_old == -1) {Serial.println(mensaje1+mensaje2); delay(50);modo=3; orden = 400; totalMilliLitres=0; digitalWrite(13, HIGH); }
    b5_old = b5; b5 = digitalRead(12); if(b5-b5_old == -1) {Serial.println(mensaje1+mensaje2); delay(50);modo=4; orden = 500; totalMilliLitres=0; digitalWrite(13, HIGH); }
    if (totalMilliLitres/4 > orden) {digitalWrite(13,LOW); }


   if((millis() - oldTime) > 400)    // Only process counters once per second
  { 
    // Disable the interrupt while calculating flow rate and sending the value to
    // the host
    detachInterrupt(sensorInterrupt);


        
    // Because this loop may not complete in exactly 1 second intervals we calculate
    // the number of milliseconds that have passed since the last execution and use
    // that to scale the output. We also apply the calibrationFactor to scale the output
    // based on the number of pulses per second per units of measure (litres/minute in
    // this case) coming from the sensor.
    flowRate = (250 * float(pulseCount) / (millis() - oldTime));
    
    // Note the time this processing pass was executed. Note that because we've
    // disabled interrupts the millis() function won't actually be incrementing right
    // at this point, but it will still return the value it was set to just before
    // interrupts went away.
    oldTime = millis();
    
    // Divide the flow rate in litres/minute by 60 to determine how many litres have
    // passed through the sensor in this 1 second interval, then multiply by 1000 to
    // convert to millilitres.
    flowMilliLitres = flowRate * 1.0;
    
    // Add the millilitres passed in this second to the cumulative total

    oldTotalMillilitres = totalMilliLitres;
    totalMilliLitres += flowMilliLitres;
    losMililitros = totalMilliLitres / 4;
      
    
    // Print the flow rate for this second in litres / minute
    // Serial.print(int(flowRate));  // Print the integer part of the variable
    

    
    /*
    if (oldTotalMillilitres != totalMilliLitres)
      {
      before = millis();
      }
    if ((millis() - before) > 43200000 ) //     12 horas sin uso?
      {totalMilliLitres = 0;}
      // Serial.println("mL");
    */
 

    // Reset the pulse counter so we can start incrementing again
    pulseCount = 0;
    
    // Enable the interrupt again now that we've finished sending output
    attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
  }
}

/*
Insterrupt Service Routine
 */
void pulseCounter()
{
  // Increment the pulse counter
  pulseCount++;
}
