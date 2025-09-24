import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
p = 4
GPIO.setup(p, GPIO.OUT)

try:
  while True:
    GPIO.output(p, 0)
    sleep(0.5)
    GPIO.output(p, 1)
    sleep(0.5)
except KeyboardInterrupt: # if user hits ctrl-C
  print('\nExiting')
except Exception as e:    # catch all other errors
  print('\ne')
  
GPIO.cleanup()            # clean up GPIO ports
