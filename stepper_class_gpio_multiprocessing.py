# Stepper class
#
# Supports simultaneous operation of an arbitrary number 
# of stepper motors using with direct GPIO control.
#
# THIS VERSION DOES NOT HAVE goAngle() CODED, AND
# DOES NOT PROPERLY ALLOW THE SELF.ANGLE ATTRIBUTE TO BE MODIFIED
# WITHIN THE SUB-PROCESSES

import time
import multiprocessing
from RPi import GPIO

GPIO.setmode(GPIO.BCM)


class Stepper:

  # Class attributes:
  seq = [0b0001,0b0011,0b0010,0b0110,0b0100,0b1100,0b1000,0b1001] # CCW sequence
  stepsPerDegree = 4096/360    # 4096 steps/rev * 1/360 rev/deg

  def __init__(self, pins, lock, delay=1200):
    self.delay = delay         # delay between motor steps [us]
    self.pins = pins           # motor drive pins (4-element list)
    self.angle = 0             # current output shaft angle
    self.seq_state = 0         # track position in sequence
    self.lock = lock           # multiprocessing lock

    for p in self.pins:
      GPIO.setup(p,GPIO.OUT)

  # Signum function:
  def __sgn(self, x):
    if x == 0: return(0)
    else: return(int(abs(x)/x))

  # Move a single +/-1 step in the motor sequence:
  def __step(self, dir):
    seq = Stepper.seq[self.seq_state]
    self.seq_state += dir          # increment/decrement the step
    self.seq_state %= 8            # ensure result stays in [0,7]
    for idx in range(4):
      GPIO.output(self.pins[idx], seq & 1<<idx)

    # THE FOLLOWING LINES WILL NOT ACTUALLY CHANGE THE ANGLE ATTRIBUTE! 
    # NOT A PROBLEM FOR RELATIVE MOVEMENT SINCE WE DON'T NEED TO KNOW
    # THE ABSOLUTE ANGLE, BUT THIS WILL BE A PROBLEM WHEN TRYING TO
    # IMPLEMENT THE goAngle() METHOD!!!  
    #
    # HINT: THINK ABOUT USING A multiprocessing.value() AS AN
    # INSTANCE ATTRIBUTE TO HOLD THE CURRENT ANGLE INSTEAD OF 
    # A REGULAR FLOAT...
    #
    self.angle += dir/Stepper.stepsPerDegree
    self.angle %= 360              # limit to [0,359.9+] range

  # Move relative angle from current position:
  def __rotate(self, delta, lock):
    lock.acquire()                 # wait until the lock is available
    numSteps = int(Stepper.stepsPerDegree * abs(delta))    # find the right # of steps
    dir = self.__sgn(delta)        # find the direction (+/-1)
    for s in range(numSteps):      # take the steps
      self.__step(dir)
      time.sleep(self.delay/1e6)
    lock.release()

  # Move relative angle from current position:
  def rotate(self, delta):
    time.sleep(0.1)
    p = multiprocessing.Process(target=self.__rotate, args=(delta,self.lock))
    p.start()

  # Move to an absolute angle taking the shortest possible path:
  def goAngle(self, angle):
     pass
     # This is a problem for Lab 7!

  # Set the motor zero point
  def zero(self):
    self.angle = 0


# Example use:

if __name__ == '__main__':

  # Use multiprocessing.Lock() to prevent a single motor from trying to 
  # execute multiple operations at the same time:
  lock1 = multiprocessing.Lock()
  lock2 = multiprocessing.Lock()

  # Instantiate 2 Steppers:
  m1 = Stepper([6,13,19,26], lock1)
  m2 = Stepper([12,16,20,21], lock2)

  # Zero the motors:
  m1.zero()
  m2.zero()

  # Move as desired. Each step will occur as soon as the previous steps ends.
  m1.rotate(-90)
  m1.rotate(45)
  m1.rotate(-180)
  m1.rotate(145)

  m2.rotate(-90)
  m2.rotate(45)
  m2.rotate(-90)
  m2.rotate(145)

