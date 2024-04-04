import eel
import os

# Initialize the Eel application with the 'web' directory containing your HTML, CSS, and JS files
eel.init('web')

@eel.expose  # Expose this function to JavaScript so it can be called from the frontend
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
            print(f"Failed to open {file_name}\n{e}")

# Start the Eel application with configurations directly passed as keyword arguments
eel.start('index.html', mode='chrome-app', cmdline_args=['--start-maximized'])
