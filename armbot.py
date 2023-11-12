import mediapipe as mp
import cv2
import serial
import time

# Connect to Arduino over serial
arduino = serial.Serial('COM8', 9600, timeout=1)  # Change 'COM8' to your Arduino port

# Create a MediaPipe Hands instance
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Initialize the hand landmark model
with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5) as hands:
    cap = cv2.VideoCapture(0)  # Open the default camera

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture frame from the camera.")
            break

        # Resize the frame to reduce processing load
        frame = cv2.resize(frame, (640, 480))

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                thumb_tip = landmarks.landmark[4]
                index_tip = landmarks.landmark[8]

                x = int(thumb_tip.x * 1000)  # Multiply by 1000 for more precision
                y = int(thumb_tip.y * 1000)

                # Send x, y coordinates to Arduino as a string
                command = f"{x},{y}\n"
                arduino.write(command.encode())

                mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow('Hand Tracking', frame)

        # Introduce a small delay to reduce the frame rate
        time.sleep(0.01)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    arduino.close()
    cv2.destroyAllWindows()
