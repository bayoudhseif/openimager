import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import random

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

# Snake properties
snake_color = (0, 255, 0)  # Green
treat_color = (0, 0, 255)  # Red
snake_size = 20
treat_size = 20
treat_pos = [random.randint(100, 1180), random.randint(100, 620)]
score = 0
snake_body = [[640, 360]]  # Starting position of the snake

def add_treat():
    return [random.randint(100, 1180), random.randint(100, 620)]

def check_collision_with_treat(head, treat):
    dx = head[0] - treat[0]
    dy = head[1] - treat[1]
    distance = np.sqrt(dx**2 + dy**2)
    return distance < (snake_size + treat_size) / 2

def check_self_collision(snake_body):
    head = snake_body[0]
    return head in snake_body[1:]

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, draw=False)

    if hands:
        # Make sure the landmarks list is not empty before accessing it
        if hands[0].get("lmList"):
            # Use the index finger tip position as the head of the snake
            index_finger_tip = hands[0]["lmList"][8][:2]  # Index finger tip position
            snake_head = index_finger_tip
            snake_body.insert(0, list(snake_head))  # Move the snake based on index finger position

            if check_collision_with_treat(snake_head, treat_pos):
                score += 1
                treat_pos = add_treat()  # Generate new treat
            else:
                if len(snake_body) > 1:
                    snake_body.pop()  # Keep the snake the same length unless it has eaten a treat

            if check_self_collision(snake_body):
                print("Game Over. Score:", score)
                break  # End the game if the snake collides with itself

    # Draw the treat
    cv2.circle(img, tuple(treat_pos), treat_size, treat_color, cv2.FILLED)

    # Draw the snake
    for segment in snake_body:
        cv2.circle(img, tuple(segment), snake_size, snake_color, cv2.FILLED)

    cv2.imshow("Snake Game", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
