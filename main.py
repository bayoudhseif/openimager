import tkinter as tk
from tkinter import ttk, messagebox
import os

def open_file(difficulty):
    file_map = {
        "Simple": "levels/01_simple.py",
        "Intermediate": "levels/02_intermediate.py",
        "Advanced": "levels/03_advanced.py"
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

# Try to set a more modern theme if available
try:
    root.tk.call("source", "sun-valley.tcl")
    root.tk.call("set_theme", "light")
except tk.TclError:
    pass  # Fallback to default if the theme is not available

# Set window size and position
root.geometry("400x300+400+200")

# Custom styling
style = ttk.Style()
style.configure("TButton", font=("Montserrat", 12), background="#f0f0f0")
style.configure("TLabel", font=("Montserrat", 16))

# Title and subtitle
title = ttk.Label(root, text="Open Imager", font=("Montserrat", 20, "bold"))
title.pack(pady=(10, 5))

subtitle = ttk.Label(root, text="Orthopedic Gesture Control", font=("Montserrat", 14))

subtitle.pack(pady=(0, 20))

# Button frame
button_frame = ttk.Frame(root)
button_frame.pack(pady=20)

# Buttons
btn_simple = ttk.Button(button_frame, text="Simple", command=lambda: open_file("Simple"))
btn_simple.pack(pady=5, fill='x')

btn_intermediate = ttk.Button(button_frame, text="Intermediate", command=lambda: open_file("Intermediate"))
btn_intermediate.pack(pady=5, fill='x')

btn_advanced = ttk.Button(button_frame, text="Advanced", command=lambda: open_file("Advanced"))
btn_advanced.pack(pady=5, fill='x')

# Credits
credits = ttk.Label(root, text="A project by Bayoudh Seïf & Bouzian Hicham.", font=("Montserrat", 10))
credits.pack(side='bottom', pady=(10, 0))

# Run the application
root.mainloop()
