import os
import espeak
path = '/home/pi/Documents/IoTCurriculum/IOTDay2/OCRenv/python-docs-samples/vision/cloud-client/detect/speechfile.txt'
file = open(path)


for word in f.read().split():
	print(word)
	espeak.say(word)
