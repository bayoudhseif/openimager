import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)
colorR = (30, 144, 255)  # Use Dodger Blue for the rectangle
colorGrabbing = (50, 205, 50)  # Green when grabbing
colorCursor = (70, 130, 180)  # Steel Blue for cursor
colorLandmarks = (255, 215, 0)  # Gold for hand landmarks

grab_threshold = 30
release_threshold = 40
is_grabbing = False

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

singleRect = DragRect([640, 360])

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, draw=True)  # Don't draw default dots

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

    out = cv2.addWeighted(img, 0.5, imgNew, 0.5, 0)

    cv2.imshow("Image", out)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
