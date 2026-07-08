import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(1)

while True:
    ## getting frame
    success, image = cap.read() 
    cv2.imshow("Image", image)
    cv2.waitKey(1)