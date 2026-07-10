import cv2
import mediapipe as mp
import time

class handDetector():


    def __init__(self, mode = False,max_hands = 2, min_detection_confidence = 0.5, track_confidence =0.5):
        
        self.mode = mode
        self.max_hands = max_hands
        self.min_detection_confidence = min_detection_confidence
        self.track_confidence = track_confidence
        self.mpHands = mp.solutions.hands
        
        self.hands = self.mpHands.Hands(self.mode,self.max_hands,1,self.min_detection_confidence,self.track_confidence)
        self.mpDraw = mp.solutions.drawing_utils
       

    def findHands(self,image,draw=True):
        imageRBG = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        results = self.hands.process(imageRBG)
        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image,hand,self.mpHands.HAND_CONNECTIONS)
                # for id,lndmrk in enumerate(hand.landmark):
                #     h,w,c = image.shape
                #     ## normalizing now
                #     cx,cy = int(lndmrk.x*w), int(lndmrk.y*h)
                #     print(id,cx,cy)
                # mpDraw.draw_landmarks(image,hand,mpHands.HAND_CONNECTIONS)
        return image
    
    def FindPosition(self):
        
def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0
    detector = handDetector()
    
    while True:
        ## getting frame
        success, image = cap.read()
        img = detector.findHands(image,True)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(image,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,8,255))
        cv2.imshow("Image", image)
        cv2.waitKey(1)
        cv2.waitKey(1)




if __name__ == '__main__':
    main()

