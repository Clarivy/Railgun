from commandor import Comm
from detector import Detector
import time

comm = Comm()
dect = Detector()

dect.ListenerBegin()

try:
	while True:
		loc = dect.GetLocation()
		if loc:
			if loc[0] < 0:
				comm.write("l")
			else:
				comm.write("r")
finally:
	dect.ListenerEnd()
