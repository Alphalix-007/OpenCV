from cvzone.SerialModule import SerialObject
from time import sleep

ardunio= SerialObject("COM9")

while True:
    ardunio.sendData([1])
    sleep(3)
    ardunio.sendData([0])
    sleep(1)