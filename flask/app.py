from flask import Flask, Response, render_template
from video_processor import generate_frames  # Make sure this is correctly named and accessible

app = Flask(__name__)

@app.route('/')
def index():
    # Serve an HTML file with JavaScript that can interact with the Flask API
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(generate_frames(),  # This generator function will yield JPEG frames
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
