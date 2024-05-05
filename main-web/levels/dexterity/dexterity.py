import cv2
import mediapipe as mp
import time
import random
import pygame
import threading
import numpy as np
import sys

class handDetector:
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
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
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

    def countFingers(self, lmList):
        if lmList:
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


def play_piano_sequence(gesture_made):
    piano_notes = [pygame.mixer.Sound("levels/dexterity/song.mp3")]
    elapsed_time = 0

    while True:
        if gesture_made.is_set():
            for note in piano_notes:
                if elapsed_time < note.get_length():
                    note.play()
                    time.sleep(note.get_length() - elapsed_time)
                    elapsed_time = 0
                else:
                    elapsed_time -= note.get_length()
                if gesture_made.is_set():
                    continue


def main():
    # Initialize pygame and create a fullscreen window
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Image")

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    detector = handDetector()
    gesture_count = 0
    previous_number = 0
    current_number = random.randint(1, 5)
    last_gesture_time = time.time()
    gesture_made = threading.Event()

    pygame.mixer.init()
    play_piano_sequence_thread = threading.Thread(target=play_piano_sequence, args=(gesture_made,))
    play_piano_sequence_thread.daemon = True
    play_piano_sequence_thread.start()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        img = cv2.flip(img, 1)

        if lmList:
            fingers_count = detector.countFingers(lmList)
            if fingers_count == current_number:
                gesture_made.set()
                gesture_count += 1
                last_gesture_time = time.time()
                previous_number = current_number
                while previous_number == current_number:
                    current_number = random.randint(1, 5)
                display_text = f"Show {current_number} fingers"
                pygame.mixer.unpause()  # Resume the music when a new gesture is made
        else:
            pygame.mixer.pause()  # Pause the music if no hands are detected

        if time.time() - last_gesture_time > 0.8:
            pygame.mixer.pause()

                # Create instructions text
        instructions_line1 = "Show the number of fingers as per the prompt on the screen."
        instructions_line2 = "Do 60 correct gestures to finish."
        display_text = f"Show {current_number} fingers"
        text_img = np.zeros_like(img, np.uint8)
        cv2.putText(text_img, instructions_line1, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(text_img, instructions_line2, (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(text_img, display_text, (50, 125), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)

        img = cv2.addWeighted(img, 0.6, text_img, 0.4, 0)

        # Convert OpenCV image to Pygame surface
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.rot90(img)
        img = pygame.surfarray.make_surface(img)
        img = pygame.transform.flip(img, True, False)

        screen.blit(img, (0, 0))
        pygame.display.flip()

        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)):
                pygame.quit()
                cap.release()
                cv2.destroyAllWindows()
                pygame.mixer.quit()
                sys.exit()

        if gesture_count == 60:
            break

    pygame.quit()
    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.quit()


if __name__ == "__main__":
    main()
