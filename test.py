import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy.mouse
import autopy
import pyautogui

time.sleep(5)

cap =  cv2.VideoCapture(0)

ht = htm.handDetector()
while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = ht.findHands(img)
    lmList, bbox = ht.findPosition(img)
    ls=ht.fingersUp()
    # print(ls)

    cv2.imshow("img", img)
    key = cv2.waitKey(1)
    if key == 27:
        break
    
    ls2 = ht.fingersDown()
    print(ls2)
    # if(ls[1]==1 and ls[2]==1) and (ls[3]==0 and ls[4] ==0 and ls[0] == 0):
    #     pyautogui.scroll(clicks=100)
    