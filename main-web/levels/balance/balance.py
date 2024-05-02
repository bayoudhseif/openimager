import cv2
import numpy as np
import random
from cvzone.HandTrackingModule import HandDetector

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Initialize hand detector
detector = HandDetector(detectionCon=0.8)

# Define colors
color_rectangle = (30, 144, 255)  # Use Dodger Blue for the rectangle
color_grabbing = (50, 205, 50)  # Green when grabbing
color_planting_zone = (255, 0, 0)  # Red for the planting zone

# Define thresholds
grab_threshold = 30
release_threshold = 40
is_grabbing = False

# Define planting zone parameters
planting_zone_pos = [1000, 360]  # Position of the center of the planting zone
planting_zone_size = [200, 200]  # Size of the planting zone (width, height)
planting_count = 0  # Keep track of how many seeds have been planted
total_plants_required = 10  # Total number of plants required to end the game

# Define class for draggable rectangle
class DragRect:
    def __init__(self, pos_center, size=[200, 200]):
        self.pos_center = pos_center
        self.size = size
        self.is_grabbed = False

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
    margin = 50  # To ensure the zone does not spawn too close to the edges
    x = random.randint(margin + zone_width // 2, img_width - margin - zone_width // 2)
    y = random.randint(margin + zone_height // 2, img_height - margin - zone_height // 2)
    return [x, y]

# Initialize draggable rectangle
single_rect = DragRect([640, 360])

# Create window and set to fullscreen
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

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

# Main loop
while True:
    success, img = cap.read()
    if not success:
        break

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
    rectangle_color = color_grabbing if single_rect.is_grabbed else color_rectangle
    cv2.rectangle(img_new, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2),
                  rectangle_color, cv2.FILLED, cv2.LINE_AA)
    cv2.rectangle(img_new, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2),
                  (255, 255, 255), 2, cv2.LINE_AA)

    # Draw the planting zone
    pz_x, pz_y = planting_zone_pos
    pz_w, pz_h = planting_zone_size
    cv2.rectangle(img_new, (pz_x - pz_w // 2, pz_y - pz_h // 2), (pz_x + pz_w // 2, pz_y + pz_h // 2),
                  color_planting_zone, 2, cv2.LINE_AA)

    # Check if the rectangle is inside the planting zone and if the seed has been released
    if is_inside_planting_zone(single_rect.pos_center, planting_zone_pos, planting_zone_size) and not single_rect.is_grabbed:
        if planting_count < total_plants_required:  # Check if fewer than total plants required
            # Generate a new planting zone position, avoiding the current one
            planting_zone_pos = generate_new_planting_zone(planting_zone_pos, (1280, 720), planting_zone_size)
            planting_count += 1  # Increment the count of planted seeds
        elif planting_count == total_plants_required:  # If total required plants achieved
            cv2.putText(img_new, "All seeds planted!", (50, 50), font, font_scale, font_color, line_type)
            break  # End the loop/game

    # Display planting count
    cv2.putText(img_new, f"Planted: {planting_count}/{total_plants_required}", (50, 50), font, font_scale, font_color, line_type)

    # Display instructions
    for i, text in enumerate(instructions):
        cv2.putText(img_new, text, (50, 80 + i * 30), font, font_scale, font_color, line_type)

    out = cv2.addWeighted(img, 0.5, img_new, 0.5, 0)

    cv2.imshow("Image", out)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
