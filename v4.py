import webview

def create_app():
    # Create a webview window with full width and height
    window = webview.create_window('My', 'v4.html', fullscreen=True)

    # Run the app
    webview.start()

if __name__ == '__main__':
    create_app()