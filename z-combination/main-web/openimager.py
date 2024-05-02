from flask import Flask, render_template
import subprocess

app = Flask(__name__)
app = Flask(__name__, template_folder='', static_folder='')

@app.route('/')
def index():
    return render_template('openimager.html')

@app.route('/run_balance')
def run_balance():
    subprocess.Popen(["python", "levels/balance/balance.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    return "balance.py is running in a separate window."

@app.route('/run_agility')
def run_agility():
    subprocess.Popen(["python", "levels/agility/agility.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    return "agility.py is running in a separate window."

@app.route('/run_dexterity')
def run_dexterity():
    subprocess.Popen(["python", "levels/dexterity/dexterity.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    return "dexterity.py is running in a separate window."

if __name__ == '__main__':
    app.run(debug=True)