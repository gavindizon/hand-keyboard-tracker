import os
import sys
import string

from pynput.keyboard import Listener
import cv2

import hand_tracking_module as htm
import utils as utils





def main():
    if not os.geteuid() == 0:
        sys.exit("\nOnly root can run this script\n")

    lm_list, lm_list2 = [], []
    detector = htm.hand_detector()

    def on_press(key):
        #print("Character: {} CX: {} CY: {} HAND: {}".format(key.char, lm_list[0][1], lm_list[0][2], lm_list[0][3]))
        if len(lm_list) != 0:
            try:
                print('alphanumeric key {0} pressed'.format(
                    key.char))
            except AttributeError:
                print('special key {0} pressed'.format(
                    key))

    listener = Listener(on_press=on_press, on_release=None)
    listener.start()


    cap = cv2.VideoCapture(2)
    keys = dict.fromkeys(string.ascii_lowercase, None)


    #TODO: Detect Key Coordinates Placements
    while utils.none_in_dict(keys) == True:
        success, img = cap.read()
        print("None")

        cv2.imshow("Hand Camera", img)
        cv2.waitKey(1)


    # Detect Hand Movement
    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        lm_list = detector.find_position(img)
        lm_list2 = detector.find_position(img, 1)

        cv2.imshow("Hand Camera", img)
        cv2.waitKey(1)
        



if __name__ == "__main__":
    main()