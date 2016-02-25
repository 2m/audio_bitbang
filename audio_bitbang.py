#!/usr/bin/python2
import wave
import time
from RPi import GPIO

SAMP_RATE = 44100
IO_BULK = 10000
BIT_RESOLUTION = 8

class Writer:

	def flush(self):
		self.wavefile.writeframes(self.buffer)
		self.buffer = ""

	def putframe(self, frame):
		self.buffer += chr(frame)
		if len(self.buffer) > READ_BULK:
			self.flush()

	def close(self):
		self.flush()
		self.wavefile.close()

	def __init__(self, filename):
		w = wave.open(filename, 'w')
		w.setnchannels(1)
		w.setsampwidth(1)
		w.setframerate(SAMP_RATE)
		self.wavefile = w

		self.buffer = ""

class Player:

	@staticmethod
	def getframe(wavefile):
		while True:
			frames = wavefile.readframes(IO_BULK)
			if len(frames) == 0:
				break
			for f in frames:
				yield f

	def play(self):
		elapsed = 0
		ignorebits = BIT_RESOLUTION - len(self.pins)
		try:
			wavefile = wave.open(self.filename, 'r')
			last_time = time.time()
			for frame in self.getframe(wavefile):
				byte = frame >> ignorebits # lowering bit resolution
				for pin in self.pins:
					#GPIO.output(pin, byte & 1)
					GPIO.setup(pin, not (byte & 1))
					byte >>= 1
				elapsed += 1
				if elapsed % SAMP_RATE == 0:
					print("%ds" % (elapsed // SAMP_RATE))
		finally:
			wavefile.close()

	def spin(self):
		while True:
			self.play()

	def downgrade(self, filename):
		elapsed = 0
		unit_mask = 1 - (1 << BIT_RESOLUTION)
		mask = (unit_mask << (BIT_RESOLUTION - len(self.pins))) & unit_mask
		try:
			source = wave.open(self.filename, 'r')
			sink = Writer(filename)
			for frame in self.getframe(source):
				byte = frame & mask
				sink.putframe(byte)
				elapsed += 1
				if elapsed % SAMP_RATE == 0:
					print(elapsed / SAMP_RATE)
		finally:
			source.close()
			sink.close()


	def __init__(self, filename, pins):
		self.filename = filename
		self.pins = pins

		GPIO.setmode(GPIO.BCM)
		for pin in pins:
			GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)
			GPIO.setup(pin, GPIO.IN)

p = Player("audio.wav", [17,27,22])
