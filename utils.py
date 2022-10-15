import cv2 as cv
import numpy as np
import math

def not_enough_dict(d, min = 10):
    for _, value in d.items():
        if len(value) < min:
            return True
    return False

def zoom(img, zoom_factor=2):
    return cv.resize(img, None, fx=zoom_factor, fy=zoom_factor)

def midpoint(p1, p2):
    return ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)

def closest(pressed_key, landmarks):
    np_landmarks = np.array(landmarks, dtype=object)[:,0]


    print(np_landmarks, pressed_key)
    distance = list(map(lambda z : abs(math.sqrt((z[0] - pressed_key[0])**2 + (z[0] - pressed_key[0])**2)), np_landmarks))

    min_value = min(distance)
    idx = distance.index(min_value)

    return landmarks[idx]





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

    