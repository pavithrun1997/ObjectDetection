#!/usr/bin/env python 
"""
This code will help in the detection of a Yellow ball and will draw a circle around the detected yellow ball.
All the detection in this case is done based on simple color filtering technique where the rgb image obtained 
is convereted to a HSV image and by passing the Hue values of yellow color which we already know we put a mask
on the obtained frame and perform contour detection of the image and thus obtain the detection of images. By 
changing the Hue filter limit passed we will be able to obtain object detection of different colors.

"""

import cv2                             
import numpy as np
from sensor_msgs.msg import Image


def color_filter(image):
    yellowUpper = (60,255,255)   # Filter levels for Yellow could be changed for other objects
    yellowLower = (30,150,100)
    mask = cv2.inRange(image,yellowLower,yellowUpper)
    return mask

def contour_finder(image):
    contour,heirarchy = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    return contour

def draw_contours(binary_image,rgb_image,contours):
    black_image = np.zeros([binary_image.shape[0], binary_image.shape[1],3],'uint8')
    
    for c in contours:
        area = cv2.contourArea(c)
        perimeter= cv2.arcLength(c, True)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if (area>100):
            cv2.drawContours(rgb_image, [c], -1, (250,0,0), 1)
            cv2.drawContours(black_image, [c], -1, (150,250,150), 1)
            cx, cy = get_contour_center(c)
            cv2.circle(rgb_image, (cx,cy),(int)(radius),(0,0,255),1)
            cv2.circle(black_image, (cx,cy),(int)(radius),(0,0,255),1)
            #cv2.circle(black_image, (cx,cy),2,(150,150,255),-1)
            print ("Area: {}, Perimeter: {}".format(area, perimeter))
    print ("number of contours: {}".format(len(contours)))
    cv2.imshow("Yellow Ball Detection",rgb_image)
    cv2.imshow("Black Image Contours",black_image)

def get_contour_center(contour):
    M = cv2.moments(contour)                ## The moments function help us to find the center of the detected contours
    cx=-1                                   ## thus enabling to draw a circel around the detected objects,
    cy=-1
    if (M['m00']!=0):
        cx= int(M['m10']/M['m00'])
        cy= int(M['m01']/M['m00'])
    return cx, cy

    

def detect_ball(frame):
    hsv_image = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    binary_image = color_filter(hsv_image)
    contours_img = contour_finder(binary_image)
    contours_on_image = draw_contours(binary_image,frame,contours_img)
    
    


def main():
    video_capture = cv2.VideoCapture(0)                                ## This code could be run on live video
    #video_capture = cv2.VideoCapture('video/tennis-ball-video.mp4')     ## which is connected to the device on which
    while(True):                                                        ## this script is run just comment/uncomment the necessary line
        ret, frame = video_capture.read()
        #cv2.imshow("H",frame)
        detect_ball(frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()



cv2.waitKey(0)
cv2.destroyAllWindows()

"""
Press q and esc to exit from the code 

"""
