import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
p = 4
GPIO.setup(p, GPIO.OUT)
pwm = GPIO.PWM(p, 100)          # create PWM object @ 100 Hz
try:
  pwm.start(0)                  # initiate PWM at 0% duty cycle
  while 1:
    for dc in range(101):       # loop duty cycle from 0 to 100  
      pwm.ChangeDutyCycle(dc)   # set duty cycle  
      sleep(0.01)               # sleep 10 ms
except KeyboardInterrupt:       # stop gracefully on ctrl-C
  print('\nExiting')
pwm.stop()
GPIO.cleanup()
