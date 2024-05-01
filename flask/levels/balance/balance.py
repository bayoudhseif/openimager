import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import random
import subprocess

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)
colorR = (30, 144, 255)  # Use Dodger Blue for the rectangle
colorGrabbing = (50, 205, 50)  # Green when grabbing
colorPlantingZone = (255, 0, 0)  # Red for the planting zone

grab_threshold = 30
release_threshold = 40
is_grabbing = False

# Initial planting zone position
plantingZonePos = [1000, 360]  # Position of the center of the planting zone
plantingZoneSize = [200, 200]  # Size of the planting zone (width, height)
plantingCount = 0  # Keep track of how many seeds have been planted

class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size
        self.isGrabbed = False

    def update(self, cursor, isGrabbing):
        cx, cy = self.posCenter
        w, h = self.size

        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            if isGrabbing:
                self.posCenter = cursor
                self.isGrabbed = True
        else:
            if self.isGrabbed and isGrabbing:
                self.posCenter = cursor
            elif not isGrabbing:
                self.isGrabbed = False

def isInsidePlantingZone(rectPos, zonePos, zoneSize):
    rx, ry = rectPos
    zx, zy = zonePos
    zw, zh = zoneSize

    return zx - zw // 2 < rx < zx + zw // 2 and zy - zh // 2 < ry < zy + zh // 2

def generateNewPlantingZone(exclude_pos, img_size, zone_size):
    img_width, img_height = img_size
    zone_width, zone_height = zone_size
    margin = 50  # To ensure the zone does not spawn too close to the edges
    x = random.randint(margin + zone_width // 2, img_width - margin - zone_width // 2)
    y = random.randint(margin + zone_height // 2, img_height - margin - zone_height // 2)
    return [x, y]

singleRect = DragRect([640, 360])

cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, draw=False)

    if hands:
        for hand in hands:
            lmList = hand["lmList"]
            cursor = lmList[8][:2]
            l, _, _ = detector.findDistance(lmList[8][:2], lmList[12][:2], img)

            if not is_grabbing and l < grab_threshold:
                is_grabbing = True
            elif is_grabbing and l > release_threshold:
                is_grabbing = False

            singleRect.update(cursor, is_grabbing)

    imgNew = np.zeros_like(img, np.uint8)
    cx, cy = singleRect.posCenter
    w, h = singleRect.size
    rectangleColor = colorGrabbing if singleRect.isGrabbed else colorR
    cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), rectangleColor, cv2.FILLED)

    # Draw the planting zone
    pz_x, pz_y = plantingZonePos
    pz_w, pz_h = plantingZoneSize
    cv2.rectangle(imgNew, (pz_x - pz_w // 2, pz_y - pz_h // 2), (pz_x + pz_w // 2, pz_y + pz_h // 2), colorPlantingZone, 2)

    # Check if the rectangle is inside the planting zone and if the seed has been released
    if isInsidePlantingZone(singleRect.posCenter, plantingZonePos, plantingZoneSize) and not singleRect.isGrabbed:
        if plantingCount < 5:  # Check if fewer than 6 seeds have been planted
            # Generate a new planting zone position, avoiding the current one
            plantingZonePos = generateNewPlantingZone(plantingZonePos, (1280, 720), plantingZoneSize)
            plantingCount += 1  # Increment the count of planted seeds
        elif plantingCount == 5:  # If this was the 6th successful planting
            print("All seeds planted!")  # Indicate game completion (or replace with visual/auditory feedback)
            break  # Optionally end the loop/game or reset for a new game

    out = cv2.addWeighted(img, 0.5, imgNew, 0.5, 0)

    cv2.imshow("Image", out)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# After the level is completed or closed
subprocess.Popen(["python", "main.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
