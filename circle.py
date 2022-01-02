import numpy as np
import cv2
import time
class Circles:
    def __init__(self, debug = False):
        self.debug = debug
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
    def center(self,img,zoom=3,thres = 3):
        height, width = img.shape[:2]
        output = cv2.resize(img, (0, 0), fx=zoom, fy=zoom)
        image = cv2.resize(img, (0, 0), fx=zoom, fy=zoom)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 1)
        if circles is not None:
            if circles.shape[1] > thres:
                circles = np.median(circles,axis=0)
                circles = np.round(circles[0, :]).astype("int")
                x, y, r = circles

                check = image[ max(y - 20,1):min((y + 20),height*zoom) ,max(x - 20,1):min((x + 20),width*zoom) , :]
                hsv=[]
                for i in range(10):
                    for j in range(10):
                        hsv.append(self.rgb2hsv(check[i,j,0],check[i,j,1],check[i,j,2]))
                hsv = np.mean(np.array(hsv),axis = 0)       
                if self.debug:
                    cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                    cv2.putText(output, str((-(width//2 - x // zoom), height//2 - y // zoom)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                0.75, (0, 0, 225), 2)
                    cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                    cv2.imshow("output", output)
                if hsv[0] < 110 and hsv[0] > 75:
                    return ((-(width // 2 - x // zoom), height // 2 - y // zoom),hsv)
                else:
                    return None
            else:
                if self.debug:
                    cv2.imshow("output", output)
                return None
        else:
            if self.debug:
                cv2.imshow("output", output)
            return None

