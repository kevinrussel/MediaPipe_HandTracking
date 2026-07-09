import cv2
import mediapipe as mp
import time


mpDraw = mp.solutions.drawing_utils
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,max_num_hands=2,min_detection_confidence=0.5,min_tracking_confidence=0.5)

class handDetector():
    def __init__(self, mode = False,max_hands = 2, min_detection_confidence = 0.5, track_confidence =0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.min_detection_confidence = min_detection_confidence
        self.track_confidence = track_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.max_hands,self.min_detection_confidence,self.track_confidence)
        
        

        pass
def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0
    while True:
    ## getting frame
    success, image = cap.read() 
    imageRBG = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    results = hands.process(imageRBG)
    
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            for id,lndmrk in enumerate(hand.landmark):
                h,w,c = image.shape
                ## normalizing now
                cx,cy = int(lndmrk.x*w), int(lndmrk.y*h)
                print(id,cx,cy)
            mpDraw.draw_landmarks(image,hand,mpHands.HAND_CONNECTIONS)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(image,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,8,255))
    cv2.imshow("Image", image)
    cv2.waitKey(1)




if __name__ == '__main__':
    main()

