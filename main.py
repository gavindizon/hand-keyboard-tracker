import os
import sys
import string

from pynput.keyboard import Listener
import cv2
import pytesseract
from paddleocr import PaddleOCR, draw_ocr

import hand_tracking_module as htm
import utils as utils

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/5.2.0/bin/tesseract'



def main():
#    if not os.geteuid() == 0:
#        sys.exit("\nOnly root can run this script\n")

    lm_list, lm_list2 = [], []
    detector = htm.hand_detector()

    def on_press(key):
        #print("Character: {} CX: {} CY: {} HAND: {}".format(key.char, lm_list[0][1], lm_list[0][2], lm_list[0][3]))
        if len(lm_list) != 0:
            try:
                print('alphanumeric key {} pressed at coordinate: {},{} at hand {} {}'.format(
                    key.char, lm_list[4][1], lm_list[4][2], lm_list[4][3]))
            except AttributeError:
                print('special key {0} pressed'.format(
                    key))

    listener = Listener(on_press=on_press, on_release=None)
    listener.start()
    #ocr = PaddleOCR(use_angle_cls=True, lang="en",)


    cap = cv2.VideoCapture(2)
    keys = dict.fromkeys(string.ascii_uppercase, [])

    MIN = 2000

    #TODO: Detect Key Coordinates Placements
    while utils.not_enough_dict(keys, MIN) == True:
        success, img = cap.read()
        h, w, c = img.shape

#        img = utils.zoom(img, 2)

        #grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #(thresh, grayimg) = cv2.threshold(img, 78, 230, cv2.THRESH_BINARY)
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (thresh, img) = cv2.threshold(img, 78, 230, cv2.THRESH_BINARY)
        img = utils.canny(img)

        boxes = (pytesseract.image_to_boxes(img, config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 11'))
        for b in boxes.splitlines():
            b = b.split(' ')
            print(b)
            if b[0] in keys:
                #keys[b[0]] = (int((int(b[1]) + int(b[3])) / 2), int((int(b[2]) + int(b[4])) / 2))
                if int(b[1]) != 0 and int(b[2]) != 0 and len(keys[b[0]]) < MIN:
                    keys[b[0]].append(utils.midpoint((int(b[1]), int(h/2) + int(b[2])), (int(b[3]), int(h/2) + int(b[4]))))
                #img = cv2.rectangle(img, (int(b[1]), int(h) + int(b[2])), (int(b[3]), int(h) + int(b[4])), (0, 255, 0), 1)

        # for key in keys.keys():
        #     if(len(keys[key]) > 10):
        #         print(key)

        cv2.imshow("Hand Camera", img)
        cv2.waitKey(1)

    print(keys['A'])


    # Detect Hand Movement
    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        lm_list = detector.find_position(img)
        lm_list2 = detector.find_position(img, 1)
        if len(lm_list) != 0:
            print(lm_list[4])

        cv2.imshow("Hand Camera", img)
        cv2.waitKey(1)
        



if __name__ == "__main__":
    main()