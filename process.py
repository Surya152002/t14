import cv2
import numpy as np
import darknet

from flask import Flask, render_template, Response

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def detect_plate(frame):
    # Load the YOLOv3 model and configuration files
    net = darknet.load_net_custom("yolov3-custom.cfg", "yolov3-custom.weights", 0, 1)
    meta = darknet.load_meta("obj.data")
    
    # Convert the frame to a darknet image
    darknet_image = darknet.make_image(frame.shape[1], frame.shape[0], 3)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    darknet.copy_image_from_bytes(darknet_image, frame_rgb.tobytes())
    
    # Use YOLOv3 to detect license plates
    detections = darknet.detect_image(net, meta, darknet_image)
    for detection in detections:
        if detection[0].decode() == 'license_plate':
            x, y, w, h = detection[2]
            x1 = int(x - w / 2)
            y1 = int(y - h / 2)
            x2 = int(x + w / 2)
            y2 = int(y + h / 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
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
