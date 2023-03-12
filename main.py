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
import json

def main():
    lm_list, lm_list2 = [], []
    #CONFIG
    START_COORDINATE = (280,350)
    KEY_SIZE = 60
    SPACING = 10

    # LAYOUTS
    SALVO = ["1234567890-","DHRLWBKYEU", "STNGPMIAO;'", "ZXCVQFJ,.?"]
    TYPHE_H = ["1234567890-", "QWEDRUYKPJ", "ZASTGNIOL;'", "XVFCBMH,.?"]
    TYPHE_LP = ["1234567890-", "", ";'", ",.?"]

    QWERTY_TO_SALVO =  {}
    QWERTY_TO_TYPHE_H = {}

    # get salvo mapping from salvo json file
    with open('salvo.json') as json_file:
        QWERTY_TO_SALVO = json.load(json_file)

   # get salvo mapping from salvo json file
    with open('heuristic.json') as json_file:
        QWERTY_TO_TYPHE_H = json.load(json_file)

    FILENAME_PREF = sys.argv[1] if len(sys.argv) > 0 else "DEFAULT"
    LAYOUT = "QWERTY"

    if len(sys.argv) > 2:
        LAYOUT = str(sys.argv[2]).upper()

    # initialize keyboard coordinates
    # keys = keyboard.create_keyboard(mapping=SALVO, starting_coordinate=START_COORDINATE, size=KEY_SIZE, spacing=SPACING)

    switch_keys = {
        "SALVO": keyboard.create_keyboard(mapping=SALVO, starting_coordinate=START_COORDINATE, size=KEY_SIZE, spacing=SPACING),
        "TYPHE_H": keyboard.create_keyboard(mapping=TYPHE_H, starting_coordinate=START_COORDINATE, size=KEY_SIZE, spacing=SPACING)
    }

    keys = switch_keys[LAYOUT]
    detector = htm.hand_detector()
    RESULT = []

    def map_on_layout(raw_letter, layout = LAYOUT):
        switcher = {
            "SALVO": QWERTY_TO_SALVO[raw_letter],
            "TYPHE_H": QWERTY_TO_TYPHE_H[raw_letter],
            "QWERTY": raw_letter
        }
        return switcher.get(layout, raw_letter)

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
                raw_letter = key.char.upper()
                key_convert = map_on_layout(raw_letter)
                RESULT.append(utils.generate_object(lm_list + lm_list2, keys, key_convert))
                print("Pressed key: "+ key_convert)
            except AttributeError:
                if(key == Key.space):
                    RESULT.append(utils.generate_object(lm_list + lm_list2, keys, " "))
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

        img = cv2.putText(img, "Testing", (100, 100), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)
        img = cv2.circle(img, (666, 1668), 100, (255, 0, 0), 2)
        img = keyboard.show_keyboard(img, keys, starting_coordinate=START_COORDINATE, size=KEY_SIZE, spacing=SPACING)
        cv2.imshow("Hand Camera", img)
        cv2.waitKey(10)
        
if __name__ == "__main__":
    main()
