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
style.configure('TButton', font=('Arial', 12), borderwidth='1')
style.map('TButton',
          background=[('active', '#2b2b2b')],
          foreground=[('active', 'white')])

# Title and subtitle
title = tk.Label(root, text="Open Imager", font=("Arial", 24, "bold"), bg='#f0f0f0', fg='#0066cc')
title.pack(pady=(20, 10))

subtitle = tk.Label(root, text="Orthopedic Gesture Control", font=("Arial", 16), bg='#f0f0f0', fg='#333')
subtitle.pack(pady=(0, 20))

# Button frame
button_frame = tk.Frame(root, bg='#f0f0f0')
button_frame.pack(pady=10)

# Buttons for each level
levels = ["Simple", "Intermediate", "Advanced"]
for level in levels:
    ttk.Button(button_frame, text=level, command=lambda lvl=level: open_file(lvl)).pack(pady=5, fill='x')

# Buttons to control window
control_frame = tk.Frame(root, bg='#f0f0f0')
control_frame.pack(side='bottom', pady=20)

minimize_button = ttk.Button(control_frame, text="Minimize", command=minimize_window)
minimize_button.grid(row=0, column=0, padx=10)

fullscreen_button = ttk.Button(control_frame, text="Toggle Fullscreen", command=toggle_fullscreen)
fullscreen_button.grid(row=0, column=1, padx=10)

close_button = ttk.Button(control_frame, text="Close", command=close_window)
close_button.grid(row=0, column=2, padx=10)

# Run the application
root.mainloop()
