import numpy as np
import threading
import time
import copy
import cv2
from circle import Circles

exitFlag = False

class multThread(threading.Thread):
    def __init__(self, func):
        threading.Thread.__init__(self)
        self.func = func

    def run(self):
        print ("Begin: " + self.name)
        self.func()
        print ("End: " + self.name)


class Detector:
    
    def __init__(self, id = 0, flip = True, debug = True, xBias = 0, yBias = 0, printFPS = True, zoom = 1):
        self.cam = cv2.VideoCapture(id)
        if not self.cam.isOpened():
            raise Exception("Cannot Open camera in " + str(id))
        self.__curFrame = None
        self.frame = None
        self.exitFlag = False
        self.lock = threading.Lock()
        self.crossCount = 0
        self.flip = flip
        self.debug = debug
        self.yBias = yBias
        self.xBias = xBias
        self.printFPS = printFPS
        self.zoom = zoom
        self.circles = Circles(debug=self.debug)
    def UpdateFrame(self):
        lst_clk = 0
        
        while not self.exitFlag:
            lst_clk = time.time()
            suc, self.__curFrame = self.cam.read()
            if self.flip:
                self.__curFrame = cv2.flip(self.__curFrame, -1)
            if not suc:
                print("Cannot read frame")
                continue
            with self.lock:
                self.frame = copy.deepcopy(self.__curFrame)
            self.camFPS = 1 / ((time.time() - lst_clk)+0.01)
            #if self.debug:
            #    print("FPS: " + str(self.camFPS))

    def process(self, thres = 25):
        self.location = None
        count = 0
        lst_clk = 0
        while not self.exitFlag:
            lst_clk = time.time()
            # vedio = cv2.VideoCapture(0)
            # img = vedio.read()

            img = self.frame
            loc = self.circles.center(img,self.zoom,thres)
            if loc != None:
                self.location = (self.xBias + loc[0], self.yBias + loc[1])
                count = 0
            else:
                count += 1
                if count >= 15:
                    self.location = None
                    count = 0
            # location_all = np.zeros(shape=(5,2))
            # for i in range(5):
            #     if self.location != None:
            #         location_all[i] = (self.location)
            
            # # Exit if ESC pressed
            camFPS = 1 / (time.time() - lst_clk)
            if self.printFPS == True:
                print("Process FPS: " + str(camFPS))
            k = cv2.waitKey(1) & 0xff
            if k == 27: break

    
    def ListenerBegin(self):
        try:
            self.camThread = multThread(self.UpdateFrame)
            self.camThread.start()

            time.sleep(2)
            

            self.procThread = multThread(self.process)
            self.procThread.start()

            time.sleep(2)
        except:
            print ("Error0: Cannot start update frame thread")

    def ListenerEnd(self):
        self.exitFlag = True
        self.camThread.join()
        self.procThread.join()
        

    def GetLocation(self):
        return self.location  


if __name__ == '__main__': 
    exitFlag = False
    detector = Detector()
    detector.ListenerBegin()
    
    while True:
        location = detector.GetLocation()
        print(location)
        time.sleep(0.1)

