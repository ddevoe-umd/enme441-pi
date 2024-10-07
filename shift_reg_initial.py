import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

dataPin, latchPin, clockPin = 23, 24, 25

GPIO.setup(dataPin, GPIO.OUT)
GPIO.setup(latchPin, GPIO.OUT, initial=0)  # start latch & clock low
GPIO.setup(clockPin, GPIO.OUT, initial=0)  

pattern = 0b01100110        # 8-bit pattern to display on LED bar

for i in range(8):
  GPIO.output(dataPin, pattern & (1<<i))
  GPIO.output(clockPin,1) 	    # ping the clock pin to shift register data
  time.sleep(0)
  GPIO.output(clockPin,0)

GPIO.output(latchPin, 1)        # ping the latch pin to send register to output
time.sleep(0)
GPIO.output(latchPin, 0)

try:
  while 1: pass
except:
  GPIO.cleanup()
