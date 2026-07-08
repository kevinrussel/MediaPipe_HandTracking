import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,max_num_hands=2,min_detection_confidence=0.5,min_tracking_confidence=0.5)

while True:
    ## getting frame
    success, image = cap.read() 
    imageRBG = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    results = hands.process(imageRBG)
    cv2.imshow("Image", image)
    cv2.waitKey(1)