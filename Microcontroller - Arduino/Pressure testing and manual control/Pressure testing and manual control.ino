
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

//manual control
int manual_control;
char c = 'q';
int terminate = 0;

//Pressure sensor
int PressureSensor = A2;
int pressure = 0;

int cycle_switch = 0;


// Setup the essentials for your circuit to work. It runs first every time your circuit is powered with electricity.
void setup() 
{
    // Setup Serial which is useful for debugging
    // Use the Serial Monitor to view printed messages
    Serial.begin(9600);
    while (!Serial) ; // wait for serial port to connect. Needed for native USB
    Serial.println("start");
    
    // menuOption = menu();
    
}

// Main logic of your circuit. It defines the interaction between the components you selected. After setup, it runs over and over again, in an eternal loop.

void loop(){
  // Deflate();
  Menu();
}

void Menu() {
    Menu_banner();
    for (;;) {
        switch (Serial.read()) {
            case '1': Inialize(); Menu_banner(); break;
            case '2': Manual_control(); break;
            case '3': {
              c = 'q';
              Biofeedback(); break;
            }
            case '4': {
               c = 'q';
              cycle_switch = 1;
              Cycle(); break;
            }
            case '5': {
              Hold(); 
              Serial.println(F("Solenoids are offline"));
              Menu_banner();
              break;}
    
            case '6': {
              Hold(); 
              Serial.println(F("Presure test start"));
              Pressure_test(); break;
              }
            case '9': return;
            default: continue;  // includes the case 'no input'
        }
    }
}

void Menu_banner(){
  Serial.println(F("\nWhat would you like to test?"));
  Serial.println(F("(1) Inialize #1"));
  Serial.println(F("(2) Manual Control #2"));
  Serial.println(F("(3) Biofeedback #3"));
  Serial.println(F("(4) Cycle #4"));
  Serial.println(F("(5) System Off #5"));
  Serial.println(F("(6) Pressure test #6"));
  Serial.println(F("(menu) send anything else or press on board reset button\n"));
}

void Inialize(){
  solenoidValve2_2.on();
  solenoidValve1_1.off();
  delay(5000);
  solenoidValve1_1.on();
  solenoidValve2_2.off();
  delay(3000);
  solenoidValve2_2.off();
  solenoidValve1_1.off();
}

void Manual_control(){
 
  Serial.println(F("(1) Inflate short #1"));
  Serial.println(F("(2) Deflate short #2"));
  Serial.println(F("(3) Inflate long #3"));
  Serial.println(F("(4) Deflate long #4"));
  // Serial.println(F("(3) Hold #3"));
  Serial.println(F("(5) Return #5"));
  for (;;) {
    // pressure = analogRead(PressureSensor);
    // Serial.println(pressure);
        switch (Serial.read()) {
            case '1': Inflate(); delay(100); Hold(); break;
            case '2': Deflate(); delay(100); Hold(); break;
            case '3': Inflate(); delay(1000); Hold(); break;
            case '4': Deflate(); delay(1000); Hold(); break;
            // case '5': Hold(); break;
            case '5': Hold(); Menu(); break;
            default: continue;  // includes the case 'no input'
            }
          }
}


// void Biofeedback(){
//   while (c == 'q') {
//     // c = Serial.read();
//       while(i<20){
//           array[i] = analogRead(BreathingSensor);
//           total = total + array[i];
//           i++;
//           delay(10);
//         }
//       i=0;
//         prev = val;   
//         val = total/20;
//         total=0;

//         if (val > prev+2) {
//                 Serial.print("1");
//                 Inflate();
//             } else if (val < prev-2) {
//                 Serial.print("-1");
//                 Deflate();
//             } else if ((val <= prev+3) && (val >= prev-3)) {
//                 Serial.print("0");
//                 Hold();
//             }
//       Serial.print(" ");
//       Serial.println(val); 
//     }
// }

void Biofeedback(){
  while (c == 'q') {
    // c = Serial.read();
      while(i<20){
          BreatheArray[i] = analogRead(BreathingSensor);
          PressureArray[i] = analogRead(PressureSensor);
          BreatheTotal = BreatheTotal + BreatheArray[i];
          PressureTotal = PressureTotal + BreatheArray[i];
          i++;
          delay(10);
        }
      i=0;
        Prev_BreatheVal = BreatheVal;   
        BreatheVal = BreatheTotal/20; PressureVal = PressureTotal/20;
        BreatheTotal=0; PressureTotal=0;

        if (BreatheVal > Prev_BreatheVal+2) {
                Serial.print("1");
                Inflate();
            } else if (BreatheVal < Prev_BreatheVal-2) {
                Serial.print("-1");
                Deflate();
            } else if ((BreatheVal <= Prev_BreatheVal+3) && (BreatheVal >= Prev_BreatheVal-3)) {
                Serial.print("0");
                Hold();
            }
      Serial.print(" ");
      Serial.println(BreatheVal); 
      Serial.print(" ");
      Serial.println(PressureVal); 
    }
}

void Cycle(){
while (c == 'q') {
    while(i<60){
      i++;
    } 
    i=0;
    if (cycle_switch == 1){
      Inflate();
      cycle_switch = -1;
    } else if (cycle_switch == -1){
      Deflate();
      cycle_switch = 1;
    }
  }
}


void Pressure_test(){
  while(c== 'q'){
    PressureVal = analogRead(PressureSensor);
    Serial.println(PressureVal);
    delay(5000);
    Inflate(); 
    delay(100); 
    Hold();
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



