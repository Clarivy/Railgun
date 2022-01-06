import time
import sys

class Comm():
	def __init__(self, debug = False):
		print("Communicator module is in debug mode!")
		self.debug = debug

	def write(self, ch):
		if self.debug:
			print(ch)
