import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)  # Use the default camera
cap.set(3, 1280)  # Width of the video capture
cap.set(4, 720)   # Height of the video capture

detector = HandDetector(detectionCon=0.8)
colorR = (255, 0, 255)

grab_threshold = 30  # Distance threshold to consider as a grab gesture
release_threshold = 35  # Distance threshold to release the object
is_grabbing = False  # State to keep track of whether an object is currently grabbed

class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size
        self.isGrabbed = False  # Track if this rectangle is grabbed

    def update(self, cursor, isGrabbing):
        cx, cy = self.posCenter
        w, h = self.size

        # Check if cursor is inside the rectangle
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            if isGrabbing:
                self.posCenter = cursor
                self.isGrabbed = True
        else:
            if self.isGrabbed and isGrabbing:  # Move only if already grabbed
                self.posCenter = cursor
            elif not isGrabbing:
                self.isGrabbed = False  # Release if not grabbing anymore

singleRect = DragRect([640, 360])  # Center of the screen for 1280x720 resolution

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        for hand in hands:
            lmList = hand["lmList"]
            cursor = lmList[8][:2]  # Index finger tip position
            l, _, _ = detector.findDistance(lmList[8][:2], lmList[12][:2], img)  # Distance
            
            # Check for grabbing and releasing with hysteresis
            if not is_grabbing and l < grab_threshold:
                is_grabbing = True
            elif is_grabbing and l > release_threshold:
                is_grabbing = False

            singleRect.update(cursor, is_grabbing)

    imgNew = np.zeros_like(img, np.uint8)
    cx, cy = singleRect.posCenter
    w, h = singleRect.size
    cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)

    out = cv2.addWeighted(img, 0.5, imgNew, 0.5, 0)

    cv2.imshow("Image", out)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
