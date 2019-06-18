from picamera import PiCamera
from time import sleep


camera = PiCamera()

camera.resolution = (1600,1200)
camera.start_preview()
sleep(7)
camera.capture('snapshot.png')
camera.stop_preview()



 