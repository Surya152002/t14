import cv2
import numpy as np
from flask import Flask, render_template, Response

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def detect_plate(frame):
    # Perform image processing and detect the number plate here
    # Return the processed image with the number plate highlighted
    
    # Example code to draw a rectangle around a detected number plate
    x, y, w, h = 100, 100, 200, 50
    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    return frame

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = detect_plate(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
