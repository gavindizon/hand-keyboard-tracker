import cv2 as cv
import numpy as np

def not_enough_dict(d, min = 10):
    for _, value in d.items():
        if len(value) < min:
            return True
    return False

def zoom(img, zoom_factor=2):
    return cv.resize(img, None, fx=zoom_factor, fy=zoom_factor)

def midpoint(p1, p2):
    return ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)

#dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv.morphologyEx(image, cv.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv.Canny(image, 100, 200)