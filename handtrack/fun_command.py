import cv2
import mediapipe as mp
import math

# Initialize MediaPipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Variables to keep track of the last detected gestures
current_hand_gesture = None
movement_gesture = None
waving_state = None  # Track the current state of waving
last_direction = None  # Track the last detected direction of the wave
waved_once = False  # Track if we've already waved to avoid flooding

def is_waving(landmarks):
    """Detect if the hand is waving left or right."""
    global waving_state, last_direction, waved_once
    wrist = landmarks.landmark[0]
    index_tip = landmarks.landmark[8]

    # Determine the current direction of the wave
    if wrist.x < index_tip.x - 0.1:  # Waving to the right
        current_direction = "right"
    elif wrist.x > index_tip.x + 0.1:  # Waving to the left
        current_direction = "left"
    else:
        current_direction = None

    # State machine for detecting a complete wave
    if current_direction and current_direction != last_direction:
        # Direction changed, update the state
        if waving_state is None:
            waving_state = current_direction
        elif waving_state == current_direction:
            # A complete wave is detected when moving back
            if not waved_once:  # Check if we already detected a wave
                waved_once = True  # Set the flag to true
                last_direction = None
                waving_state = None
                return "Bye bye"
        else:
            waved_once = False  # Reset if the direction is the same

    # Update last direction
    last_direction = current_direction
    return None

def is_thumbs_up_or_down(landmarks):
    """Detect thumbs up or down gestures only when the hand is closed."""
    thumb_tip = landmarks.landmark[4]  # Tip of the thumb
    wrist = landmarks.landmark[0]  # Wrist position

    # Check if the other fingers are curled down (indicating a closed fist)
    index_tip = landmarks.landmark[8]
    middle_tip = landmarks.landmark[12]
    ring_tip = landmarks.landmark[16]
    pinky_tip = landmarks.landmark[20]

    # Check if all fingers except the thumb are curled down
    is_hand_closed = (index_tip.y > thumb_tip.y and
                      middle_tip.y > thumb_tip.y and
                      ring_tip.y > thumb_tip.y and
                      pinky_tip.y > thumb_tip.y)

    # Calculate distances for thumb orientation detection
    thumb_distance = thumb_tip.y - wrist.y
    index_distance = index_tip.y - wrist.y

    # Thumbs up: thumb is higher than the wrist
    if is_hand_closed and thumb_distance < 0:
        return "Thumbs Up"
    # Thumbs down: thumb is lower than the wrist
    elif is_hand_closed and thumb_distance > 0 and abs(thumb_tip.x - wrist.x) < 0.1:
        return "Thumbs Down"

    return None

def is_peace_sign(landmarks):
    """Detect the peace sign gesture."""
    index_tip = landmarks.landmark[8]  # Tip of the index finger
    middle_tip = landmarks.landmark[12]  # Tip of the middle finger
    thumb_tip = landmarks.landmark[4]  # Tip of the thumb

    # Check if the index and middle fingers are extended and thumb is down
    if (index_tip.y < thumb_tip.y) and (middle_tip.y < thumb_tip.y):
        return "Peace"
    
    return None

def is_middle_finger(landmarks):
    """Detect holding up the middle finger."""
    middle_tip = landmarks.landmark[12]  # Tip of the middle finger
    index_tip = landmarks.landmark[8]  # Tip of the index finger
    thumb_tip = landmarks.landmark[4]  # Tip of the thumb

    # Check if the middle finger is up and other fingers are down
    if (middle_tip.y < thumb_tip.y) and (index_tip.y > thumb_tip.y):
        return "Fuck you"

    return None

def update_current_gesture(landmarks):
    """Update the current hand gesture based on detected gestures."""
    global current_hand_gesture

    # Check for thumbs up/down
    thumb_gesture = is_thumbs_up_or_down(landmarks)
    if thumb_gesture:
        current_hand_gesture = thumb_gesture
        return

    # Check for peace sign gesture
    peace_gesture = is_peace_sign(landmarks)
    if peace_gesture:
        current_hand_gesture = peace_gesture
        return

    # Check for middle finger gesture
    middle_finger_gesture = is_middle_finger(landmarks)
    if middle_finger_gesture:
        current_hand_gesture = middle_finger_gesture
        return

    # If no recognized gesture, set to None
    current_hand_gesture = None

def display_active_gestures(frame):
    """Display currently active gestures on the frame."""
    # Display the hand gesture if recognized
    if current_hand_gesture:
        cv2.putText(frame, current_hand_gesture, (10, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the movement gesture if recognized
    if movement_gesture:
        cv2.putText(frame, movement_gesture, (10, 80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

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
            
            # Update current hand gesture based on landmarks
            update_current_gesture(hand_landmarks)

            # Check for waving gesture
            wave_gesture = is_waving(hand_landmarks)
            if wave_gesture:
                movement_gesture = wave_gesture  # Set the movement gesture to "Bye bye"
            else:
                movement_gesture = None  # Reset movement gesture if no wave is detected

    # Display active gestures on the frame
    display_active_gestures(frame)

    # Display the result
    cv2.imshow('Hand Gesture Detection', frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
