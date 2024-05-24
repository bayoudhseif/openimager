# Open Imager

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-312/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-4.2.0-blue.svg)]()

**Open Imager** is a gesture-controlled interface designed to harness the power of advanced hand tracking technologies. Utilizing a combination of **OpenCV**, **CVZone**, and **MediaPipe**, it offers an unparalleled interactive experience.

This application was specifically crafted to aid individuals undergoing orthopedic rehabilitation, facilitating the relearning and training of fine motor skills and hand movements.

![Interface Preview](https://github.com/bayoudhseif/openimager/blob/master/assets/interface.PNG?raw=true)

These instructions are for Windows. While Mac is supported, documentation for it is not available at the moment.

---

## Setup & Installation

<details>
<summary>Hardware Recommendations</summary>

To ensure optimal performance, it is recommended to use the following hardware specifications:

- **Processor**: Quad-core CPU with 2.5 GHz or higher clock speed.
- **RAM**: Minimum 8 GB RAM.
- **GPU**: Optional but recommended for improved performance, with at least 2 GB VRAM.
- **Camera**: Standard webcam capable of at least 720p resolution.

</details>

<details>
<summary>Expand for Setup & Installation Instructions</summary>

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

---

## Troubleshooting

<details>
<summary>Expand for Troubleshooting Tips</summary>

If you're having trouble getting the training modules to work after starting the Flask server from `openimager-windows.py`, follow these steps:

1. **Go to the Levels Directory**: Open your command prompt or terminal and navigate to the `levels` folder inside the `main-web` folder of your project.

2. **Find the Module**: Inside the `levels` folder, you'll see folders named `agility`, `balance`, and `dexterity`. Go into the folder that corresponds to the module you're having trouble with. For example, if it's the agility module, go into the `agility` folder.

3. **Run the Module**: Once you're inside the module's folder, find the Python file (it will have the same name as the folder) and run it by typing `python filename.py` in your command prompt or terminal. This will run the module directly and may show any errors that are preventing it from working properly.

Repeat these steps for the other modules if needed.

</details>

---

## Training Modules

<details>
<summary>Balance Module (Snake Game)</summary>

### Purpose
A hand-controlled snake game using OpenCV and Pygame.

#### Game Mechanics
- The game continuously captures frames from the camera, detects hand landmarks, and uses the index finger position to control the snake.
- If the snake's head (index finger tip) collides with a treat, the score increases, and a new treat position is generated.
- The game ends if the snake collides with itself.

</details>

<details>
<summary>Agility Module (Planting Game)</summary>

### Purpose
A hand-controlled drag-and-drop planting game using OpenCV and Pygame.

#### Game Mechanics
- The game detects hand gestures to grab and move a box (seed) to a planting zone.
- If the box is placed inside the planting zone, a new planting zone is generated, and the count of planted seeds increases.

</details>

<details>
<summary>Dexterity Module (Piano Game)</summary>

### Purpose
A hand gesture-controlled piano game using OpenCV, MediaPipe, and Pygame.

#### Game Mechanics
- Plays a piano note when the correct gesture is made.
- Tracks the number of correct gestures and stops after 60 successful gestures.

</details>
