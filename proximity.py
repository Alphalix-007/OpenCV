from cvzone.SerialModule import SerialObject
from time import sleep
import cv2
from pkg_resources import resource_filename
known_distance=76.2
known_width=14.3
#colour scheme
orange=(255, 102, 0)
red=(204, 0, 0)
yellow=(255, 255, 0)
grey=(102, 102, 153)
fonts=cv2.FONT_HERSHEY_SCRIPT_COMPLEX
face_detector=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

#focal length
def Focal_Length(measured_distance,real_width,width_in_rf_image):
    focal_length=(width_in_rf_image*measured_distance)/real_width
    return focal_length

#Proximity
def proximity(focal_length,real_face_width,face_width_in_frame):
    prox=(real_face_width*focal_length)/face_width_in_frame
    return prox

def face_data(image):
    #iniclializing the face width as 0
    face_width=0
    #converting BGR file to greyscale image
    gray_image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #face detection
    faces=face_detector.detectMultiScale(gray_image, 1.3, 5)
    #Rectangle for face detection
    for (x,y,h,w) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), red, 2)

        #face width
        face_width= w
    return face_width

ref_image= cv2.imread("Ref_image.jpg")
ref_image_face_width=face_data(ref_image)
# get the focal by calling "Focal_Length_Finder"
# face width in reference(pixels),
# Known_distance(centimeters),
# known_width(centimeters)

Focal_length_found= Focal_Length(known_distance, known_width, ref_image_face_width)
print("Focal_Length=", Focal_length_found)

#showing refrence image
#img = cv2.imread("test.jpeg", cv2.IMREAD_COLOR)
#cv2.imshow("image", img)

cap=cv2.VideoCapture(0)
count=0
#looping for countiniously taking the video
while True:
    ret,frame= cap.read()
    print(type(frame),"@")
    face_width_in_frame = face_data(frame)

    #checking for the face width must not be zero i.e. there is some face in the screen

    if face_width_in_frame != 0:
        Proximity_1=proximity(Focal_length_found, known_width, face_width_in_frame)
        print(Proximity_1,"%")
        cv2.line(frame, (30,30), (230,30), yellow, 32)
        cv2.line(frame, (30,30), (230,30), grey, 28)
        cv2.putText(frame, f"Distance: {round(Proximity_1,2)} CM", (30, 35), fonts, 0.6, orange, 2)
    cv2.imshow("frame",frame)
    #for closing the code
    cv2.waitKey(10)
    #for deallocation of the resources
    #cv2.destroyAllWindows()
    if Proximity_1<200:
        count+=1
    else:
        count=0
    if count==10:
        cv2.destroyAllWindows()
        
        ardunio= SerialObject("COM9")
        while True:
            ardunio.sendData([1])
            sleep(1)
            break


