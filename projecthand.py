from handtrackingmodule import handDetector as hd
import cv2
import mediapipe as mp
import time
import math
import numpy as np
import socket
class Hand_Drone:

    def __init__(self):
        self.widthcam = 1000
        self.height =1000
        self.hand = hd()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3,self.widthcam)
        self.cap.set(4,self.height)
        self.pTime = 0
        self.cTime = 0
        self.server_address = "127.0.0.1"
        self.port = 8080

message = b"hello world"
def calculate_hypot(x1,y1,x2,y2):
    return math.hypot(x2-x1,y2-y1)

udp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    
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



    filling = np.interp(percent,[0,100],[400,150])


    cv2.putText(image,f"{str(int(fps))} fps",(10,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,8,255))
    cv2.putText(image,str(int(percent)),(500,400),cv2.FONT_HERSHEY_COMPLEX,2,(255,8,255))
    
    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(filling)),(85,400),(0,255,0),cv2.FILLED)
    cv2.imshow("Image", image)
    udp_client_socket.sendto(message,(server_address,port))
    cv2.waitKey(1)
    cv2.waitKey(1)
