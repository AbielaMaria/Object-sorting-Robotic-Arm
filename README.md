Object Sorting Robotic Arm
  The Robotic Arm sorts objects using color with the help of espcam and the movement is controlled by the servo motors attached in arm.
  Hardware:Robotic Arm kit,esp32 cam
  Software:Arduino IDE,VSCode.
  Working:
  Color Detection: Uses OpenCV to detect specific colors (orange, green, blue, red, white, yellow) in real-time via webcam.
  Object Tracking: Calculates the center of the detected color object and compares it with the center of the video frame.
  Direction Control: Determines movement direction (left, right, up, down) based on object position.
  Serial Communication: Sends movement commands to the Arduino (ESP32) via a serial port (COM3).
  Robotic Arm Movement: The Arduino receives the command and moves the servo motor of the robotic arm accordingly.
