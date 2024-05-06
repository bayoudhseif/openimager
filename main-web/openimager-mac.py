from flask import Flask, render_template
import subprocess
import os
import sys

app = Flask(__name__, template_folder='', static_folder='')

@app.route('/')
def index():
    return render_template('openimager.html')

@app.route('/run_balance')
def run_balance():
    python_path = sys.executable
    script_path = os.path.join(os.getcwd(), "levels", "balance", "balance.py")
    process = subprocess.Popen([python_path, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        return f"Failed to run balance.py: {stderr.decode()}"
    return "balance.py is running in a separate window."

@app.route('/run_agility')
def run_agility():
    python_path = sys.executable
    script_path = os.path.join(os.getcwd(), "levels", "agility", "agility.py")
    process = subprocess.Popen([python_path, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        return f"Failed to run agility.py: {stderr.decode()}"
    return "agility.py is running in a separate window."

@app.route('/run_dexterity')
def run_dexterity():
    python_path = sys.executable
    script_path = os.path.join(os.getcwd(), "levels", "dexterity", "dexterity.py")
    process = subprocess.Popen([python_path, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        return f"Failed to run dexterity.py: {stderr.decode()}"
    return "dexterity.py is running in a separate window."

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)