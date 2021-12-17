import serial.tools.list_ports
import time
import sys

plist = list(serial.tools.list_ports.comports())

if len(sys.argv) != 5:
	a = 1

if len(plist) <= 0:
	print("No valid com!")
else:
	plist_1 = list(plist[0])
	serialName = plist_1[0]
	serialFd = serial.Serial(serialName, 9600, timeout=60)
	print("Available com >>", serialFd.name)
	while True :
		a = input()
		serialFd.write((a).encode())
