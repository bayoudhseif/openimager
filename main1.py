import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from cvzone.HandTrackingModule import HandDetector
import subprocess
import threading

# Initialize the webcam and cvzone hand detector
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height
detector = HandDetector(detectionCon=0.8)

# Grabbing thresholds
grab_threshold = 30
release_threshold = 40
is_grabbing = False

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

def gesture_control():
    global is_grabbing
    try:
        while True:
            success, img = cap.read()
            if not success:
                continue

            hands, img = detector.findHands(img, draw=False)  # Hands are detected from the flipped image

            if hands:
                hand = hands[0]
                lmList = hand["lmList"]  # List of 21 Landmark points

                # Adjust cursor position according to the flipped image
                cursor_x = int((1280 - lmList[8][0]) * root.winfo_width() / 1280)  # 1280 should be replaced with the actual width if different
                cursor_y = int(lmList[8][1] * root.winfo_height() / 720)

                cursor_label.place(x=cursor_x, y=cursor_y)
                cursor_label.lift()

                # Use thumb tip and index finger tip for distance measurement
                length, _, _ = detector.findDistance(lmList[4][:2], lmList[8][:2], img)  # Distance between thumb tip and index fingertip

                if not is_grabbing and length < grab_threshold:
                    is_grabbing = True
                    print("Click Start Detected")  # Debugging print for click start
                    trigger_click(cursor_x, cursor_y)
                elif is_grabbing and length > release_threshold:
                    is_grabbing = False
                    print("Click End Detected")  # Debugging print for click end

    finally:
        cap.release()
        cv2.destroyAllWindows()



def trigger_click(x, y):
    widget = root.winfo_containing(x, y)
    if widget and hasattr(widget, 'invoke'):
        print(f"Triggering click on widget at ({x}, {y})")
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
