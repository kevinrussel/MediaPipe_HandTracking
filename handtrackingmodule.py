import cv2
import mediapipe as mp
import time
import struct
class handDetector():

    def __init__(self, mode = False,max_hands = 2, min_detection_confidence = 0.5, track_confidence =0.5):
        
        self.mode = mode
        self.max_hands = max_hands
        self.min_detection_confidence = min_detection_confidence
        self.track_confidence = track_confidence
        self.mpHands = mp.solutions.hands
        
        self.hands = self.mpHands.Hands(self.mode,self.max_hands,1,self.min_detection_confidence,self.track_confidence)
        self.mpDraw = mp.solutions.drawing_utils
       
    '''
    This function plots out where each point is on the hand.
    '''
    def findHands(self,image,draw=True):
        imageRBG = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRBG)
        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image,hand,self.mpHands.HAND_CONNECTIONS)
        return image

    

    '''
    This function draws a line between two points
    '''
    def draw_line(self,image,left_point,right_point):
        return cv2.line(image,left_point,right_point,(0, 255, 0), 3)
    

    def append_hand_positions_to_list(self,hand, height, width, channel):
        positions = []
        for id,landmark in enumerate(hand.landmark):
            ## normalizing now
            cx,cy = int(landmark.x*width), int(landmark.y*height)
            positions.append([id,cx,cy])
        return positions
    
    



    '''
    This function returns the list of positions of both hands when they are BOTH present.
    '''
    def findposition(self,image,handNumber = 0):
        left_hand = []
        right_hand = []
        h,w,c = image.shape
        if self.results.multi_hand_landmarks:
            if len(self.results.multi_hand_landmarks) == 2:        
                myhand = self.results.multi_hand_landmarks[0]
                left_hand = self.append_hand_positions_to_list(myhand,h,w,c)
                myhand = self.results.multi_hand_landmarks[1]
                right_hand = self.append_hand_positions_to_list(myhand,h,w,c)
            elif len(self.results.multi_hand_landmarks) == 1:
                myhand = self.results.multi_hand_landmarks[0]
                left_hand = self.append_hand_positions_to_list(myhand,h,w,c)
        return left_hand, right_hand

def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0
    detector = handDetector()
    
    while True:
        ## getting frame
        success, image = cap.read()
        img = detector.findHands(image,True)
        landmarklist = detector.findposition(image)

        if(len(landmarklist)!= 0):
            print(landmarklist[4])
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(image,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,8,255))
        cv2.imshow("Image", image)
        cv2.waitKey(1)
        cv2.waitKey(1)




if __name__ == '__main__':
    main()

