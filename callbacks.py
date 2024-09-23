import RPi.GPIO as gpio
import time

# Define input port numbers:
in1 = 17

gpio.setmode(gpio.BCM)
gpio.setup(in1, gpio.IN, pull_up_down=gpio.PUD_DOWN)

# Define a threaded callback function:
def myCallback(pin):
  print("Rising edge detected on pin %d" % pin)

# Execute myCallback() if port 1 goes HIGH:
gpio.add_event_detect(in1, gpio.RISING, callback=myCallback, bouncetime=100)

# Infinite loop:
while True:
  print('.')
  time.sleep(0.1)

gpio.cleanup()
