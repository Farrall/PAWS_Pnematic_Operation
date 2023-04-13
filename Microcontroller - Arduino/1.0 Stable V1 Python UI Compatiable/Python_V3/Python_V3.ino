
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
int start = 0;


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
  Inialize();
  start = 0;
}

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
  Serial.println(F("(menu) send anything else or press on board reset button\n"));
}

void Inialize(){
  Deflate();
  delay(30000);
  Inflate();
  delay(20000);
  Hold();
  return;
}

void Manual_control(){
  Serial.println(F("(1) Inflate #1"));
  Serial.println(F("(2) Deflate #2"));
  Serial.println(F("(3) Hold #3"));
  Serial.println(F("(4) Return #4"));
  for (;;) {
    // pressure = analogRead(PressureSensor);
    // Serial.println(pressure);
        switch (Serial.read()) {
            case '1': Inflate(); break;
            case '2': Deflate(); break;
            case '3': Hold(); break;
            case '4': Hold(); Menu(); break;
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
      
              if (BreatheVal > Prev_BreatheVal+1) {
                Serial.println("1");
                Inflate();
            } else if (BreatheVal < Prev_BreatheVal-1) {
                Serial.println("-1");
                Deflate();
            } else if ((BreatheVal <= Prev_BreatheVal+1) && (BreatheVal >= Prev_BreatheVal-1)) {
                Serial.println("0");
                Hold();
            }
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



// void loop() 
// {
//     if(menuOption == '1') { //initalize
//     solenoidValve2_2.on();
//     solenoidValve1_1.off();
//     delay(5000);
//     solenoidValve1_1.on();
//     solenoidValve2_2.off();
//     delay(3000);
//     solenoidValve2_2.off();
//     solenoidValve1_1.off();
//     menuOption = menu();
//     }

//     else if(menuOption == '2') { //biofeedback
//       manual_control = Serial.read();
//       pressure = analogRead(PressureSensor);
//       Serial.println(PressureSensor);

//       if (manual_control == 'p'); {
//           solenoidValve1_1.off();
//           solenoidValve2_2.off();
//           // menuOption = menu();
//           terminate=1;
//     }
//       while(i<10){
//         array[i] = analogRead(BreathingSensor);
//         total = total + array[i];
//         i++;
//         delay(10);
//       }
//       i=0;
//         prev = val;   
//         val = total/10;
//         total=0;

//         if (val > prev+1) {
//                 // Serial.println("1");
//                 solenoidValve1_1.on();
//                 solenoidValve2_2.off();
//             } else if (val < prev-1) {
//                 // Serial.println("-1");
//                 solenoidValve1_1.off();
//                 solenoidValve2_2.on();
//             } else if ((val <= prev+1) && (val >= prev-1)) {
//                 // Serial.println("0");
//                 solenoidValve1_1.off();
//                 solenoidValve2_2.off();
//             }
//         // Serial.print(" ");
//         // Serial.println(val);          // debug value
//     }
    
//     else if(menuOption == '3') { //Empty and Finish
//     solenoidValve2_2.on();
//     solenoidValve1_1.off();
//     delay(20000);
//     solenoidValve2_2.off();
//     solenoidValve1_1.off();
//     menuOption = menu();
//     }

//     else if(menuOption == '4') { //manual control
//     // while (!Serial.available());
//     // while (Serial.available()) {
//       char c = Serial.read();
//       if(c == 'd'){
//         solenoidValve1_1.on();
//         solenoidValve2_2.off();
//       }
//       if(c == 'a'){
//         solenoidValve1_1.off();
//         solenoidValve2_2.on();
//       }
//       if(c == 'p'){
//         solenoidValve1_1.off();
//         solenoidValve2_2.off();
//         // menuOption = menu();
//         terminate=1;
//       }
//     }
//     // }
//     // menuOption = menu();
//     if (terminate == 1)
//     {
//         solenoidValve1_1.off();
//         solenoidValve2_2.off();
//         terminate=0;
//         menuOption = menu();
//     }
     
// }


// Menu function for selecting the components to be tested
// Follow serial monitor for instrcutions
// char menu()
// {
//   Serial.println(F("\nWhat would you like to test?"));
//   Serial.println(F("(1) Inialize #1"));
//   Serial.println(F("(2) Biofeedback #2"));
//   Serial.println(F("(3) Empty and Finish #3"));
//   Serial.println(F("(4) Manual Control #4"));
//   Serial.println(F("(menu) send anything else or press on board reset button\n"));
//   while (!Serial.available());

//   // Read data from serial monitor if received
//   while (Serial.available()) 
//   {
//       char c = Serial.read();
//       if (isAlphaNumeric(c)) 
//       {   
//           if(c == '1') 
//             Serial.println(F("Now initalizing #1"));
//           else if(c == '2') {
//             Serial.println(F("Biofeedback is now operational #2"));
//             Serial.println(F("Enter 'p' to terminate"));
//           }
//           else if(c == '3') 
//             Serial.println(F("Deflating and powering down #3"));
//           else if(c == '4') {
//             Serial.println(F("Manual Control acquired #3"));
//             Serial.println(F("Enter 'a' to continually deflate or 'd' to inflate"));
//             Serial.println(F("Enter 'p' to terminate"));
//             }
//           else
//           {
//               Serial.println(F("illegal input!"));
//               return 0;
//           }
//           time0 = millis();
//           // terminate = 0;
//           return c;
//       }
//   }
// }
