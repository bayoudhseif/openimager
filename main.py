import tkinter as tk
from tkinter import ttk, messagebox
import os

def open_file(difficulty):
    file_map = {
        "Simple": "levels/01_simple/01_simple.py",
        "Intermediate": "levels/02_intermediate/02_intermediate.py",
        "Advanced": "levels/03_advanced/03_advanced.py"
    }
    file_name = file_map.get(difficulty)
    if file_name:
        try:
            os.system(f"python {file_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open {file_name}\n{e}")

# Create the main window
root = tk.Tk()
root.title("Open Imager")

# Set window size and position
root.geometry("400x300+400+200")

# Title and subtitle
title = tk.Label(root, text="Open Imager", font=("Arial", 20, "bold"))
title.pack(pady=(10, 5))

subtitle = tk.Label(root, text="Orthopedic Gesture Control", font=("Arial", 14))
subtitle.pack(pady=(0, 20))

# Button frame
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

# Buttons
btn_simple = tk.Button(button_frame, text="Simple", command=lambda: open_file("Simple"))
btn_simple.pack(pady=5, fill='x')

btn_intermediate = tk.Button(button_frame, text="Intermediate", command=lambda: open_file("Intermediate"))
btn_intermediate.pack(pady=5, fill='x')

btn_advanced = tk.Button(button_frame, text="Advanced", command=lambda: open_file("Advanced"))
btn_advanced.pack(pady=5, fill='x')

# Credits
credits = tk.Label(root, text="A project by Bayoudh Seïf & Bouzian Hicham.", font=("Arial", 10))
credits.pack(side='bottom', pady=(10, 0))

credits2 = tk.Label(root, text="openimager.com", font=("Arial", 10))
credits2.pack(side='bottom', pady=(0, 0))

# Run the application
root.mainloop()
