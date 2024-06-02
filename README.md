# Open Imager

[![Version](https://img.shields.io/badge/version-4.2.0-blue.svg)]()
[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-312/)

**Open Imager** is a gesture-controlled interface designed to harness the power of advanced hand tracking technologies. Utilizing a combination of **OpenCV**, **CVZone**, and **MediaPipe**, it offers an unparalleled interactive experience.

This application was specifically crafted to aid individuals undergoing orthopedic rehabilitation, facilitating the relearning and training of fine motor skills and hand movements.

<div style="display: flex; flex-direction: column;">
  <img src="https://github.com/bayoudhseif/openimager/blob/master/assets/interface.PNG?raw=true" alt="Interface Preview" style="width: 100%;">
</div>

<div style="display: flex; justify-content: center; margin-top: 20px;">
  <a href="https://www.youtube.com/watch?v=ZJ_tWuLcxhg" target="_blank">
    <img src="https://img.shields.io/badge/Watch%20on-YouTube-red?style=for-the-badge&logo=youtube" alt="Watch on YouTube" style="width: 300px;">
  </a>
</div>

<details>
<summary>Flowchart</summary>

<img src="https://github.com/bayoudhseif/openimager/blob/master/assets/flowchart.png?raw=true" alt="Flowchart" style="width: 100%;">

</details>

These instructions are for Windows. While Mac is supported, documentation for it is not available at the moment.

---

## Setup & Installation

<details>
<summary>Setup & Installation</summary>

### Prerequisites

- **[Python 3.12](https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe)**: Ensure you have Python 3.12 installed.
- **[Microsoft Visual C++](https://aka.ms/vs/17/release/vc_redist.x64.exe)**: Install the Microsoft Visual C++ 2015-2022 Redistributable.

### Installation

1. **Clone or Download Repository**
   - Clone the project repository using Git or download it as a ZIP file.

2. **Install Dependencies**
   - Open your terminal or command prompt.
   - Navigate to the project repository directory.
   - Run the following command to install the required Python packages:
     ```sh
     pip install -r requirements.txt
     ```

### Running the Application

1. **Navigate to Application Directory**
   - Change directory to `main-web`:
     ```sh
     cd main-web
     ```

2. **Run the Application**
   - Execute the following command to start the application:
     ```sh
     python openimager-windows.py
     ```

</details>

<details>
<summary>Hardware Recommendations</summary>

To ensure optimal performance, it is recommended to use the following hardware specifications:

- **Processor**: Quad-core CPU with 2.5 GHz or higher clock speed.
- **RAM**: Minimum 8 GB RAM.
- **GPU**: Optional but recommended for improved performance, with at least 2 GB VRAM.
- **Camera**: Standard webcam capable of at least 720p resolution.

</details>

---

## Troubleshooting

<details>
<summary>Games don't open when clicked in web interface</summary>

If you're having trouble getting the training modules to work after starting the Flask server from `openimager-windows.py`, follow these steps:

1. **Go to the Levels Directory**: Open your command prompt or terminal and navigate to the `levels` folder inside the `main-web` folder of your project.

2. **Find the Module**: Inside the `levels` folder, you'll see folders named `agility`, `balance`, and `dexterity`. Go into the folder that corresponds to the module you're having trouble with. For example, if it's the agility module, go into the `agility` folder.

3. **Run the Module**: Once you're inside the module's folder, find the Python file (it will have the same name as the folder) and run it by typing `python filename.py` in your command prompt or terminal. This will run the module directly and may show any errors that are preventing it from working properly.

Repeat these steps for the other modules if needed.

</details>

<details>
<summary>Module not found</summary>

If the troubleshooting tip above shows **"module name not found"**, follow these steps:

1. **Try Installing with pip**:
    - Run `pip install <module_name>`

2. **If Error Persists**:
    - Run `pip install <module_name> --user`

Replace `<module_name>` with the library name that gives the error, for example, `cvzone`, `flask`, etc.

</details>

---

## Training sequences & code snippets

<details>
<summary>Balance sequence / Snake Game</summary>

### Purpose
- A hand-controlled snake game using OpenCV and Pygame.

### Game Mechanics
- The game continuously captures frames from the camera, detects hand landmarks, and uses the index finger position to control the snake.
- If the snake's head (index finger tip) collides with a treat, the score increases, and a new treat position is generated.
- The game ends if the snake stands still for too long.

1. **Hand Detection and Grabbing Mechanism**
   <details>
   <summary><b>View Code</b></summary>

   ```python
   # Initialize hand detector
   detector = HandDetector(detectionCon=0.8)

   # Main loop
   while True:
       success, img = cap.read()
       if not success:
           print("Failed to capture video frame.")
           continue  # Skip the rest of the loop and try to get another frame

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
   ```

   **Explanation**:
   - The hand detector is initialized with a confidence threshold of 0.8.
   - In the main loop, it captures frames from the camera, flips them horizontally, and detects hands in the frame.
   - It calculates the distance between the index and middle fingertips to determine if the user is grabbing (fingers close together) or releasing (fingers apart) the draggable object.

   </details>

2. **Draggable Rectangle Class with Image**
   <details>
   <summary><b>View Code</b></summary>

   ```python
   # Define class for draggable rectangle (now with images)
   class DragRect:
       def __init__(self, pos_center, image):
           self.pos_center = pos_center
           self.image = image
           self.is_grabbed = False
           self.size = [image.shape[1], image.shape[0]]

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
   ```

   **Explanation**:
   - `DragRect` class manages a draggable rectangle with an image.
   - It updates the rectangle's position based on the cursor's position when the hand is grabbing it.
   - It checks if the cursor is within the rectangle's bounds to determine if the rectangle should follow the cursor.

   </details>

3. **Planting Zone and Seed Planting Logic**
   <details>
   <summary><b>View Code</b></summary>

   ```python
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
       margin = 100  # To ensure the zone does not spawn too close to the edges
       x = random.randint(margin + zone_width // 2, img_width - margin - zone_width // 2)
       y = random.randint(margin + zone_height // 2, img_height - margin - zone_height // 2)
       return [x, y]
   ```

   **Explanation**:
   - `is_inside_planting_zone`: Checks if the rectangle's center is within the planting zone's boundaries.
   - `generate_new_planting_zone`: Generates a new random position for the planting zone, ensuring it doesn't spawn too close to the edges or overlap with the current zone.

   </details>

</details>

<details>
<summary>Agility sequence (Planting Game)</summary>

### Purpose
- A hand-controlled drag-and-drop planting game using OpenCV and Pygame.

### Game Mechanics
- The game detects hand gestures to grab and move a box (seed) to a planting zone.
- If the box is placed inside the planting zone, a new planting zone is generated.

1. **Hand Detection and Initialization**
   <details>
   <summary><b>View Code</b></summary>

   ```python

   # Initialize camera
   cap = cv2.VideoCapture(0)
   cap.set(3, 1920)
   cap.set(4, 1080)

   # Initialize hand detector
   detector = HandDetector(detectionCon=0.8)

   # Initialize pygame
   pygame.init()
   display_info = pygame.display.Info()
   screen = pygame.display.set_mode((display_info.current_w, display_info.current_h), pygame.FULLSCREEN)
   pygame.display.set_caption("Planting Game")

   # Font settings for instructions
   font = cv2.FONT_HERSHEY_SIMPLEX
   font_scale = 0.8
   font_color = (255, 255, 255)
   line_type = 2

   # Instructions to display
   instructions = [
       "Use your index finger to control the snake's direction.",
       "Eat the red dots to grow longer and increase your score.",
   ]
   ```

   **Explanation**:
   - Initializes the camera, hand detector, and Pygame for full-screen display.
   - Sets up the font settings for displaying instructions on the screen.

   </details>

2. **Game State and Collision Detection**
   <details>
   <summary><b>View Code</b></summary>

   ```python
   # Function to initialize game state
   def initialize_game():
       return {
           "treat_pos": [random.randint(100, 1180), random.randint(100, 620)],
           "score": 0,
           "snake_body": [[640, 360]],  # Starting position
           "game_over": False,
       }

   # Function to add a new treat
   def add_treat():
       return [random.randint(100, 1180), random.randint(100, 620)]

   # Function to check collision with treat
   def check_collision_with_treat(head, treat, tolerance=20):
       dx = head[0] - treat[0]
       dy = head[1] - treat[1]
       distance = np.sqrt(dx**2 + dy**2)
       return distance < tolerance

   # Function to check self collision
   def check_self_collision(snake_body):
       head = snake_body[0]
       return head in snake_body[1:]
   ```

   **Explanation**:
   - `initialize_game`: Initializes the game state with a random treat position, score, initial snake position, and game over flag.
   - `add_treat`: Generates a new random position for the treat.
   - `check_collision_with_treat`: Checks if the snake's head has collided with the treat.
   - `check_self_collision`: Checks if the snake has collided with itself.

   </details>

3. **Main Game Loop and Drawing**
   <details>
   <summary><b>View Code</b></summary>

   ```python
   # Main game loop
   game_running = True
   while game_running:
       game_state = initialize_game()

       while not game_state["game_over"]:
           success, img = cap.read()
           if not success:
               continue

           img = cv2.flip(img, 1)
           hands, img = detector.findHands(img, draw=False)

           if hands:
               index_finger_tip = hands[0]["lmList"][8][:2]
               if len(game_state["snake_body"]) < 2 or not check_self_collision([index_finger_tip] + game_state["snake_body"][1:]):
                   game_state["snake_body"].insert(0, list(index_finger_tip))  # Move the snake
                   if check_collision_with_treat(index_finger_tip, game_state["treat_pos"], tolerance=25):
                       game_state["score"] += 1
                       game_state["treat_pos"] = add_treat()  # Add new treat
                   else:
                       game_state["snake_body"].pop()  # Keep the snake's length constant
               else:
                   game_state["game_over"] = True  # End game condition

           # Drawing
           # Draw the treat with white outline
           cv2.circle(img, tuple(game_state["treat_pos"]), 12, (255, 255, 255), cv2.FILLED)  # White outline
           cv2.circle(img, tuple(game_state["treat_pos"]), 10, (220, 204, 138), cv2.FILLED)  # Lighter treat color

           # Draw the snake with white outline
           for segment in game_state["snake_body"]:
               cv2.rectangle(img, (segment[0] - 9, segment[1] - 9), (segment[0] + 9, segment[1] + 9), (255, 255, 255), cv2.FILLED)  # White outline
               cv2.rectangle(img, (segment[0] - 7, segment[1] - 7), (segment[0] + 7, segment[1] + 7), (51, 27, 10), cv2.FILLED)  # Lighter snake color

           if game_state["score"] >= 30:
               game_running = False
               break

       if game_state["game_over"]:
           print(f"Game Over. Final Score: {game_state['score']}")
           cv2.waitKey(1000)  # Wait a bit before potentially restarting

   cap.release()
   cv2.destroyAllWindows()
   pygame.quit()
   ```

   **Explanation**:
   - Main game loop: Handles game initialization, updates game state based on hand detection, checks for collisions, and updates the display.
   - Drawing: Draws the treat and snake with a white outline, blends text with the video frame, and converts the image to Pygame format for display.

   </details>

</details>

<details>
<summary>Dexterity sequence (Piano Game)</summary>

### Purpose
- A hand gesture-controlled piano game using OpenCV, MediaPipe, and Pygame.

### Game Mechanics
- Plays a piano note when the correct gesture is made.
- Tracks the number of correct gestures and stops after 60 successful gestures.

1. **Hand Detection and Finger Counting**
   <details>
   <summary><b>View Code</b></summary>

   ```python

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
   ```

   **Explanation**:
   - Defines a `handDetector` class using MediaPipe for hand detection.
   - Includes methods for finding hands, finding hand landmarks positions, and counting the number of fingers extended.

   </details>

2. **Playing Piano Notes**
   <details>
   <summary><b>View Code</b></summary>

   ```python
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
   ```

   **Explanation**:
   - Defines a function `play_piano_sequence` that plays a sequence of piano notes when a gesture is detected.

   </details>

3. **Main Game Loop**
   <details>
   <summary><b>View Code</b></summary>

   ```python
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
   ```

   **Explanation**:
   - Counts the number of fingers shown and updates the game state accordingly.
   - Plays piano notes based on detected gestures.
   - Ends the game after 60 correct gestures.

   </details>

</details>
