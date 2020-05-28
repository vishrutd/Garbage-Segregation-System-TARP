#include <Keypad.h>
#include <SoftwareSerial.h>


SoftwareSerial SIM900(7, 8); //(RX,TX)

String str;
const byte numRows= 4;

const byte numCols= 4;



char keymap[numRows][numCols]= { {'1', '2', '3', 'A'},

{'4', '5', '6', 'B'},

{'7', '8', '9', 'C'},

{'*', '0', '#', 'D'} };

byte rowPins[numRows] = {6,2,3,9}; 

byte colPins[numCols]= {10,11,12,5}; 

Keypad myKeypad= Keypad(makeKeymap(keymap), rowPins, colPins, numRows, numCols);
void setup() {
  Serial.begin(19200);
  // Arduino communicates with SIM900 GSM shield at a baud rate of 19200
  
  SIM900.begin(19200);
  int c=0;
Serial.print("Enter a mobile number: ");
while(c<10){
char keypressed = myKeypad.getKey();
if (keypressed != NO_KEY)
{
c++;
str=str+keypressed;
Serial.print(keypressed);
}
}
Serial.println();
Serial.println(str);
  // Send SMS
  sendSMS();
}

void loop() { 
  
}

void sendSMS() {
  
  SIM900.print("AT+CMGF=1\r");// 
  delay(100);

  
  SIM900.println("AT + CMGS = \"+91"+str+"\""); 
  delay(100);
  
  // REPLACE WITH YOUR OWN SMS MESSAGE CONTENT
  SIM900.println("TEST123"); 
  delay(100);

  // End AT command with a ^Z, ASCII code 26
  SIM900.println((char)26); 
  delay(100);
  SIM900.println();
  delay(5000); 
}
