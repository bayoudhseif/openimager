import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import random
import pygame
import sys

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)

# Initialize hand detector
detector = HandDetector(detectionCon=0.8)

# Initialize pygame
pygame.init()
display_info = pygame.display.Info()
screen = pygame.display.set_mode((display_info.current_w, display_info.current_h), pygame.FULLSCREEN)
pygame.display.set_caption("Snake Game")

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
        # Draw the treat with white outline
        cv2.circle(img, tuple(game_state["treat_pos"]), 12, (255, 255, 255), cv2.FILLED)  # White outline
        cv2.circle(img, tuple(game_state["treat_pos"]), 10, (220, 204, 138), cv2.FILLED)  # Lighter treat color

        # Draw the snake with white outline
        for segment in game_state["snake_body"]:
            cv2.rectangle(img, (segment[0] - 9, segment[1] - 9), (segment[0] + 9, segment[1] + 9), (255, 255, 255), cv2.FILLED)  # White outline
            cv2.rectangle(img, (segment[0] - 7, segment[1] - 7), (segment[0] + 7, segment[1] + 7), (51, 27, 10), cv2.FILLED)  # Lighter snake color

        # Before displaying the image, blend text with video
        text_image = np.zeros_like(img, dtype=np.uint8)  # Create a blank image for text

        # Display score
        cv2.putText(text_image, f"Score: {game_state['score']}/30", (50, 50), font, font_scale, font_color, line_type)

        # Display instructions
        for i, text in enumerate(instructions):
            cv2.putText(text_image, text, (50, 80 + i * 30), font, font_scale, font_color, line_type)

        # Blend text image with video frame
        blended_img = cv2.addWeighted(img, 0.6, text_image, 0.4, 0)

        # Convert the blended image to Pygame format
        blended_img = cv2.cvtColor(blended_img, cv2.COLOR_BGR2RGB)
        blended_img = np.rot90(blended_img)
        blended_img = pygame.surfarray.make_surface(blended_img)
        blended_img = pygame.transform.scale(blended_img, (display_info.current_w, display_info.current_h))
        blended_img = pygame.transform.flip(blended_img, True, False)

        screen.blit(blended_img, (0, 0))
        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                game_running = False
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()

        if game_state["score"] >= 30:
            game_running = False
            break

    if game_state["game_over"]:
        print(f"Game Over. Final Score: {game_state['score']}")
        cv2.waitKey(1000)  # Wait a bit before potentially restarting

cap.release()
cv2.destroyAllWindows()
pygame.quit()


