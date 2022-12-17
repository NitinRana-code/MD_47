import cv2
import numpy as np
import HandTrackingModule as htm
import autopy
import time
# import frontend as fe
# from autopy.mouse import LEFT_BUTTON

import pyautogui

class AiMouse():

    wCam, hCam = 640, 480
    frameR = 80 # Frame Reduction
    
    # print("smoothening = ", smoothening)
    pyautogui.FAILSAFE = False
    tholdY1 = 240
    tholdY2 = 240
    #########################

    

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    detector = htm.handDetector(maxHands=1)
    wScr, hScr = autopy.screen.size()

    def __init__(self, smoothening, allFingersUpCheck, clickFinger,invScr):
        self.smoothening = smoothening
        self.invScr = invScr
        self.allFingersUpCheck = allFingersUpCheck
        self.clickFinger = clickFinger
    

    def run(self):
        print(self.smoothening)
        
        pTime = 0
        plocX, plocY = 0, 0
        clocX, clocY = 0, 0
        while True:
            
            # 1. Find hand Landmarks
            success, img = self.cap.read()
            img = self.detector.findHands(img)
            lmList, bbox = self.detector.findPosition(img)
            # if len(lmList)!=0:
            #     print(lmList[4])
            img = cv2.line(img, (80,240), (560, 240), (255,0,0), 2)
            # 2. Get the tip of the index and middle fingers
            if len(lmList) != 0:
                x1, y1 = lmList[8][1:]
                x2, y2 = lmList[12][1:]
                
            
            # 3. Check which fingers are up
            fingers = self.detector.fingersUp()
            
            cv2.rectangle(img, (self.frameR, self.frameR),(self.wCam - self.frameR, self.hCam - self.frameR), (255, 0, 255), 2)
            
             # all fingers up
            if self.allFingersUpCheck:
                if fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1 and fingers[0]==1:
                    break


            # 4. Only Index Finger : Moving Mode...............................
            if fingers[1] == 1 and (fingers[2]==0 and fingers[0]==0 and fingers[3]==0 and fingers[4]==0):
                
                # 5. Convert Coordinates
                x3 = np.interp(x1, (self.frameR, (self.wCam - self.frameR)-100), (0, self.wScr))
                y3 = np.interp(y1, (self.frameR, (self.hCam - self.frameR)-100), (0, self.hScr))
                
                # 6. Smoothen Values
                clocX = plocX + (x3 - plocX) / self.smoothening
                clocY = plocY + (y3 - plocY) / self.smoothening
            
                # 7. Move Mouse.....................................
                # if length < 40:
                
                try:
                    if (self.invScr==False):
                        autopy.mouse.move((self.wScr-clocX), (clocY))   #subtract clocX with self.wScr to flip the screen
                    else:
                        autopy.mouse.move((clocX), (clocY))
                    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                    plocX, plocY = clocX, clocY
                except:
                    continue

                
            # 8. Both Index and thumb are up : Clicking Mode
            # left click..........................
            if fingers[1] == 1 and fingers[self.clickFinger] == 1:
                print(self.clickFinger)
                # 9. Find distance between fingers
                # length, img, lineInfo = detector.findDistance(8, 12, img)
                # print(length)
                # 10. Click mouse if distance short
                #     cv2.circle(img, (lineInfo[4], lineInfo[5]),
                #     15, (0, 255, 0), cv2.FILLED)
            
                    
                ls = self.detector.lmList[(self.clickFinger+1)*4]
                cx = ls[1]
                cy = ls[2]
                cv2.circle(img, (cx, cy),
                    15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()
                time.sleep(.1)
            
            # right click ..........................
            if fingers[1] == 1 and fingers[2] == 1 and fingers[0]==0 and fingers[3]==0 and fingers[4]==0:
                # Find distance between fingers
                length, img, lineInfo = self.detector.findDistance(8, 12, img)
                
            
                # 10. Click mouse if distance short
                if length < 40:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]),
                    15, (0, 255, 0), cv2.FILLED)
                    pyautogui.click(button = "right", interval=.2)   
                
                # scroll......................
                if length>40:
                    if (y2<self.tholdY2 and y1<self.tholdY1):
                        pyautogui.scroll(100)
                        print("up....")
                    elif(y2>self.tholdY2 and y1>self.tholdY1):
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

if __name__ == "__main__":
    obj = AiMouse(10, False)
    obj.run()
    
