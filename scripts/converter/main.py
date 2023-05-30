import os
import json
import numpy as np
import math
import copy
from datetime import datetime

def closest(pressed_key, landmarks):
    np_landmarks = np.array(landmarks, dtype=object)[:,0]
    #print(np_landmarks, pressed_key)
    distance = list(map(lambda z : abs(math.sqrt((z[0] - pressed_key[0])**2 + (z[0] - pressed_key[0])**2)), np_landmarks))
    min_value = min(distance)
    idx = distance.index(min_value)

    return idx


items = []
SALVO = {}
with open('salvo.json') as json_file:
    SALVO = json.load(json_file)

with open('./input/input4.json') as json_file:
    items = json.load(json_file)

salvo_mappings = {'1': (270, 310), '2': (340, 310), '3': (410, 310), '4': (480, 310), '5': (550, 310), '6': (620, 310), '7': (690, 310), '8': (760, 310), '9': (830, 310), '0': (900, 310), '-': (970, 310), 'D': (310, 380), 'H': (380,
380), 'R': (450, 380), 'L': (520, 380), 'W': (590, 380), 'B': (660, 380), 'K': (730, 380), 'Y': (800, 380), 'E': (870, 380), 'U': (940, 380), 'S': (330, 450), 'T': (400, 450), 'N': (470, 450), 'G': (540, 450), 'P': (610, 450), 'M': (680, 450), 'I': (750, 450), 'A': (820, 450), 'O': (890, 450), ';': (960, 450), "'": (1030, 450), 'Z': (350, 520), 'X': (420, 520), 'C': (490, 520), 'V': (560, 520), 'Q': (630, 520), 'F': (700, 520),
'J': (770, 520), ',': (840, 520), '.': (910, 520), '?': (980, 520), ' ': (630, 590)}

new_item = []
 
for item in items:
    temp = item.copy()

    keyPressed = SALVO[temp["keyPressed"]]
    indx = closest(salvo_mappings[keyPressed], temp['landmarks'])

    temp['hand'] = temp['landmarks'][indx][2]
    temp['finger'] = temp['landmarks'][indx][1]
    temp['activeLandmarkLoc'] = temp['landmarks'][indx][0]
    temp['keyPressed'] = keyPressed
    new_item.append(temp)

output_dir = os.path.join("output", "{}-{}.json".format("converted", datetime.now().strftime("%m-%d-%Y_%H-%M-%S")))
json_object = json.dumps(new_item, indent=4)
with open(output_dir, "x") as outfile:
    outfile.write(json_object)












