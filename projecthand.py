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
        self.udp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        

    def create_header(self,percent):
        pass


    def calculate_hypot(self,x1,y1,x2,y2):
        return math.hypot(x2-x1,y2-y1)


    def calculate_percentage(self,hypot) -> int: 
        percent = np.interp(hypot,[30,270],[0,100])
        return percent
    
    def drone_move_down(self,percent):
        movement_speed = np.interp(percent,[0,40],[-20,-80])
        return movement_speed
    
    def drone_move_up(self,percent):
        movement_speed = np.interp(percent,[60,100],[20,80])
        return movement_speed

    def drone_movement(self,percent):
        movement = "HOLD"
        movement_speed = 0
        if(percent > 40 and percent < 60):
            movement = "HOLD"
        elif(percent<=40):
            movement = "DOWN"
            movement_speed = self.drone_move_donw
        else:
            movement = "UP"
        return movement

    def worker(self):
        while True:
            ## getting frame
            success, image = self.cap.read()
            if success:
                movement = ""
                percent = 0
                img = self.hand.findHands(image,True)
                left_hand,right_hand = self.hand.findposition(image)
                if(len(left_hand)!= 0) and len(right_hand) == 0:
                    thumbpoint = (left_hand[4][1],left_hand[4][2])
                    indexpoint = (left_hand[8][1],left_hand[8][2])
                    hypot = self.calculate_hypot(left_hand[4][1],left_hand[4][2],left_hand[8][1],left_hand[8][2])
                    percent =  self.calculate_percentage(hypot) 
                    movement = self.drone_movement(percent)
                    img = self.hand.draw_line(img,thumbpoint,indexpoint)
                    
                self.cTime = time.time()
                fps = 1/(self.cTime-self.pTime)
                self.pTime = self.cTime
                filling = np.interp(percent,[0,100],[400,150])
                cv2.putText(image,f"{str(int(fps))} fps",(10,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,8,255))
                cv2.putText(image,str(int(percent)),(500,400),cv2.FONT_HERSHEY_COMPLEX,2,(255,8,255))
                print(movement)
                cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
                cv2.rectangle(img,(50,int(filling)),(85,400),(0,255,0),cv2.FILLED)
                cv2.imshow("Image", image)
                # self.udp_client_socket.sendto(self.message,(self.server_address,self.port))
                cv2.waitKey(1)

handdrone = Hand_Drone()
handdrone.worker()
              
