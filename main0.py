import eel
import os

eel.init('web')  # Assuming your HTML/CSS/JS file is inside a directory named 'web'

@eel.expose  # Make this Python function callable from JavaScript
def open_file(difficulty):
    file_map = {
        "Simple": "levels/01_simple/01_simple.py",
        "Intermediate": "levels/02_intermediate/02_intermediate.py",
        "Advanced": "levels/03_advanced/03_advanced.py",
        "Expert": "levels/04_expert/04_expert.py",
        "Master": "levels/05_master/05_master.py"
    }
    file_name = file_map.get(difficulty)
    if file_name:
        try:
            os.system(f"python {file_name}")
        except Exception as e:
            print(f"Failed to open {file_name}\n{e}")  # Eel does not support messagebox directly

eel.start('index.html', size=(400, 400))  # Start Eel with your main HTML page
