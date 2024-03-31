import tkinter as tk
from tkinter import ttk, messagebox
import os
import eel


def open_file(difficulty):
    file_map = {
        "Simple": "levels/01_simple/01_simple.py",
        "Intermediate": "levels/02_intermediate/02_intermediate.py",
        "Advanced": "levels/03_advanced/03_advanced.py",
        "Expert": "levels/04_expert/04_expert.py",  # New level added
        "Master": "levels/05_master/05_master.py"   # New level added
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

# Adjust window size to accommodate more buttons
root.geometry("400x400+400+200")  # Increased height
root.configure(bg='#121212')
root.attributes("-alpha", 0.95)  # Slightly transparent window

# Style configuration for ttk
style = ttk.Style()
style.theme_use('clam')

# Configure ttk button style
style.configure('TButton', font=('Arial', 12), borderwidth='1')
style.map('TButton',
          background=[('active', '#2b2b2b')],
          foreground=[('active', 'white')])

# Title and subtitle
title = tk.Label(root, text="Open Imager", font=("Arial", 20, "bold"), bg='#121212', fg='light blue')
title.pack(pady=(10, 5))

subtitle = tk.Label(root, text="Orthopedic Gesture Control", font=("Arial", 14), bg='#121212', fg='light gray')
subtitle.pack(pady=(0, 20))

# Button frame
button_frame = tk.Frame(root, bg='#121212')
button_frame.pack(pady=10)

# Buttons for each level
levels = ["Simple", "Intermediate", "Advanced", "Expert", "Master"]
for level in levels:
    ttk.Button(button_frame, text=level, command=lambda lvl=level: open_file(lvl)).pack(pady=5, fill='x')

# Credits
credits = tk.Label(root, text="A project by Bayoudh Seïf & Bouzian Hicham.", font=("Arial", 10), bg='#121212', fg='light gray')
credits.pack(side='bottom', pady=(10, 0))

credits2 = tk.Label(root, text="openimager.com", font=("Arial", 10), bg='#121212', fg='light gray')
credits2.pack(side='bottom', pady=(0, 0))

# Run the application
root.mainloop()
