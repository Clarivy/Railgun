import threading
import numpy as np
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


class Dectector:
    
    def __init__(self, id = 0):
        self.cam = cv2.VideoCapture(id)
        if not self.cam.isOpened():
            raise Exception("Cannot Open camera in " + str(id))
        self.__curFrame = None
        self.frame = None
        self.exitFlag = False
        self.lock = threading.Lock()
        self.crossCount = 0

    def UpdateFrame(self):
        lst_clk = 0
        
        while not self.exitFlag:
            lst_clk = time.time()
            suc, self.__curFrame = self.cam.read()
            if not suc:
                print("Cannot read frame")
                continue
            with self.lock:
                self.frame = copy.deepcopy(self.__curFrame)
            self.camFPS = 1 / (time.time() - lst_clk + 1e-7)

    def process(self,img,zoom=1,thres = 20):
        while not self.exitFlag:
            vedio = cv2.VideoCapture(0)
            img = vedio.read()
            a=Circles(debug = False)
            _, img = vedio.read()
            location = a.center(img,zoom,thres)
            # # Exit if ESC pressed
            k = cv2.waitKey(1) & 0xff
            if k == 27: break


    def GetLocation(self):
        return self.location
    
    def ListenerBegin(self):
        try:
            self.camThread = multThread(self.UpdateFrame)
            self.camThread.start()

            time.sleep(2)
            self.GetThres()

            self.procThread = multThread(self.process)
            self.procThread.start()

            time.sleep(2)
        except:
            print ("Error0: Cannot start update frame thread")


    def ListenerEnd(self):
        self.exitFlag = True
        self.camThread.join()

