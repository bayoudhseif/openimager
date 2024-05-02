import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import random
import subprocess

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Initialize the hand detector
detector = HandDetector(detectionCon=0.8)

# Before your while loop
cv2.namedWindow("Snake Game", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Snake Game", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

def initialize_game():
    # Resets or initializes the game state for a new game
    return {
        "treat_pos": [random.randint(100, 1180), random.randint(100, 620)],
        "score": 0,
        "snake_body": [[640, 360]],  # Starting position
        "game_over": False,
    }

def add_treat():
    # Generates a new position for the treat
    return [random.randint(100, 1180), random.randint(100, 620)]

def check_collision_with_treat(head, treat, tolerance=20):
    # Checks if the snake's head has collided with a treat
    dx = head[0] - treat[0]
    dy = head[1] - treat[1]
    distance = np.sqrt(dx**2 + dy**2)
    return distance < tolerance

def check_self_collision(snake_body):
    # Checks if the snake has collided with itself
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

# After the level is completed or closed
subprocess.Popen(["python", "main.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
