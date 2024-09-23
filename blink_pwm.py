import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

p = 25    # GPIO pin number
f = 1     # frequency (Hz)
dc = 50   # duty cycle (%)

GPIO.setup(p, GPIO.OUT)
pwm = GPIO.PWM(p, f)        # create PWM object

try:
  pwm.start(dc)             # initiate PWM object
  while True:
    pass
except KeyboardInterrupt:   # stop gracefully on ctrl-C
  print('\nExiting')

pwm.stop()
GPIO.cleanup()
