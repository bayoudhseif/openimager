import cv2
import mediapipe as mp
import time
import random
import pygame

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode,
                                        max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw and id == 0:  # Example for drawing circles on the wrist
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmList

    def countFingers(self, img, lmList):
        if len(lmList) != 0:
            fingers = []

            # Thumb
            if lmList[self.tipIds[0]][1] > lmList[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Fingers
            for id in range(1, 5):
                if lmList[self.tipIds[id]][2] < lmList[self.tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            
            return fingers.count(1)
        return 0

def play_piano_sequence(sequence_number):
    # Define the piano notes in sequence
    piano_notes = [
        pygame.mixer.Sound("levels/03_advanced/deprecated/do.mp3"),
        pygame.mixer.Sound("levels/03_advanced/deprecated/re.mp3"),
        pygame.mixer.Sound("levels/03_advanced/deprecated/mi.mp3"),
        pygame.mixer.Sound("levels/03_advanced/deprecated/fa.mp3"),
        pygame.mixer.Sound("levels/03_advanced/deprecated/sol.mp3")
    ]
    
    # Play the piano note based on the sequence number
    note_index = (sequence_number - 1) % len(piano_notes)
    piano_notes[note_index].play()

def main():
    cap = cv2.VideoCapture(0)  # Use camera 0
    detector = handDetector()
    gesture_count = 0  # Initialize a counter for correct gestures
    previous_number = 0
    current_number = random.randint(1, 5)
    display_text = f"Show {current_number} fingers"

    # Initialize pygame mixer
    pygame.mixer.init()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        
        if lmList:
            fingers_count = detector.countFingers(img, lmList)
            if fingers_count == current_number:
                gesture_count += 1  # Increment the count for each correct gesture
                play_piano_sequence(gesture_count)  # Play the note based on the sequence of correct gestures

                # Prepare for the next round
                previous_number = current_number
                while previous_number == current_number:
                    current_number = random.randint(1, 5)
                display_text = f"Show {current_number} fingers"

            cv2.putText(img, display_text, (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()
