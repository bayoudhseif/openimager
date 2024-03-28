import cv2
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self, detectionCon=0.5, trackCon=0.5):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(min_detection_confidence=detectionCon, 
                                        min_tracking_confidence=trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        return img

    def findDistance(self, img, handNo=0):
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNo]
            landmarks = hand.landmark
            thumb_tip = landmarks[self.mpHands.HandLandmark.THUMB_TIP]
            index_finger_tip = landmarks[self.mpHands.HandLandmark.INDEX_FINGER_TIP]
            x1, y1 = int(thumb_tip.x * img.shape[1]), int(thumb_tip.y * img.shape[0])
            x2, y2 = int(index_finger_tip.x * img.shape[1]), int(index_finger_tip.y * img.shape[0])
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            length = math.hypot(x2 - x1, y2 - y1)
            return length, img
        return 0, img

def main():
    cap = cv2.VideoCapture(0) # Adjust camera index if necessary
    detector = handDetector()
    while True:
        success, img = cap.read()
        if not success:
            continue
        img = detector.findHands(img)
        length, img = detector.findDistance(img)
        print(f"Distance: {length}") # Print distance for demonstration
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
