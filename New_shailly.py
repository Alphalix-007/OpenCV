import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import numpy as np

from cvzone.FaceDetectionModule import FaceDetector
from cvzone.SerialModule import SerialObject
from playsound import playsound
from threading import Thread

arduino = SerialObject("COM9")

# import pygame
# from pygame.locals import *
# from pygame import mixer

# mixer.init()
# mixer.music.load('bensound-summer_mp3_music.mp3')
# mixer.music.play()
# pygame.mixer.music.play(loops=-1)

cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)
alarm_sound="Calling Santa.mp3"
alarm_on=False
def start_alarm(sound):
    playsound('Calling Santa.mp3')

def play(alarm_on):
    if(alarm_on==True):
        t=Thread(target=start_alarm,args=(alarm_sound,))
        t.daemon=True
        t.start()
        


count=0
flag=0
while True:
    success, img = cap.read()
    imgText = np.zeros_like(img)
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        pointLeft = face[145]
        pointRight = face[374]
        w, _ = detector.findDistance(pointLeft, pointRight)
        W = 6.3

        # Finding distance
        f = 840
        d = (W * f) / w
        #print(d)

        if(d<200):
            if flag==0and count>20:
                print("$")
                alarm_on=True
                flag+=1
                play(alarm_on)
            count = count+1
            #print(count,"*")
            if(count>200):
                arduino.sendData([0])
                # print("YES")
        else:
            arduino.sendData([1])
                # print("No")
            alarm_on=False
            play(alarm_on)
            count=0

        cvzone.putTextRect(img, f'Depth: {int(d)}cm',
                           (face[10][0] - 100, face[10][1] - 50),
                           scale=2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break                 

    imgStacked = cvzone.stackImages([img], 2,1)
    cv2.imshow("Image", imgStacked)
    cv2.waitKey(1)