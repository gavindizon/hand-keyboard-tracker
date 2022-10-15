import cv2
import mediapipe as mp
from google.protobuf.json_format import MessageToDict


class hand_detector():
    def __init__(self, mode = False, maxHands = 2, modelComplexity = 1, detectionCon =0.5, trackCon =0.5, cx = 0, cy = 0):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplexity = modelComplexity
        self.trackCon = trackCon
        self.cx = cx
        self.cy = cy
        self.finger_dictionary = {
            '4': "thumb",
            '8': 'index',
            '12': 'middle',
            '16': 'ring',
            '20': 'pinky'
        }

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity,  self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        

    def find_hands(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                h, w, c = img.shape
                if(draw):
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        
        return img


    def find_position(self, img, hand_number = 0, draw = True):

        lm_list = []

        if self.results.multi_hand_landmarks and len(self.results.multi_hand_landmarks) > hand_number:
            my_hand = self.results.multi_hand_landmarks[hand_number]

            label = MessageToDict(self.results.multi_handedness[hand_number])['classification'][0]['label']

            if(label == "Right"):
                label = "Left"
            else:
                label = "Right"


            mh, mw, mc = img.shape
            cv2.putText(img, label, (int(my_hand.landmark[0].x * mw), int(my_hand.landmark[0].y * mh)), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
            
            for id, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if draw and id % 4 == 0 and id != 0:
                    lm_list.append([(cx, cy), self.finger_dictionary[str(id)], label])
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        
        return lm_list