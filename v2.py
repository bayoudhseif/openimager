import webview

def create_app():
    # Create a webview window
    window = webview.create_window('My', 'v2.html', width=800, height=600)

    # Run the app
    webview.start()

if __name__ == '__main__':
    create_app()
