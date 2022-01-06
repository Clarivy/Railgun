import numpy as np
import copy
import cv2
import time
class Circles:
    def __init__(self, debug = False):
        self.debug = debug
        self.x = None
        self.y = None
        self.r = None
    def rgb2hsv(self,r, g, b):
        r, g, b = r/255.0, g/255.0, b/255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        m = mx-mn
        if mx == mn:
            h = 0
        elif mx == r:
            if g >= b:
                h = ((g-b)/m)*60
            else:
                h = ((g-b)/m)*60 + 360
        elif mx == g:
            h = ((b-r)/m)*60 + 120
        elif mx == b:
            h = ((r-g)/m)*60 + 240
        if mx == 0:
            s = 0
        else:
            s = m/mx
        v = mx
        H = h / 2
        S = s * 255.0
        V = v * 255.0
        return H, S, V
    def center(self,img,zoom=1,thres = 3):
        raw_height, raw_width = img.shape[:2]
        if self.x is not None:
            height, width = img.shape[:2]
            img = copy.copy(img[max(self.y-self.r,0):min(self.y+self.r,height),max(self.x-self.r,0):min(self.x+self.r,width)])

        height, width = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        image = img
        gray = cv2.resize(gray, (0, 0), fx=zoom, fy=zoom)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 1)
        if circles is not None:
            if circles.shape[1] > thres:
                circles = np.median(circles,axis=0)
                circles = np.round(circles[0, :]).astype("int")
                x, y, r = circles
                x = int(x // zoom)
                y = int(y // zoom)
                r = int(r // zoom)

                check = image[ max(y - 20,1):min(y + 20, height) ,max(x - 20,1):min(x + 20,width) , :]
                hsv=[]
                for i in range(10):
                    for j in range(10):
                        hsv.append(self.rgb2hsv(check[i,j,0],check[i,j,1],check[i,j,2]))
                hsv = np.mean(np.array(hsv),axis = 0)       
                if self.debug:
                    output = copy.deepcopy(image)
                    cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                    cv2.putText(output, str((-(width // 2 - x), height // 2 - y)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                0.75, (0, 0, 225), 2)
                    cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                    cv2.imshow("output", output)
                    #print(hsv)
                if hsv[0] < 110 and hsv[0] > 70:
                    if self.x is not None:
                        xold = self.x
                        yold = self.y
                        rold = self.r
                        self.x = x
                        self.y = y
                        self.r = max(r,50)
                        x = x + max(xold - rold,0)
                        y = y + max(yold - rold,0)
                    else:
                        self.x = x
                        self.y = y
                        self.r = max(r,50)
                    return ((-(raw_width // 2 - x), raw_height // 2 - y))
                else:
                    self.x = None
                    self.y = None
                    self.r = None
                    return None
            else:
                self.x = None
                self.y = None
                self.r = None
                if self.debug:
                    cv2.imshow("output", image)
                return None
        else:
            self.x = None
            self.y = None
            self.r = None
            if self.debug:
                cv2.imshow("output", image)
            return None

