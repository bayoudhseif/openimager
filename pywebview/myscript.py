import webview
import threading
import subprocess

def run_scripty():
    # Launch scripty.py as a separate process
    subprocess.Popen(["python", "scripty.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    return "scripty.py is running in a separate window."

def create_window():
    window = webview.create_window('My App', html='''
        <html>
            <body>
                <div id="result"></div>
        </html>
    ''')
    window.expose(run_scripty)
    webview.start()

if __name__ == '__main__':
    create_window()
