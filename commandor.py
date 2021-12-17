import serial.tools.list_ports
import time
import sys

class Comm():
	def __init__(self, com_id = 0):
		plist = list(serial.tools.list_ports.comports())
		if len(plist) <= 0:
			print("No valid com!")
		try:
			com = list(plist[com_id])
			serialName = com[0]
			self.serialFd = serial.Serial(serialName, 9600, timeout=60)
		except:
			print("Cannot open com" + str(com_id))

	def write(self, ch):
		return self.serialFd.write(ch.encode())
