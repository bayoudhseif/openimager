from flask import Flask, render_template
import subprocess
import os

app = Flask(__name__, template_folder='', static_folder='')

@app.route('/')
def index():
    return render_template('openimager.html')

@app.route('/run_balance')
def run_balance():
    python_path = "/Users/hichambzn/Desktop/prefinal/venv/bin/python"
    script_path = "/Users/hichambzn/Desktop/prefinal/openimager/main-web/levels/balance/balance.py"
    result = subprocess.run([python_path, script_path], capture_output=True, text=True)
    if result.returncode != 0:
        error_message = result.stderr or "balance.py is running in a separate window."
        return f"Failed to run balance.py: {error_message}"
    return "balance.py executed successfully."

@app.route('/run_agility')
def run_agility():
    python_path = "/Users/hichambzn/Desktop/prefinal/venv/bin/python"
    script_path = "/Users/hichambzn/Desktop/prefinal/openimager/main-web/levels/agility/agility.py"
    result = subprocess.run([python_path, script_path], capture_output=True, text=True)
    if result.returncode != 0:
        return f"Failed to run agility.py: {result.stderr}"
    return "agility.py is running in a separate window."

@app.route('/run_dexterity')
def run_dexterity():
    python_path = "/Users/hichambzn/Desktop/prefinal/venv/bin/python"
    script_path = "/Users/hichambzn/Desktop/prefinal/openimager/main-web/levels/dexterity/dexterity.py"
    result = subprocess.run([python_path, script_path], capture_output=True, text=True)
    if result.returncode != 0:
        return f"Failed to run dexterity.py: {result.stderr}"
    return "dexterity.py is running in a separate window."

if __name__ == '__main__':
    app.run(debug=True)