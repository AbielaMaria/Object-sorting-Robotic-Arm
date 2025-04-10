#include <Arduino.h>
#include <ESP32Servo.h>
#include <vector>

// Servo structure and variables
struct ServoPins {
  Servo servo;
  int servoPin;
  String servoName;
  int initialPosition;
};

std::vector<ServoPins> servoPins = {
  { Servo(), 14, "Arm", 90 },  // Single servo on pin 14, starting at 90 degrees
};

void writeServoValues(int servoIndex, int value) {
  servoPins[servoIndex].servo.write(value);
  Serial.printf("Moving %s to position %d\n", servoPins[servoIndex].servoName.c_str(), value);
}

void setUpPinModes() {
  for (int i = 0; i < servoPins.size(); i++) {
    servoPins[i].servo.attach(servoPins[i].servoPin);
    servoPins[i].servo.write(servoPins[i].initialPosition);  // Set to initial position
  }
}

void handleCommand(String command) {
  if (command == "Move Left") {
    writeServoValues(0, 90);  // Move arm to the left (0 degrees)
  } else if (command == "Move Right") {
    writeServoValues(0, 180);  // Move arm to the right (180 degrees)
  } else if (command == "Move Up") {
    writeServoValues(0, 180);  // Move arm up (90 degrees)
  } else if (command == "Move Down") {
    writeServoValues(0, 90);  // Move arm down (45 degrees)
  } else {
    Serial.println("Unknown command.");
  }
}

void setup() {
  setUpPinModes();
  Serial.begin(9600);  // Start serial communication at 9600 baud rate
  Serial.println("Ready to receive commands.");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');  // Read the command from serial
    handleCommand(command);
  }
}
