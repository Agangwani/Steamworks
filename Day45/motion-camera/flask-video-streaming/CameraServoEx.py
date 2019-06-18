import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
# servo motor HXT900 brown wire to pin 6, red to pin 2 and orange to pin 3
GPIO.setup(3,GPIO.OUT)


pwm = GPIO.PWM(3, 50)

pwm.start(0)
def setAngle(angle):
	duty = angle/ 18+2
	GPIO.output(3,True)
	pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(3,False)
	pwm.ChangeDutyCycle(0)


setAngle(90)
pwm.stop()
GPIO.cleanup()
