from flask import Flask, render_template
import os

app = Flask(__name__)
app = Flask(__name__, template_folder='', static_folder='')

@app.route('/')
def index():
    return render_template('openimager.html')

@app.route('/run_balance')
def run_balance():
    os.system("open -a Terminal.app python levels/balance/balance.py")
    return "balance.py is running in a separate window."

@app.route('/run_agility')
def run_agility():
    os.system("open -a Terminal.app python levels/agility/agility.py")
    return "agility.py is running in a separate window."

@app.route('/run_dexterity')
def run_dexterity():
    os.system("open -a Terminal.app python levels/dexterity/dexterity.py")
    return "dexterity.py is running in a separate window."

if __name__ == '__main__':
    app.run(debug=True)