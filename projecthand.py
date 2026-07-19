from handtrackingmodule import handDetector as hd
import cv2
import mediapipe as mp
import time
import math
import numpy as np
import socket
import struct
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
        self.server_address = "192.168.10.2"
        self.port = 8080
        self.already_sent_takeoff = False
        self.udp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        

    def create_header(self,movement,movement_speed):

        timestamp = time.time_ns()
        print(f"{movement} and speed {movement_speed}")

        if(movement == "LAND"):
            command_type = b'l'
            movement_speed = 0
        elif(movement == "TAKEOFF"):
            if(self.already_sent_takeoff):
                return None
            command_type = b't'
            movement_speed = 0
        else:
            command_type = b'm'
        header = struct.pack('!Qch',timestamp,command_type,movement_speed)
        return header
        


    def calculate_hypot(self,x1,y1,x2,y2):
        return math.hypot(x2-x1,y2-y1)


    def calculate_percentage(self,hypot) -> int: 
        percent = np.interp(hypot,[30,270],[0,100])
        return percent
    
    def drone_move_down(self,percent):
        movement_speed = np.interp(percent,[0,40],[-80,-20])
        return movement_speed
    
    def drone_move_up(self,percent):
        movement_speed = np.interp(percent,[60,100],[20,80])
        return movement_speed

    def drone_movement(self,percent):
        movement = "HOLD"
        movement_speed = 0
        if(percent > 40 and percent < 60):
            movement = "HOLD"
        elif (percent == 0):
            movement = "LAND"
            movement_speed = 0
        elif (percent == 100):
                movement = "TAKEOFF"
                movement_speed = 60
        elif(percent<=40):
            movement = "DOWN"
            movement_speed = self.drone_move_down(percent)
        else:
            movement = "UP"
            movement_speed = self.drone_move_up(percent)
        return movement,int(movement_speed)

    def calculate_fps(self):
        self.cTime = time.time()
        fps = 1/(self.cTime-self.pTime)
        self.pTime = self.cTime
        return fps
    
    def image_on_screen(self,img,fps,percent,movement):
        filling = np.interp(percent,[0,100],[400,150])
        cv2.putText(img,f"{str(int(fps))} fps",(10,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,8,255))
        cv2.putText(img,str(int(percent)),(500,400),cv2.FONT_HERSHEY_COMPLEX,2,(255,8,255))
        if movement == "HOLD":
            color = (70,253,76)
        elif movement == "UP":
            color = (0,0,255)
        elif movement == "DOWN":
            color = (255,0,0)
        else:
            color = (51,255,255)
        cv2.putText(img,str(movement),(200,200),cv2.FONT_HERSHEY_COMPLEX,2,color)   
        cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
        cv2.rectangle(img,(50,int(filling)),(85,400),(0,255,0),cv2.FILLED)
        cv2.imshow("Image", img)

    def worker(self):
        while True:
            ## getting frame
            success, image = self.cap.read()
            if success:
                movement = ""
                movement_speed = 0
                percent = 0
                img = self.hand.findHands(image,True)
                left_hand,right_hand = self.hand.findposition(image)
                if(len(left_hand)!= 0) and len(right_hand) == 0:
                    thumbpoint = (left_hand[4][1],left_hand[4][2])
                    indexpoint = (left_hand[8][1],left_hand[8][2])
                    hypot = self.calculate_hypot(left_hand[4][1],left_hand[4][2],left_hand[8][1],left_hand[8][2])
                    percent =  self.calculate_percentage(hypot) 
                    movement,movement_speed = self.drone_movement(percent)
                    img = self.hand.draw_line(img,thumbpoint,indexpoint)
                    header = self.create_header(movement,movement_speed)
                    if(header):
                        self.udp_client_socket.sendto(header,(self.server_address,self.port))

                fps = self.calculate_fps()
                self.image_on_screen(img,fps,percent,movement)
                cv2.waitKey(1)

handdrone = Hand_Drone()
handdrone.worker()
              
