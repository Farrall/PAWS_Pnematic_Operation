
// Include Libraries
#include "Arduino.h"
#include "SolenoidValve.h"

// Pin Definitions
#define SOLENOIDVALVE1_1_PIN_COIL1	4
#define SOLENOIDVALVE2_2_PIN_COIL1	2

// Global variables and defines

// object initialization
SolenoidValve solenoidValve1_1(SOLENOIDVALVE1_1_PIN_COIL1);
SolenoidValve solenoidValve2_2(SOLENOIDVALVE2_2_PIN_COIL1);


// define vars for testing menu
const int timeout = 10000;       //define timeout of 10 sec
char menuOption = 0;
long time0;

// define vars for breathing
int BreathingSensor = A0;
int BreatheArray[20];
int PressureArray[20];
int i = 0;
int j = 0;
int BreatheTotal = 0;
int PressureTotal = 0;
int average = 0;
int BreatheVal = 0;
int Prev_BreatheVal;
int PressureVal;
float ballSize = 60.0;

//manual control
int manual_control;
char c = 'q';
int terminate = 0;

//Pressure sensor
int PressureSensor = A2;
int pressure = 0;

int cycle_switch = 0;
int start = 0;
int paused = 0; // 0 is paused, 1 is playing
int action = 6; // 6 is hold, 5 is inflate, 7 is deflate


// Setup the essentials for your circuit to work. It runs first every time your circuit is powered with electricity.
void setup() 
{
    // Setup Serial which is useful for debugging
    // Use the Serial Monitor to view printed messages
    Serial.begin(9600);
    while (!Serial) ; // wait for serial port to connect. Needed for native USB
//    Serial.println("start");
    
    // menuOption = menu();
    
}

// Main logic of your circuit. It defines the interaction between the components you selected. After setup, it runs over and over again, in an eternal loop.

void loop(){
//  Deflate();
//  Menu();
while (!Serial.available());
start = Serial.readString().toInt();
if (start == 1){
  Biofeedback();
}
if (start == 2){
  Manual();
}

}

void Biofeedback(){
  while (c == 'q') {
    if(Serial.available()){
      paused = Serial.readString().toInt();
    }
     //c = Serial.read();
     if(paused == 0){
      while(i<20){
          BreatheArray[i] = analogRead(BreathingSensor);
          PressureArray[i] = analogRead(PressureSensor);
          BreatheTotal = BreatheTotal + BreatheArray[i];
          PressureTotal = PressureTotal + PressureArray[i];
          i++;
          delay(5);
        }
      i=0;
        Prev_BreatheVal = BreatheVal;   
        BreatheVal = BreatheTotal/20; PressureVal = PressureTotal/20;
        BreatheTotal=0; PressureTotal=0;

      Serial.print(BreatheVal); 
      Serial.print(" ");
      Serial.print(PressureVal); 
      Serial.print(" ");
      
              if (BreatheVal > Prev_BreatheVal+1 && ballSize <= 80.0) {
                Serial.println("1");
                Inflate();
                ballSize += 0.4;
            } else if (BreatheVal < Prev_BreatheVal-1 && ballSize >= 40.0) {
                Serial.println("-1");
                Deflate();
                ballSize -= 0.4;
            } else if ((BreatheVal <= Prev_BreatheVal+1) && (BreatheVal >= Prev_BreatheVal-1)) {
                Serial.println("0");
                Hold();
            }
     }
     else if(paused == 1){
       Hold();
       delay(50);
     }
     else if(paused == -1){
       Hold();
       loop();
     }
    }
}

void Manual(){
  while(c == 'q'){
    if(Serial.available()){
      // actions are 5 for inflate, 6 for hold, 7 for deflate, 0 for pausing
      action = Serial.readString().toInt();
    }
    if(action != 0){
        if(action == 5 && ballSize <= 80.0){
          PressureVal = analogRead(PressureSensor);

          Serial.print(int(ballSize * 10));
          Serial.print(" ");

          Serial.print(PressureVal); 
          Serial.print(" ");

          Serial.println("1");
          Inflate();
          ballSize += 0.4;
        }
        else if(action == 7 && ballSize >= 40.0){
          PressureVal = analogRead(PressureSensor);

          Serial.print(int(ballSize * 10));
          Serial.print(" ");

          Serial.print(PressureVal); 
          Serial.print(" ");

          Serial.println("-1");
          Deflate();
          ballSize -= 0.4;
        }
        else if(action == 6){
          PressureVal = analogRead(PressureSensor);

          Serial.print(int(ballSize * 10));
          Serial.print(" ");

          Serial.print(PressureVal); 
          Serial.print(" ");

          Serial.println("0");
          Hold();
        }
      
    }
    else if(action == 0){
      Hold();
      delay(50);
    }
    else if(action == -1){
      Hold();
      loop();
    }
  }
}

void Inflate(){
  solenoidValve2_2.off();
  solenoidValve1_1.on();
}

void Deflate(){
  solenoidValve2_2.on();
  solenoidValve1_1.off();
}

void Hold(){
  solenoidValve2_2.off();
  solenoidValve1_1.off();
}

