from operator import truediv
from typing import Any
from cv2 import waitKey
import mediapipe as mp
import time
import cv2

# creating useful objects
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
while True:
    success, img = cap.read()

    # converting the image to RGB to process
    imgRgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # process the image and gives the landmarks of the each finger
    results = hands.process(imgRgb)
    # print(type(results.multi_hand_landmarks))

    # drawing landmarks of the screen
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks: # gives the list of finger coordinates in every frame --> it is a 2D list
            for id, lms in enumerate(handlms.landmark): # gives the coordinate of fingers(hand) of each frame
                h, w , c = img.shape
                cx, cy = int(lms.x*w), int(lms.y*h)
                
                if(id == 4):
                    # cv2.circle(img, (cx, cy), 15, (0,0,255), 15, cv2.FILLED)
                    pass

            mpDraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS,
                                     mpDraw.DrawingSpec(color = (255, 255, 255)),
                                     mpDraw.DrawingSpec(color = (115, 115, 115)),
                                 )
                                     

                



    key = waitKey(1)
    # print(key)
    cv2.imshow("project", img)
    if(key == 27):
        break