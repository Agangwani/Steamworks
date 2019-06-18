#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response
import cv2

import face_detect
from face_detect import detectFace
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
#from camera_pi import Camera



app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + detectFace() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/servoButton')
def servoButton(angle):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
# servo motor HXT900 brown wire to pin 6, red to pin 2 and orange to pin 3
    GPIO.setup(3,GPIO.OUT)


    pwm = GPIO.PWM(3, 50)

    pwm.start(0)

    duty = angle/ 18+2
    GPIO.output(3,True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(3,False)
    pwm.ChangeDutyCycle(0)
    pwm.stop()
    GPIO.cleanup()

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
