import cv2
import numpy as np
import random
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

color_rectangle = (30, 144, 255)  # Use Dodger Blue for the rectangle
color_grabbing = (50, 205, 50)  # Green when grabbing
color_planting_zone = (255, 0, 0)  # Red for the planting zone

grab_threshold = 30
release_threshold = 40
is_grabbing = False

# Initial planting zone position
planting_zone_pos = [1000, 360]  # Position of the center of the planting zone
planting_zone_size = [200, 200]  # Size of the planting zone (width, height)
planting_count = 0  # Keep track of how many seeds have been planted


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
            if self.is_grabbed and is_grabbing:
                self.pos_center = cursor
            elif not is_grabbing:
                self.is_grabbed = False


def is_inside_planting_zone(rect_pos, zone_pos, zone_size):
    rx, ry = rect_pos
    zx, zy = zone_pos
    zw, zh = zone_size

    return zx - zw // 2 < rx < zx + zw // 2 and zy - zh // 2 < ry < zy + zh // 2


def generate_new_planting_zone(exclude_pos, img_size, zone_size):
    img_width, img_height = img_size
    zone_width, zone_height = zone_size
    margin = 50  # To ensure the zone does not spawn too close to the edges
    x = random.randint(margin + zone_width // 2, img_width - margin - zone_width // 2)
    y = random.randint(margin + zone_height // 2, img_height - margin - zone_height // 2)
    return [x, y]


single_rect = DragRect([640, 360])

cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_color = (255, 255, 255)
line_type = 2

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
    cv2.rectangle(img_new, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), rectangle_color, cv2.FILLED)

    # Draw the planting zone
    pz_x, pz_y = planting_zone_pos
    pz_w, pz_h = planting_zone_size
    cv2.rectangle(img_new, (pz_x - pz_w // 2, pz_y - pz_h // 2), (pz_x + pz_w // 2, pz_y + pz_h // 2),
                  color_planting_zone, 2)

    # Check if the rectangle is inside the planting zone and if the seed has been released
    if is_inside_planting_zone(single_rect.pos_center, planting_zone_pos, planting_zone_size) and not single_rect.is_grabbed:
        if planting_count < 5:  # Check if fewer than 6 seeds have been planted
            # Generate a new planting zone position, avoiding the current one
            planting_zone_pos = generate_new_planting_zone(planting_zone_pos, (1280, 720), planting_zone_size)
            planting_count += 1  # Increment the count of planted seeds
        elif planting_count == 5:  # If this was the 6th successful planting
            cv2.putText(img_new, "All seeds planted!", (50, 50), font, font_scale, font_color, line_type)
            break  # Optionally end the loop/game or reset for a new game

    # Display planting count
    cv2.putText(img_new, f"Planted: {planting_count}/5", (50, 50), font, font_scale, font_color, line_type)

    out = cv2.addWeighted(img, 0.5, img_new, 0.5, 0)

    cv2.imshow("Image", out)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
