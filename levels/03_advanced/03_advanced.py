import cv2
import mediapipe as mp
import time
import random
import pygame
import threading
import subprocess

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

def play_piano_sequence():
    # Define the piano notes in sequence
    piano_notes = [
        pygame.mixer.Sound("levels/03_advanced/song2.mp3"),
    ]
    
    # Keep track of the elapsed time
    elapsed_time = 0

    # Play the piano notes in a loop
    while True:
        for note in piano_notes:
            if elapsed_time < note.get_length():
                note.play()
                time.sleep(note.get_length() - elapsed_time)  # Wait for the remaining duration
                elapsed_time = 0  # Reset elapsed time for the next note
            else:
                elapsed_time -= note.get_length()  # Update elapsed time for the next note

def main():
    cap = cv2.VideoCapture(0)  # Use camera 0
    detector = handDetector()
    gesture_count = 0  # Initialize a counter for correct gestures
    previous_number = 0
    current_number = random.randint(1, 5)
    display_text = f"Show {current_number} fingers"
    last_gesture_time = time.time()  # Initialize the time of the last gesture

    # Initialize pygame mixer
    pygame.mixer.init()

    # Start playing the piano sequence
    play_piano_sequence_thread = threading.Thread(target=play_piano_sequence)
    play_piano_sequence_thread.start()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        
        if lmList:
            fingers_count = detector.countFingers(img, lmList)
            if fingers_count == current_number:
                gesture_count += 1  # Increment the count for each correct gesture
                last_gesture_time = time.time()  # Update the time of the last gesture
                # Prepare for the next round
                previous_number = current_number
                while previous_number == current_number:
                    current_number = random.randint(1, 5)
                display_text = f"Show {current_number} fingers"
                # Unpause the piano sequence if paused
                pygame.mixer.unpause()

            cv2.putText(img, display_text, (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        # Check if the user hasn't made a gesture in the last 5 seconds
        if time.time() - last_gesture_time > 0.8:
            # Pause the piano sequence
            pygame.mixer.pause()

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.quit()

    # After the level is completed or closed
    subprocess.Popen(["python", "main.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)

if __name__ == "__main__":
    main()
