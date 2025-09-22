/* This example shows how to use continuous mode to take
range measurements with the VL53L0X. It is based on
vl53l0x_ContinuousRanging_Example.c from the VL53L0X API.

The range readings are in units of mm. */

#include <Wire.h>
#include <VL53L0X.h>

VL53L0X sensor;

/* -- Led status --- */
bool blinkState;

/* --- Sampling interval in microseconds --- */
uint32_t Ts = 20000;

/* --- Configuring interruption pin --- */
const int interruptPin = 2;  
volatile bool newMeasurement = false;

void setup()
{
  Serial.begin(38400);
  Wire.begin();

  /* --- Configure external interrupts --- */
  attachInterrupt(digitalPinToInterrupt(interruptPin), measurementReady, FALLING);
  
  sensor.setTimeout(500);
  if (!sensor.init())
  {
    Serial.println("VL53L0X connection failed");
    while(1){
    }
  }

  Serial.println("VL53L0X connection succesful");

  /* --- Sampling frequency response --- */
  Serial.println("Selected sampling frequency:");
  Serial.println(1.0/(Ts*1e-6));
  
  /* Waiting for confirmation */
  uint8_t proceed = 0;
  while(!proceed){
    if (Serial.available() > 0) {
      proceed = 1;
    }
  }
  
  /* Procceding to get raw data */
  Serial.println("Getting distance data in mm...");

  /*Configure board LED pin for output*/ 
  pinMode(LED_BUILTIN, OUTPUT);

  /* --- Select sampling interval in microseconds --- */
  sensor.setMeasurementTimingBudget(Ts);

  /* --- Continuous mode --- */
  sensor.startContinuous();;
}

void loop()
{
  if (newMeasurement) {
    newMeasurement = false;
  
    /* --- Read distance in mm --- */
    uint16_t distance = sensor.readRangeContinuousMillimeters();
  
    /* --- Error check --- */
    if (sensor.timeoutOccurred()) {
      Serial.println("Measurement timeout");
    } else {
      Serial.println(distance);
      /* Blink LED to indicate activity */
      blinkState = !blinkState;
      digitalWrite(LED_BUILTIN, blinkState);
    }
  }
}

void measurementReady() {
  newMeasurement = true;
}
