 #include <Servo.h>

 Servo servoThumb;          // Define the servo objects for the wrist and fingers
 Servo servoIndex;
 Servo servoMiddle;
 Servo servoRing;
 Servo servoPinky;
 Servo servoWrist;
 Servo servoElbow;         // Define the servo objects for the shoulder and elbow
 Servo servoShoulder1;
 Servo servoShoulder2;
 Servo servoShoulder3;

void setup() {
  Serial.begin(9600); // Set the baud rate to match the Serial monitor
  servoThumb.attach(22);
  servoIndex.attach(24);
  servoMiddle.attach(26);
  servoRing.attach(28);
  servoPinky.attach(30);
  servoWrist.attach(32);
  servoElbow.attach(34);
  servoShoulder1.attach(36);
  servoShoulder2.attach(38);
  servoShoulder3.attach(40); 
  resetServos();
  }

void resetServos() {
  servoShoulder1.write(0);
  servoShoulder2.write(30);
  delay(1000);
  servoShoulder3.write(60);
  delay(1000);
  servoElbow.write(0);
  servoWrist.write(0);
  servoPinky.write(0);
  servoRing.write(0);
  servoMiddle.write(0);
  servoIndex.write(0);
  servoThumb.write(0);
}

void loop() {
  if (Serial.available() >= 10) { // Check if at least 10 characters are available in the Serial buffer
    String receivedString = Serial.readStringUntil('\n'); // Read the string until a newline character is encountered
    
    if (receivedString == "hello$0110000000") { 
    servoShoulder2.write(145);
    delay(2000);
    servoShoulder3.write(80); 
    delay(8000);
    resetServos();
    receivedString ="";
  } else if (receivedString == "my$0110000000") {
    servoShoulder2.write(90);
    delay(2000);
    servoShoulder3.write(40);
    delay(6000);
    resetServos();
    receivedString ="";
  } else if (receivedString == "name$0110011001"){
    servoShoulder2.write(60);
    servoShoulder3.write(70);
    servoPinky.write(90); 
    servoRing.write(90);
    servoThumb.write(90); 
    delay(8000);
    resetServos();
    receivedString ="";
  } else if (receivedString == "is$0110011111"){
    servoShoulder2.write(130);
    servoShoulder3.write(120);
    servoPinky.write(90); 
    servoRing.write(90);
    servoThumb.write(90); 
    servoMiddle.write(90); 
    servoIndex.write(90);
    delay(8000);
    resetServos();
    receivedString ="";
  } else if (receivedString == "thamer$0110011111"){
    servoShoulder2.write(130);
    servoShoulder3.write(120);
    servoPinky.write(90); 
    servoRing.write(90);
    servoThumb.write(90); 
    servoMiddle.write(90); 
    servoIndex.write(90);
    delay(8000);
    resetServos();
    receivedString ="";
  }
}
}