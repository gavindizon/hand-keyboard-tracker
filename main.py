import json
import os
import sys
from datetime import datetime

from ctypes import util
from pynput.keyboard import Listener, Key
import cv2

import hand_tracking_module as htm
import utils as utils
import keyboard_mapper as keyboard
import numpy as np

def main():
    lm_list, lm_list2 = [], []
        #CONFIG
    START_COORDINATE = (280,350)
    KEY_SIZE = 60
    SPACING = 10

    FILENAME_PREF = sys.argv[1] if len(sys.argv) > 0 else "DEFAULT"

    # initialize keyboard coordinates
    keys = keyboard.create_keyboard(starting_coordinate=START_COORDINATE, size=KEY_SIZE, spacing=SPACING)
    detector = htm.hand_detector()
    RESULT = []

    def on_press(key): 
        if key == Key.esc:
            print("Saving results...")
            output_dir = os.path.join("output", "{}-{}.json".format(FILENAME_PREF, datetime.now().strftime("%m-%d-%Y_%H-%M-%S")))
            json_object = json.dumps(RESULT, indent=4)
            with open(output_dir, "x") as outfile:
                outfile.write(json_object)
                RESULT.clear()
            print("Results successfully saved.")

        if (len(lm_list) != 0 or len(lm_list2) != 0):
            try:
                RESULT.append(utils.generate_object(lm_list + lm_list2, keys, key.char.upper()))
                print(key.char.upper())
            except AttributeError:
                if(key == Key.space):
                    RESULT.append(utils.generate_object(lm_list + lm_list2, keys, " "))
                    print("<Space>")
            except KeyError:
                print('special key {0} pressed that is not included'.format(key))

    listener = Listener(on_press=on_press, on_release=None)
    listener.start()


    cap = cv2.VideoCapture(2)

    cap.set(3, 1920)
    cap.set(4, 1080)

    # Detect Hand Movement
    while True:
        _, img = cap.read()
        img = detector.find_hands(img)
        lm_list = detector.find_position(img)
        lm_list2 = detector.find_position(img, 1)
        # if len(lm_list) != 0:
        #     print(lm_list[8])

        img = cv2.putText(img, "Testing", (100, 100), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)
        img = cv2.circle(img, (666, 1668), 100, (255, 0, 0), 2)
        # img = cv2.rotate(img, cv2.ROTATE_180)

        # h,  w = img.shape[:2]
        # # New Image shape to generate

        # K = np.array([[0, 0. , 0],
        #               [0. , 50, 0],
        #               [0. , 0., 0.]])

        # # zero distortion coefficients work well for this image
        # D = np.array([0., 0., 0., 0.])

        # Knew = K.copy()
        # Knew[(0,1), (0,1)] = 0.4 * Knew[(0,1), (0,1)]

        # img = cv2.fisheye.undistortImage(img, K, D=D, Knew=Knew)
        
        img = keyboard.show_keyboard(img, keys, starting_coordinate=START_COORDINATE, size=KEY_SIZE, spacing=SPACING)
        cv2.imshow("Hand Camera", img)
        cv2.waitKey(10)
        
if __name__ == "__main__":
    main()