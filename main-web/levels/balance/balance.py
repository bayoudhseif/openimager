import cv2
import numpy as np
import random
from cvzone.HandTrackingModule import HandDetector
import os
import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Create Pygame window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Get screen size
screen_width, screen_height = screen.get_size()

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(3, screen_width)
cap.set(4, screen_height)

# Initialize hand detector
detector = HandDetector(detectionCon=0.8)

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Load images for the draggable box and the planting zone
box_image_path = os.path.join(script_dir, 'box.png')
zone_image_path = os.path.join(script_dir, 'plot.png')

box_image = cv2.imread(box_image_path)  # Make sure 'box.png' is in your script directory
zone_image = cv2.imread(zone_image_path)  # Make sure 'zone.png' is in your script directory

if box_image is None or zone_image is None:
    raise Exception("Images not found, please check the paths.")

# Define thresholds
grab_threshold = 30
release_threshold = 40
is_grabbing = False

# Define planting zone parameters
planting_zone_pos = [1000, 360]  # Position of the center of the planting zone
planting_zone_size = [zone_image.shape[1], zone_image.shape[0]]
planting_count = 0  # Keep track of how many seeds have been planted
total_plants_required = 10  # Total number of plants required to end the game

# Define class for draggable rectangle (now with images)
class DragRect:
    def __init__(self, pos_center, image):
        self.pos_center = pos_center
        self.image = image
        self.is_grabbed = False
        self.size = [image.shape[1], image.shape[0]]

    def update(self, cursor, is_grabbing):
        cx, cy = self.pos_center
        w, h = self.size

        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            if is_grabbing:
                self.pos_center = cursor
                self.is_grabbed = True
            else:
                self.is_grabbed = False
        else:
            if self.is_grabbed and is_grabbing:
                self.pos_center = cursor
            elif not is_grabbing:
                self.is_grabbed = False

# Initialize draggable rectangle with an image
single_rect = DragRect([640, 360], box_image)

# Font settings for instructions
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.8
font_color = (255, 255, 255)
line_type = 2

# Instructions to display
instructions = [
    "Keep your hand wide open and touch all fingers together to grab the box.",
    "While still holding, move the block to the correct plot."
]

# Function to check if a point is inside a rectangle
def is_inside_planting_zone(rect_pos, zone_pos, zone_size):
    rx, ry = rect_pos
    zx, zy = zone_pos
    zw, zh = zone_size

    return zx - zw // 2 < rx < zx + zw // 2 and zy - zh // 2 < ry < zy + zh // 2

# Function to generate a new planting zone position
def generate_new_planting_zone(exclude_pos, img_size, zone_size):
    img_width, img_height = img_size
    zone_width, zone_height = zone_size
    margin = 100  # To ensure the zone does not spawn too close to the edges
    x = random.randint(margin + zone_width // 2, img_width - margin - zone_width // 2)
    y = random.randint(margin + zone_height // 2, img_height - margin - zone_height // 2)
    return [x, y]

# Main loop
while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture video frame.")
        continue  # Skip the rest of the loop and try to get another frame

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, draw=False)

    if hands:
        for hand in hands:
            lm_list = hand["lmList"]
            cursor = lm_list[8][:2]
            l, _, _ = detector.findDistance(lm_list[8][:2], lm_list[12][:2], img)

            if not is_grabbing and l < grab_threshold:
                is_grabbing = True
            elif is_grabbing and l > release_threshold:
                is_grabbing = False

            single_rect.update(cursor, is_grabbing)

    img_new = np.zeros_like(img, np.uint8)
    cx, cy = single_rect.pos_center
    w, h = single_rect.size

    # Ensure the image placements do not go out of bounds
    start_x = max(0, cx - w // 2)
    start_y = max(0, cy - h // 2)
    end_x = min(img.shape[1], cx + w // 2)
    end_y = min(img.shape[0], cy + h // 2)

    # Ensure we don't exceed the array bounds
    if start_x < end_x and start_y < end_y:
        img_new[start_y:end_y, start_x:end_x] = single_rect.image[start_y-cy+h//2:end_y-cy+h//2, start_x-cx+w//2:end_x-cx+w//2]

    # Place the planting zone image
    pz_x, pz_y = planting_zone_pos
    pz_w, pz_h = planting_zone_size
    pz_start_x = max(0, pz_x - pz_w // 2)
    pz_start_y = max(0, pz_y - pz_h // 2)
    pz_end_x = min(img.shape[1], pz_x + pz_w // 2)
    pz_end_y = min(img.shape[0], pz_y + pz_h // 2)

    if pz_start_x < pz_end_x and pz_start_y < pz_end_y:
        img_new[pz_start_y:pz_end_y, pz_start_x:pz_end_x] = zone_image[pz_start_y-pz_y+pz_h//2:pz_end_y-pz_y+pz_h//2, pz_start_x-pz_x+pz_w//2:pz_end_x-pz_x+pz_w//2]

    # Check if the rectangle is inside the planting zone and if the seed has been released
    if is_inside_planting_zone(single_rect.pos_center, planting_zone_pos, planting_zone_size) and not single_rect.is_grabbed:
        if planting_count < total_plants_required:  # Check if fewer than total plants required
            planting_zone_pos = generate_new_planting_zone(planting_zone_pos, (screen_width, screen_height), planting_zone_size)
            planting_count += 1

            new_rect_pos = generate_new_planting_zone(planting_zone_pos, (screen_width, screen_height), planting_zone_size)
            while is_inside_planting_zone(new_rect_pos, planting_zone_pos, planting_zone_size):
                new_rect_pos = generate_new_planting_zone(planting_zone_pos, (screen_width, screen_height), planting_zone_size)
            single_rect.pos_center = new_rect_pos
        elif planting_count == total_plants_required:
            cv2.putText(img_new, "All seeds planted!", (50, 50), font, font_scale, font_color, line_type)
            break

    cv2.putText(img_new, f"Planted: {planting_count}/{total_plants_required}", (50, 50), font, font_scale, font_color, line_type)

    for i, text in enumerate(instructions):
        cv2.putText(img_new, text, (50, 80 + i * 30), font, font_scale, font_color, line_type)

    out = cv2.addWeighted(img, 0.6, img_new, 0.4, 0)

    # Convert image to Pygame surface and display it
    out_rgb = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
    out_pygame = pygame.image.fromstring(out_rgb.tostring(), out_rgb.shape[1::-1], "RGB")
    screen.blit(out_pygame, (0, 0))
    pygame.display.flip()

    # Check for Pygame events
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
            pygame.quit()
            cap.release()
            cv2.destroyAllWindows()
            quit()
