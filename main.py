from re import T
from communicator import Comm
from detector import Detector
import time
import keyboard

chargetime = 1
charge = False
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
                #comm.write("O")
                if loc[0] < 0:
                    comm.write("l")
                else:
                    comm.write("r")
            elif abs(loc[1]) >= 15:
                if loc[1] < 0:
                    comm.write("d")
                else:
                    comm.write("u")
            else:#lock on
                print("press charge time")
                while True:
                    key = keyboard.read_key(suppress=False)
                    if key in ['1','2','3','4','5']:
                        chargetime = key
                        comm.write(chargetime)
                        time.sleep(0.5)
                    elif key == 'r':
                        comm.write('b')
                        time.sleep(5)
                        comm.write('f')
                        time.sleep(5)
                    elif key == 'f':
                        comm.write('f')
                        charge = False
                        time.sleep(0.5)
                    elif key == 'c' and not charge:
                        charge = True
                        comm.write('c')
                        time.sleep(0.5)
                    elif key == 'q':
                        comm.write("o")
                        break
                    else:
                        print(f"press 1 to 5 to set charge time\npress c to charge\npress f to fire\npress q to quit")                    
        else:
            comm.write("p")
        time.sleep(0.4)
finally:
    dect.ListenerEnd()
    comm.write("o")
