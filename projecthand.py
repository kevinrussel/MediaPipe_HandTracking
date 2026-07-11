from handtrackingmodule import handDetector as hd
import cv2
import mediapipe as mp
import time

widthcam,height = 1000,1000
hand = hd()
cap = cv2.VideoCapture(0)
cap.set(3,widthcam)
cap.set(4,height)
pTime = 0
cTime = 0

    
while True:
    ## getting frame
    success, image = cap.read()
    img = hand.findHands(image,True)
    left_hand,right_hand = hand.findposition(image)
    if(len(left_hand)!= 0) and len(right_hand) == 0:
        thumbpoint = (left_hand[4][1],left_hand[4][2])
        indexpoint = (left_hand[8][1],left_hand[8][2])
        img = hand.draw_line(img,thumbpoint,indexpoint)
    elif(len(left_hand)!= 0) and len(right_hand) != 0:
        print("hitting")
        leftpoint = (left_hand[4][1],left_hand[4][2])
        rightpoint = (right_hand[4][1],right_hand[4][2])
        img = hand.draw_line(img,leftpoint,rightpoint)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(image,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,2,(255,8,255))
    cv2.imshow("Image", image)
    cv2.waitKey(1)
    cv2.waitKey(1)
