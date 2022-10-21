import string
from ctypes import util
from pynput.keyboard import Listener, Key
import cv2

import hand_tracking_module as htm
import utils as utils
import keyboard_mapper as keyboard

def main():
    lm_list, lm_list2 = [], []
        #CONFIG
    START_COORDINATE = (280,650)
    KEY_SIZE = 60
    SPACING = 10

    # initialize keyboard coordinates
    keys = keyboard.create_keyboard(starting_coordinate=START_COORDINATE, size=KEY_SIZE, spacing=SPACING)
    detector = htm.hand_detector()

    def on_press(key):
        #print("Character: {} CX: {} CY: {} HAND: {}".format(key.char, lm_list[0][1], lm_list[0][2], lm_list[0][3]))
        if (len(lm_list) != 0 or len(lm_list2) != 0):
            try:
                print('alphanumeric key {}'.format(key.char))
                print(utils.closest(keys[key.char.upper()], lm_list + lm_list2))
            except AttributeError:
                if(key == Key.space):
                    print('alphanumeric key {}'.format(key))
                    print(utils.closest(keys[' '], lm_list + lm_list2))
                else:
                    print('special key {0} pressed'.format(key))

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
        
        img = keyboard.show_keyboard(img, keys, starting_coordinate=START_COORDINATE, size=KEY_SIZE, spacing=SPACING)
        cv2.imshow("Hand Camera", img)
        cv2.waitKey(10)
        
if __name__ == "__main__":
    main()