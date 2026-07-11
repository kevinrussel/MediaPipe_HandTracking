from handtrackingmodule import handDetector as hd
import cv2
import mediapipe as mp
import time


hand = hd()
cap = cv2.VideoCapture(0)
pTime = 0
cTime = 0

    
while True:
    ## getting frame
    success, image = cap.read()
    img = hand.findHands(image,True)
    landmarklist,specific_point = hand.findposition(image)
    if(len(landmarklist)!= 0):
        left_hand = (specific_point[0][1],specific_point[0][2])
        right_hand = (specific_point[1][1],specific_point[1][2])
        img = hand.draw_line(img,left_hand,right_hand)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(image,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,8,255))
    cv2.imshow("Image", image)
    cv2.waitKey(1)
    cv2.waitKey(1)
