import tkinter as tk
from tkinter import messagebox
import os

def open_file(file_name):
    try:
        os.system(f"python {file_name}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open {file_name}\n{e}")

# Create the main window
root = tk.Tk()
root.title("Open Imager")

# Set window size (optional)
root.geometry("300x150")

# Create buttons
btn_file1 = tk.Button(root, text="Open File 1", command=lambda: open_file("file1.py"))
btn_file1.pack(pady=5)

btn_file2 = tk.Button(root, text="Open File 2", command=lambda: open_file("file2.py"))
btn_file2.pack(pady=5)

btn_file3 = tk.Button(root, text="Open File 3", command=lambda: open_file("file3.py"))
btn_file3.pack(pady=5)

# Run the application
root.mainloop()
