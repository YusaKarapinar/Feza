#include <Servo.h>
Servo servoMotor;  // Servo nesnesi oluşturuluyor
Servo servoMotor2;  // Servo nesnesi oluşturuluyor

String y;
int x;
int old_x=90;
int old_y=90;
void setup() { 
	Serial.begin(115200); 

	Serial.setTimeout(1); 
    servoMotor.attach(8);  // Servo motorun bağlı olduğu pin belirtiliyor
        servoMotor2.attach(9);  // Servo motorun bağlı olduğu pin belirtiliyor

} 
void loop() { 
	while (!Serial.available()); 
	y = Serial.readString();
  if(y[0]=='x'){
  y = y.substring(1);  
    x=y.toInt();
    old_x=x/5+old_x;
    if(old_x>0 && old_x<180){
    servoMotor.write(old_x);
    }
    if(old_x>180){
    old_x=180;
    }
    else if(old_x<0){
    old_x=0;
    }
  
  }
  else if(y[0]=='y'){
  y = y.substring(1);   
  x=y.toInt();
  old_y=x/5+old_y;
    if(old_y>0 && old_y<180){
    servoMotor2.write(old_y);
    }
    if(old_y>180){
    old_y=180;
    }
    else if(old_y<0){
    old_y=0;
    }
  }
  


  delay(100);

} 
