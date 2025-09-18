import cv2
import mediapipe as mp
import math
import time

# Initialize MediaPipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Initialize a variable to store previous position of the index fingertip for swipe detection
prev_x, prev_y = None, None

# List to keep track of swipe gestures and their timestamps
active_swipes = []

def calculate_angle(landmark1, landmark2):
    """ Calculates the angle between two landmarks """
    return math.atan2(landmark2.y - landmark1.y, landmark2.x - landmark1.x)

def get_pointing_direction(landmarks):
    """ Determines the direction of pointing based on the index finger tip and wrist position """
    index_tip = landmarks.landmark[8]
    wrist = landmarks.landmark[0]
    
    # Calculate the angle between the index finger tip and the wrist
    angle = calculate_angle(wrist, index_tip)
    
    # Convert angle to degrees
    angle_degrees = math.degrees(angle)
    
    # Define direction based on angle
    if -45 <= angle_degrees <= 45:
        return "Pointing Left"
    elif 135 <= angle_degrees or angle_degrees <= -135:
        return "Pointing Right"
    elif 45 < angle_degrees < 135:
        return "Pointing Down"
    elif -135 < angle_degrees < -45:
        return "Pointing Up"
    
    return "Unknown Direction"

def is_swipe(landmarks):
    """ Determines if the gesture is a swipe based on the movement of the index finger """
    global prev_x, prev_y
    index_tip = landmarks.landmark[8]
    
    if prev_x is None or prev_y is None:
        prev_x, prev_y = index_tip.x, index_tip.y
        return None

    dx = index_tip.x - prev_x
    dy = index_tip.y - prev_y
    prev_x, prev_y = index_tip.x, index_tip.y

    # Detect swipe direction based on horizontal movement
    if dx > 0.1 and abs(dy) < 0.05:
        return "Swipe Right"
    elif dx < -0.1 and abs(dy) < 0.05:
        return "Swipe Left"
    
    return None

def display_active_swipes(frame):
    """ Display currently active swipe gestures on the frame """
    for swipe, timestamp in active_swipes:
        if time.time() - timestamp < 2:  # Show swipe for 2 seconds
            cv2.putText(frame, swipe, (10, 80 + 40 * active_swipes.index((swipe, timestamp))), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

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
            # Draw the hand landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Check for pointing direction
            direction = get_pointing_direction(hand_landmarks)
            if direction:
                cv2.putText(frame, direction, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)  # Pointing direction is displayed immediately

            # Check for swipe gesture
            swipe_gesture = is_swipe(hand_landmarks)
            if swipe_gesture:
                active_swipes.append((swipe_gesture + " Detected", time.time()))  # Store swipe gesture with timestamp

    # Display active swipe gestures on the frame
    display_active_swipes(frame)

    # Display the result
    cv2.imshow('Hand Gesture and Movement Detection', frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
