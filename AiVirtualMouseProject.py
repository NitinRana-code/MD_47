import cv2
import numpy as np
import HandTrackingModule as htm
import autopy
import time
# from autopy.mouse import LEFT_BUTTON

import pyautogui

##########################
wCam, hCam = 640, 480
frameR = 80 # Frame Reduction
smoothening = 10
pyautogui.FAILSAFE = False
tholdY1 = 240
tholdY2 = 240
#########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()


while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    # if len(lmList)!=0:
    #     print(lmList[4])
    img = cv2.line(img, (80,240), (560, 240), (255,0,0), 2)
    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
       
    
    # 3. Check which fingers are up
    fingers = detector.fingersUp()
    
    cv2.rectangle(img, (frameR, frameR),(wCam - frameR, hCam - frameR), (255, 0, 255), 2)
    
    # 4. Only Index Finger : Moving Mode...............................
    if fingers[1] == 1 and (fingers[2]==0 and fingers[0]==0 and fingers[3]==0 and fingers[4]==0):
        # 5. Convert Coordinates
        x3 = np.interp(x1, (frameR, (wCam - frameR)-100), (0, wScr))
        y3 = np.interp(y1, (frameR, (hCam - frameR)-100), (0, hScr))
        # 6. Smoothen Values
        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening
    
        # 7. Move Mouse.....................................
        autopy.mouse.move(((wScr - clocX)), (clocY))
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        plocX, plocY = clocX, clocY

        
    # 8. Both Index and middle fingers are up : Clicking Mode
    # left click..........................
    if fingers[1] == 1 and fingers[0] == 1:
        # 9. Find distance between fingers
        # length, img, lineInfo = detector.findDistance(8, 12, img)
        # print(length)
        # 10. Click mouse if distance short
        # if length < 40:
        #     cv2.circle(img, (lineInfo[4], lineInfo[5]),
        #     15, (0, 255, 0), cv2.FILLED)
       
            
        ls = detector.lmList[4]
        cx = ls[1]
        cy = ls[2]
        cv2.circle(img, (cx, cy),
            15, (0, 255, 0), cv2.FILLED)
        autopy.mouse.click()
        time.sleep(.1)
    
    # right click ..........................
    if fingers[1] == 1 and fingers[2] == 1:
        # Find distance between fingers
        length, img, lineInfo = detector.findDistance(8, 12, img)
        
       
        # 10. Click mouse if distance short
        if length < 40:
            cv2.circle(img, (lineInfo[4], lineInfo[5]),
            15, (0, 255, 0), cv2.FILLED)
            pyautogui.click(button = "right", interval=.2)   
        
        # scroll......................
        if length>40:
            if (y2<tholdY2 and y1<tholdY1):
                pyautogui.scroll(100)
                print("up....")
            elif(y2>tholdY2 and y1>tholdY1):
                pyautogui.scroll(-100)
                print("down...")
    

    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
    (255, 0, 0), 3)
    # 12. Display
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    if cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
        break
cv2.destroyAllWindows()