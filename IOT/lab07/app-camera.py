from flask import Flask, render_template, Response
from camera_pi import Camera
import RPi.GPIO as GPIO

app = Flask(__name__)

r = 0


def clicked(btn):
    global r
    r += 1
    if r >= 8:
        r %= 8

GPIO.setmode(GPIO.BOARD)
BTN_PIN = 11
GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BTN_PIN, GPIO.FALLING, clicked, 200)

@app.route('/')
def index():
    return render_template('stream.html')

def gen(camera):
    global r
    while True:
        frame = camera.get_frame(r)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
