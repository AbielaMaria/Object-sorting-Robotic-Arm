import cv2
import numpy as np
import serial  # Import serial library

# Initialize serial communication with Arduino
arduino = serial.Serial('COM3', 9600)  # Replace 'COM3' with your Arduino port


def nothing(x):
    pass


color_ranges = {
    'orange': ([0, 85, 108], [19, 194, 201]),
    'green': ([40, 50, 50], [80, 255, 255]),
    'blue': ([83, 50, 50], [120, 250, 255]),
    'red': ([170, 49, 50], [180, 255, 255]),
    'white': ([0, 10, 108], [255, 76, 17]),
    'yellow': ([19, 50, 50], [57, 123, 255])
}

cap = cv2.VideoCapture(0)
cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_height, frame_width = frame.shape[:2]
    frame_center_x = frame_width // 2
    frame_center_y = frame_height // 2

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for color_name, (lower_bound, upper_bound) in color_ranges.items():
        lower_bound = np.array(lower_bound)
        upper_bound = np.array(upper_bound)
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        cnts, _ = cv2.findContours(
            mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            area = cv2.contourArea(c)
            if area > 5000:
                cv2.drawContours(frame, [c], -1, (255, 0, 0), 3)
                M = cv2.moments(c)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)
                cv2.putText(frame, color_name, (cx - 20, cy - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                direction = ""
                if cx < frame_center_x - 50:
                    direction += "Move Left"
                elif cx > frame_center_x + 50:
                    direction += "Move Right"
                if cy < frame_center_y - 50:
                    direction += "Move Up"
                elif cy > frame_center_y + 50:
                    direction += "Move Down"

                print(f"Detected {color_name}: {direction}")
                cv2.putText(frame, direction, (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                if direction:
                    # Send command to Arduino
                    arduino.write((direction + '\n').encode())

    cv2.imshow("live transmission", frame)
    key = cv2.waitKey(5)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()  # Close serial connection when done
