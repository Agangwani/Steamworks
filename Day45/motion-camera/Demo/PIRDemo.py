from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import time
from psonic import *

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)   #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)   #RED LED output pin
GPIO.setup(5, GPIO.OUT)   #GREEN LED output pin

camera = PiCamera()


while True:
    i=GPIO.input(11)
    if i==0:              #When output from motion sensor is LOW
        print ("No intruders", i)
        GPIO.output(3, 0) #Turn OFF RED LED
        GPIO.output(5, 1) #Turn ON GREEN LED
        time.sleep(0.1)
    elif i==1:            #When output from motion sensor is HIGH
        print ("Intruder detected", i)
        GPIO.output(3, 1) #Turn ON RED LED
        GPIO.output(5, 0) #Turn OFF GREEN LED
        

        play(70)
        sleep (0.25)
        play(chord(E4,MINOR))
        sleep (0.25)
        time.sleep(0.1)
        camera.start_preview()
        sleep(5)
        camera.stop_preview()
        

