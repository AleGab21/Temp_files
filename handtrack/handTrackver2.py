import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

def is_fist(landmarks):
    """ Determines if the gesture is a fist by comparing fingertip positions to palm """
    # Finger tip indices in MediaPipe are: 8 (index), 12 (middle), 16 (ring), 20 (pinky)
    tips = [8, 12, 16, 20]
    for tip in tips:
        if landmarks.landmark[tip].y < landmarks.landmark[tip - 2].y:  # Checking if finger is folded
            return False
    return True

def is_open_palm(landmarks):
    """ Determines if the gesture is an open palm """
    tips = [8, 12, 16, 20]
    for tip in tips:
        if landmarks.landmark[tip].y > landmarks.landmark[tip - 2].y:  # Checking if fingers are extended
            return False
    return True

# Initialize a variable to store previous position of the index fingertip
prev_x, prev_y = None, None

def is_swipe(landmarks):
    global prev_x, prev_y
    index_tip = landmarks.landmark[8]
    
    if prev_x is None or prev_y is None:
        prev_x, prev_y = index_tip.x, index_tip.y
        return False

    dx = index_tip.x - prev_x
    dy = index_tip.y - prev_y
    prev_x, prev_y = index_tip.x, index_tip.y

    # Detect right swipe
    if dx > 0.1 and abs(dy) < 0.05:
        return "Swipe Right"
    elif dx < -0.1 and abs(dy) < 0.05:
        return "Swipe Left"
    return None

# Start video capture from webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and detect hands
    result = hands.process(rgb_frame)

    # Analyze landmarks and recognize gestures
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            if is_fist(hand_landmarks):
                cv2.putText(frame, "Fist Detected", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif is_open_palm(hand_landmarks):
                cv2.putText(frame, "Open Palm Detected", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the result
    cv2.imshow('Hand Gesture Recognition', frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
