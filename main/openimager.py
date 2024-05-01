import webview
import subprocess

def run_balance():
    subprocess.Popen(["python", "levels/balance.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    return "balance.py is running in a separate window."

def run_agility():
    subprocess.Popen(["python", "levels/agility.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    return "agility.py is running in a separate window."

def run_dexterity():
    subprocess.Popen(["python", "levels/dexterity.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    return "dexterity.py is running in a separate window."

def create_window():
    window = webview.create_window('Open Imager', fullscreen=True, html='''
        <html>
            <body>
                <button onclick="pywebview.api.run_balance()">Run balance</button>
                <button onclick="pywebview.api.run_agility()">Run agility</button>
                <button onclick="pywebview.api.run_dexterity()">Run dexterity</button>
            </body>
        </html>
    ''')
    window.expose(run_balance, run_agility, run_dexterity)
    webview.start()

if __name__ == '__main__':
    create_window()
