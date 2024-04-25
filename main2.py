import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Function to run an example script.
def run_script(script_id):
    print(f"Running Script {script_id}")

# Determine screen size
screen_width, screen_height = 1920, 1080  # Adjust this to your screen's resolution if needed

# Button properties, scaled based on screen size
buttons = [
    {"name": "Script 1", "rect": [50, 100, 300, 200], "action": lambda: run_script(1)},
    {"name": "Script 2", "rect": [350, 100, 300, 200], "action": lambda: run_script(2)},
    {"name": "Script 3", "rect": [650, 100, 300, 200], "action": lambda: run_script(3)},
]

# Check if a point is inside a rectangle
def is_inside_rect(point, rect):
    x, y = point
    rx, ry, rw, rh = rect
    return rx < x < rx + rw and ry < y < ry + rh

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

cv2.namedWindow('Hand-Controlled UI', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Hand-Controlled UI', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    frame_height, frame_width, _ = frame.shape

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_x, index_y = int(index_tip.x * frame_width), int(index_tip.y * frame_height)

            for button in buttons:
                if is_inside_rect((index_x, index_y), button["rect"]):
                    cv2.rectangle(frame, (button["rect"][0], button["rect"][1]), (button["rect"][0] + button["rect"][2], button["rect"][1] + button["rect"][3]), (0, 255, 0), -1)
                    # Check for click gesture
                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    distance = np.linalg.norm([thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y])
                    if distance < 0.02:  # Threshold for "click"
                        button["action"]()
                else:
                    cv2.rectangle(frame, (button["rect"][0], button["rect"][1]), (button["rect"][0] + button["rect"][2], button["rect"][1] + button["rect"][3]), (255, 0, 0), -1)

    # Display the buttons
    for button in buttons:
        cv2.putText(frame, button["name"], (button["rect"][0] + 10, button["rect"][1] + 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Hand-Controlled UI', frame)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
