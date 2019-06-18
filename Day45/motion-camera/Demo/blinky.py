
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT) # RED
GPIO.setup(5, GPIO.OUT) # GREEN

while True:
    GPIO.output(3, GPIO.HIGH)
    GPIO.output(5, GPIO.LOW)
    time.sleep(0.1)
    
    GPIO.output(3, GPIO.LOW)
    GPIO.output(5, GPIO.HIGH)
    time.sleep(0.1)
