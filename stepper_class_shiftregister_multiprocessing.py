# DO NOT USE
# DOES NOT SUPPORT MULTIPLE SIMULTANEOUS MOTORS
#
# SEE THE GPIO VERSION...NEED TO PORT OVER FROM THERE
# USING MULTIPROCESSING.LOCK()



# Stepper class
#
# Supports operation of an arbitrary number of stepper motors using
# one or more shift registers.
#
# A class attribute (shifter_outputs) keeps track of all
# shift register output values for all motors.  In addition to
# simplifying sequential control of multiple motors, this schema also
# makes simultaneous operation of multiple motors possible.
#
# Motor instantiation sequence is inverted from the shift register outputs.
# For example, in the case of 2 motors, the 2nd motor must be connected
# with the first set of shift register outputs (Qa-Qd), and the 1st motor
# with the second set of outputs (Qe-Qh). This is because the MSB of
# the register is associated with Qa, and the LSB with Qh (look at the code
# to see why this makes sense).
#
# An instance attribute (shifter_bit_start) tracks the bit position
# in the shift register where the 4 control bits for each motor
# begin.
#
# The SharedMemoryManager is used to share a flag between all processes
# indicating when a motor is currently operating to prevent multiple
# motor movements from executing simultaneously.
#
# Multiprocessing is used instead of threading since the GIL makes
# the motor process run too slowly on the Pi Zero!


import time
import multiprocessing
from multiprocessing.managers import SharedMemoryManager


class Stepper:

  # Class attributes:
  num_steppers = 0      # track number of Steppers instantiated
  shifter_outputs = 0   # track shift register outputs for all motors
  seq = [0b0001,0b0011,0b0010,0b0110,0b0100,0b1100,0b1000,0b1001] # CCW sequence
  delay = 1200          # delay between motor steps [us]
  stepsPerDegree = 4096/360    # 4096 steps/rev * 1/360 rev/deg

  def __init__(self, shifter, sl):
    self.s = shifter           # shift register
    self.angle = 0             # current output shaft angle
    self.step_state = 0        # track position in sequence
    self.shifter_bit_start = 4*Stepper.num_steppers  # starting bit position
    self.is_active = sl        # sharable list containing is_active flag

    Stepper.num_steppers += 1   # increment the instance count

  # Signum function:
  def __sgn(self, x):
    if x == 0: return(0)
    else: return(int(abs(x)/x))

  # Move a single +/-1 step in the motor sequence:
  def __step(self, dir):
    self.step_state += dir    # increment/decrement the step
    self.step_state %= 8      # ensure result stays in [0,7]
    Stepper.shifter_outputs |= 0b1111<<self.shifter_bit_start
    Stepper.shifter_outputs &= Stepper.seq[self.step_state]<<self.shifter_bit_start
    self.s.shiftByte(Stepper.shifter_outputs)
    self.angle += dir/Stepper.stepsPerDegree
    self.angle %= 360         # limit to [0,359.9+] range

  # Move relative angle from current position:
  def __rotate(self, delta, is_active):
    numSteps = int(Stepper.stepsPerDegree * abs(delta))    # find the right # of steps
    dir = self.__sgn(delta)        # find the direction (+/-1)
    for s in range(numSteps):      # take the steps
      self.__step(dir)
      time.sleep(Stepper.delay/1e6)
    is_active[0] = False      # release the hold on further movement

  # Move relative angle from current position:
  def rotate(self, delta):
    while self.is_active[0]:       # wait for prior movement to end
      pass
    self.is_active[0] = True       # place a hold on further movement
    p = multiprocessing.Process(target=self.__rotate, args=(delta,self.is_active))
    p.start()

  # Move to an absolute angle taking the shortest possible path:
  def goAngle(self, angle):
     pass
     # This is a problem for Lab 7!

  # Set the motor zero point
  def zero(self):
    self.angle = 0


# Example use:

from shifter import Shifter

if __name__ == '__main__':

  # Set up the sharable list containing a flag (let's call it is_active) to allow 
  # all processes to determine when a motor is currently moving:
  smm = SharedMemoryManager()
  smm.start()
  sl = smm.ShareableList([False])

  s = Shifter(data=16,latch=20,clock=21)   # set up Shifter

  # Instantiate 2 Steppers:
  m1 = Stepper(s, sl)
  m2 = Stepper(s, sl)

  # Zero the motors:
  m1.zero()
  m2.zero()

  # Move as desired. Each step will occur as soon as the previous steps ends.
  m2.rotate(-90)
  m2.rotate(45)
  m2.rotate(-90)
  m2.rotate(45)


  try:
    while True:
      pass
  except:
    print('\nend')
