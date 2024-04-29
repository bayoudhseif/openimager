import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess

import subprocess

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

def toggle_fullscreen():
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

# Create the main window
root = tk.Tk()
root.title("Orthopedic Gesture Control")
root.configure(bg='#f0f0f0')

# Full screen
root.attributes("-fullscreen", True)

# Style configuration for ttk
style = ttk.Style()
style.theme_use('clam')

# Configure ttk button style
style.configure('TButton', font=('Montserrat', 24), borderwidth='0')
style.map('TButton',
          background=[('active', '#c4c4c4')],
          foreground=[('active', '#333')])

# Title and subtitle
title = tk.Label(root, text="Open Imager", font=("Montserrat", 48, "bold"), bg='#f0f0f0', fg='#0066cc')
title.pack(pady=(80, 40))

subtitle = tk.Label(root, text="Orthopedic Gesture Control", font=("Montserrat", 30), bg='#f0f0f0', fg='#333')
subtitle.pack(pady=(0, 40))

# Button frame
button_frame = tk.Frame(root, bg='#f0f0f0')
button_frame.pack(pady=40)

# Buttons for each level
levels = ["Simple", "Intermediate", "Advanced"]
for level in levels:
    ttk.Button(button_frame, text=level, command=lambda lvl=level: open_file(lvl), width=20, padding=20).pack(pady=20)

# Buttons to control window
control_frame = tk.Frame(root, bg='#f0f0f0')
control_frame.pack(side='bottom', pady=60)

minimize_button = ttk.Button(control_frame, text="Minimize", command=minimize_window, width=15)
minimize_button.grid(row=0, column=0, padx=20)

fullscreen_button = ttk.Button(control_frame, text="Toggle Fullscreen", command=toggle_fullscreen, width=15)
fullscreen_button.grid(row=0, column=1, padx=20)

close_button = ttk.Button(control_frame, text="Close", command=close_window, width=15)
close_button.grid(row=0, column=2, padx=20)

# Run the application
root.mainloop()
