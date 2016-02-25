#!/usr/bin/python3
from RPi import GPIO

GPIO.setmode(GPIO.BCM)

class Out():

  def __init__(self, pins):
    self.pins = pins
    for pin in pins:
      #GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
      GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)
      GPIO.setup(pin, GPIO.IN)

  def set(self, i):
    for pin in self.pins:
      #GPIO.output(pin, i & 1)
      GPIO.setup(pin, not (i & 1)) # GPIO.IN == 1, GPIO.OUT = 0
      i >>=1

o = Out([17, 27, 22])
