# Stepper motor control
# RPi Zero
#
# Connect the stepper motor power to 5V rail pin on Pi

from RPi import GPIO
import time

GPIO.setmode(GPIO.BCM)

pins = [12,16,20,21] # controller inputs: in1, in2, in3, in4
for p in pins:
  GPIO.setup(p, GPIO.OUT)

delay = 1200/1e6  # delay between steps

# Define the pin sequence for CW motion:
seq = [
    0b0001,
    0b0011,
    0b0010,
    0b0110,
    0b0100,
    0b1100,
    0b1000,
    0b1001
    ]

# Make a full rotation of the output shaft:
def loop(dir):    # dir = 1 (cw) or -1 (ccw)
    pos = 0       # Track position in cw sequence
    for i in range(512):            # 512 cycles/revolution
        for halfstep in range(8):   # 8 half-steps per cycle
            for j in range(4):      # Apply sequence to all pins
                GPIO.output(pins[j],seq[pos] & 1<<j)
            pos += dir         # move to next position in sequence
            pos %= 8           # stay in [0,7] range
            time.sleep(delay)  # need small delay between steps
try:
  loop(1)
  loop(-1)
except Exception as e:
  print(e)