import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import mediapipe as mp
import subprocess
import threading
import math

# Initialize MediaPipe hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize the webcam
cap = cv2.VideoCapture(0)

def open_file(difficulty):
    file_map = {
        "Simple": "levels/01_simple/01_simple.py",
        "Intermediate": "levels/02_intermediate/02_intermediate.py",
        "Advanced": "levels/03_advanced/03_advanced.py"
    }
    file_name = file_map.get(difficulty)
    if file_name:
        try:
            root.destroy()  # Close the main menu window
            subprocess.Popen(["python", file_name], creationflags=subprocess.CREATE_NEW_CONSOLE)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open {file_name}\n{e}")

def minimize_window():
    root.iconify()

def close_window():
    root.destroy()
    cap.release()
    cv2.destroyAllWindows()

def toggle_fullscreen():
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

def get_distance(landmark1, landmark2):
    return math.sqrt((landmark1.x - landmark2.x) ** 2 + (landmark1.y - landmark2.y) ** 2)

def gesture_control():
    try:
        while True:
            success, image = cap.read()
            if not success:
                continue

            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                    x = int(wrist.x * root.winfo_width())
                    y = int(wrist.y * root.winfo_height())

                    cursor_label.place(x=x, y=y)
                    cursor_label.lift()  # Ensure the label is always on top

                    if get_distance(thumb_tip, index_tip) < 0.04:  # Adjust this threshold based on your setup
                        print("Click Detected")  # Output to console when a click is detected
                        trigger_click(x, y)
                    
                    break  # Only consider the first hand
    finally:
        cap.release()
        cv2.destroyAllWindows()

def trigger_click(x, y):
    widget = root.winfo_containing(x, y)
    if widget and hasattr(widget, 'invoke'):
        widget.invoke()

root = tk.Tk()
root.title("Gesture Control Interface")
root.configure(bg='#f0f0f0')
root.attributes("-fullscreen", True)

style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', font=('Montserrat', 24), borderwidth='0')
style.map('TButton', background=[('active', '#c4c4c4')], foreground=[('active', '#333')])

title = tk.Label(root, text="Open Imager", font=("Montserrat", 48, "bold"), bg='#f0f0f0', fg='#0066cc')
title.pack(pady=(80, 40))
subtitle = tk.Label(root, text="Gesture Control Interface", font=("Montserrat", 30), bg='#f0f0f0', fg='#333')
subtitle.pack(pady=(0, 40))

cursor_label = tk.Label(root, text="⬤", font=("Arial", 34), bg='#f0f0f0', fg='#0066cc')

button_frame = tk.Frame(root, bg='#f0f0f0')
button_frame.pack(pady=40)
levels = ["Simple", "Intermediate", "Advanced"]
for level in levels:
    ttk.Button(button_frame, text=level, command=lambda lvl=level: open_file(lvl), width=20, padding=20).pack(pady=20)

control_frame = tk.Frame(root, bg='#f0f0f0')
control_frame.pack(side='bottom', pady=60)
ttk.Button(control_frame, text="Minimize", command=minimize_window, width=15).grid(row=0, column=0, padx=20)
ttk.Button(control_frame, text="Toggle Fullscreen", command=toggle_fullscreen, width=15).grid(row=0, column=1, padx=20)
ttk.Button(control_frame, text="Close", command=close_window, width=15).grid(row=0, column=2, padx=20)

threading.Thread(target=gesture_control, daemon=True).start()

root.mainloop()
