# stepper_with_shifter.py
#
# Drive a stepper motor through a shift register
#
# Note that the 5V 28BYJ-48 stepper motors can be driven directly
# from the shift register outputs (35mA @ 5V for SN74HC595)
#
# Use Vcc = 5V for both the shift register & motor.
#
# While this code is designed for driving a single motor,
# it can be extended to work with 2+ motors without
# using any additional GPIO pins.

from shifter import Shifter
import time

s = Shifter(data=16,clock=20,latch=21)   # Set up shifter

cycle = [0b0001,
         0b0011,
         0b0010,
         0b0110,
         0b0100,
         0b1100,
         0b1000,
         0b1001]

# track position within m_seq:
pos = 0

delay = 1200/1e6  # delay between steps [us]
# Make a full rotation of the output shaft:
def loop(dir): # dir = rotation direction (1=cww, -1=cw)
    global pos
    for i in range(4096): # 4096 steps/rev
        pos += dir
        pos %= 8 
        s.shiftByte(cycle[pos]<<4)
        time.sleep(delay)

try:
    loop(1)
    loop(-1)
except Exception as e:
    print(e)


