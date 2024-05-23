import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import random

def generate_frames():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # Set video width
    cap.set(4, 720)   # Set video height

    detector = HandDetector(detectionCon=0.8, maxHands=2)
    colorR = (30, 144, 255)  # Dodger Blue for the rectangle
    colorGrabbing = (50, 205, 50)  # Green when grabbing
    colorPlantingZone = (255, 0, 0)  # Red for the planting zone

    grab_threshold = 30
    release_threshold = 40
    is_grabbing = False

    # Initial planting zone position
    plantingZonePos = [1000, 360]
    plantingZoneSize = [200, 200]
    plantingCount = 0

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
                    self.isGrabbed = False
            elif not isGrabbing:
                self.isGrabbed = False

    singleRect = DragRect([640, 360])

    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)  # Flip the image horizontally for a laterally correct view
        hands, img = detector.findHands(img, draw=False)  # Find and draw hands

        if hands:
            hand = hands[0]
            lmList = hand["lmList"]  # List of 21 Landmark points
            cursor = lmList[8][:2]  # Index finger tip landmarks
            length, info, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)  # Find distance between index and middle fingers

            if length < grab_threshold:
                is_grabbing = True
            elif length > release_threshold:
                is_grabbing = False

            singleRect.update(cursor, is_grabbing)

        cx, cy = singleRect.posCenter
        w, h = singleRect.size
        color = colorGrabbing if singleRect.isGrabbed else colorR
        cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), color, cv2.FILLED)

        # Draw planting zone
        pz_x, pz_y = plantingZonePos
        pz_w, pz_h = plantingZoneSize
        cv2.rectangle(img, (pz_x - pz_w // 2, pz_y - pz_h // 2), (pz_x + pz_w // 2, pz_y + pz_h // 2), colorPlantingZone, 2)

        # Check if the rectangle is inside the planting zone
        if singleRect.isGrabbed == False and pz_x - pz_w // 2 < cx < pz_x + pz_w // 2 and pz_y - pz_h // 2 < cy < pz_y + pz_h // 2:
            if plantingCount < 5:
                plantingZonePos = [random.randint(100, 1180), random.randint(100, 620)]
                plantingCount += 1
            elif plantingCount == 5:
                print("All seeds planted!")

        # Encode the frame in JPEG format
        (flag, encodedImage) = cv2.imencode(".jpg", img)
        if not flag:
            continue

        # Yield the byte stream, this will be sent to the client
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()

