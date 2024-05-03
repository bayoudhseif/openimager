import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import random

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Initialize hand detector
detector = HandDetector(detectionCon=0.8)

# Before your while loop
cv2.namedWindow("Snake Game", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Snake Game", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Font settings for instructions
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.8
font_color = (255, 255, 255)
line_type = 2

# Instructions to display
instructions = [
    "Use your index finger to control the snake's direction.",
    "Eat the red dots to grow longer and increase your score.",
]

# Function to initialize game state
def initialize_game():
    return {
        "treat_pos": [random.randint(100, 1180), random.randint(100, 620)],
        "score": 0,
        "snake_body": [[640, 360]],  # Starting position
        "game_over": False,
    }

# Function to add a new treat
def add_treat():
    return [random.randint(100, 1180), random.randint(100, 620)]

# Function to check collision with treat
def check_collision_with_treat(head, treat, tolerance=20):
    dx = head[0] - treat[0]
    dy = head[1] - treat[1]
    distance = np.sqrt(dx**2 + dy**2)
    return distance < tolerance

# Function to check self collision
def check_self_collision(snake_body):
    head = snake_body[0]
    return head in snake_body[1:]

# Main game loop
game_running = True
while game_running:
    game_state = initialize_game()

    while not game_state["game_over"]:
        success, img = cap.read()
        if not success:
            continue

        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, draw=False)

        if hands:
            index_finger_tip = hands[0]["lmList"][8][:2]
            if len(game_state["snake_body"]) < 2 or not check_self_collision([index_finger_tip] + game_state["snake_body"][1:]):
                game_state["snake_body"].insert(0, list(index_finger_tip))  # Move the snake
                if check_collision_with_treat(index_finger_tip, game_state["treat_pos"], tolerance=25):
                    game_state["score"] += 1
                    game_state["treat_pos"] = add_treat()  # Add new treat
                else:
                    game_state["snake_body"].pop()  # Keep the snake's length constant
            else:
                game_state["game_over"] = True  # End game condition

        # Drawing
        cv2.circle(img, tuple(game_state["treat_pos"]), 10, (0, 0, 255), cv2.FILLED)  # Draw the treat
        for segment in game_state["snake_body"]:
            cv2.circle(img, tuple(segment), 10, (0, 255, 0), cv2.FILLED)  # Draw the snake
        
        # Display score
        cv2.putText(img, f"Score: {game_state['score']}", (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        
        # Display instructions
        for i, text in enumerate(instructions):
            cv2.putText(img, text, (50, 80 + i * 30), font, font_scale, font_color, line_type)

        cv2.imshow("Snake Game", img)

        if game_state["score"] >= 30 or cv2.waitKey(1) & 0xFF == ord('q'):
            game_running = False
            break

    if game_state["game_over"]:
        # Wait for a key press before restarting
        print(f"Game Over. Final Score: {game_state['score']}")
        cv2.waitKey(1000)  # Wait a bit before potentially restarting

cap.release()
cv2.destroyAllWindows()
