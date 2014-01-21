import RPi.GPIO as GPIO
import time

GPIO.setmode( GPIO.BCM )

pins = [4, 17, 21, 22, 23, 24, 25, 18]

for i in pins:
	GPIO.setup( i , GPIO.IN )

while True:
	for i in pins:
		if GPIO.input(i):
			print i
			time.sleep( 0.4 )
