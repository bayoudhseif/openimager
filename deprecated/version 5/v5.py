import webview

def create_app():
    # Create a webview window with full width and height
    window = webview.create_window('Open Imager', 'v5.html', fullscreen=True)

    # Run the app
    webview.start()

if __name__ == '__main__':
    create_app()