import numpy as np
import cv2
class Circles:
    def __init__(self, debug = False):
        self.debug = debug
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
                if self.debug:
                    cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                    cv2.putText(output, str((-(width//2 - x // zoom), height//2 - y // zoom)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                0.75, (0, 0, 225), 2)
                    cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                    cv2.imshow("output", output)
                return ((-(width // 2 - x // zoom), height // 2 - y // zoom))
            else:
                if self.debug:
                    cv2.imshow("output", output)
                return None
        else:
            if self.debug:
                cv2.imshow("output", output)
            return None
