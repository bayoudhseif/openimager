import webview
import subprocess

def run_scripty():
    # Launch scripty.py as a separate process
    subprocess.Popen(["python", "scripty.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    return "scripty.py is running in a separate window."

def create_window():
    window = webview.create_window('Open Imager', fullscreen=True, html='''
        <html>
            <body>
                <button onclick="pywebview.api.run_scripty()">Run Scripty.py</button>
            </body>
        </html>
    ''')
    window.expose(run_scripty)
    webview.start()

if __name__ == '__main__':
    create_window()
