from communicator import Comm
from detector import Detector
import time

comm = Comm()
dect = Detector(debug = False, flip = False)

dect.ListenerBegin()
try:
    comm.write("o")
    while True:
        loc = dect.GetLocation()
        print(loc)
        if loc:
            if abs(loc[0]) >= 15:
                if loc[0] < 0:
                    comm.write("l")
                else:
                    comm.write("r")
            else:
                ch = input()
                if ch == "q":
                    continue
        else:
            comm.write("c")
        time.sleep(0.2)
finally:
    dect.ListenerEnd()
