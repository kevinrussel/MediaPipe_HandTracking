from handtrackingmodule import handDetector as hd
import cv2
import mediapipe as mp
import time
import math
import numpy as np



widthcam,height = 1000,1000
hand = hd()
cap = cv2.VideoCapture(0)
cap.set(3,widthcam)
cap.set(4,height)
pTime = 0
cTime = 0

def calculate_hypot(x1,y1,x2,y2):
    return math.hypot(x2-x1,y2-y1)


    
while True:
    ## getting frame
    success, image = cap.read()
    img = hand.findHands(image,True)
    left_hand,right_hand = hand.findposition(image)
    percent = 0
    if(len(left_hand)!= 0) and len(right_hand) == 0:
        thumbpoint = (left_hand[4][1],left_hand[4][2])
        indexpoint = (left_hand[8][1],left_hand[8][2])
        hypot = calculate_hypot(left_hand[4][1],left_hand[4][2],left_hand[8][1],left_hand[8][2])
        percent = np.interp(hypot,[30,270],[0,100])
        if(percent > 40 and percent < 60):
            print("HOLD")
        elif(percent<=40):
            print("DOWN")
        else:
            print("UP")
        img = hand.draw_line(img,thumbpoint,indexpoint)
        
    # elif(len(left_hand)!= 0) and len(right_hand) != 0:
    #     leftpoint = (left_hand[8][1],left_hand[8][2])
    #     rightpoint = (right_hand[8][1],right_hand[8][2])
    #     img = hand.draw_line(img,leftpoint,rightpoint)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(image,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,2,(255,8,255))
    cv2.putText(image,str(int(percent)),(500,400),cv2.FONT_HERSHEY_COMPLEX,2,(255,8,255))
    cv2.rectangle(image,(200,200),(300,300),color=(255, 255, 255))
    cv2.imshow("Image", image)
    cv2.waitKey(1)
    cv2.waitKey(1)
