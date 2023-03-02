from picamera import PiCamera
from datetime import datetime
import numpy as np
import cv2
from cv2 import (imread, absdiff, cvtColor)
import traceback
from time import sleep
import imutils

class Camera(PiCamera):
    def __init__(self):
        self.collision_path = '/home/pi/ROAM_calls/images/collision_shots/'
        self.camera = PiCamera()
        self.comparison_dates = []
        self.ready_to_compare = False

    def takeCollisionPhoto(self):
        try:
            time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
            name = f'collision_{time}.jpg'
            self.camera.capture(''.join([self.collision_path, name]))
            print(f'\nCollision image saved as {self.collision_path}/{name}')
            sleep(2)
        except:
            print(f'Camera.takePhoto() Error:\n{traceback.format_exc()}')
    

    def takeComparisionShot(self):
        try:
            
            if len(self.comparison_dates) == 2:
                self.comparison_dates = []
                self.ready_to_compare = False

            name = f"cmp_{len(self.comparison_dates)}.jpg"
            path = ''.join(['/home/pi/ROAM_calls/images/cmp/', name])
            self.comparison_dates.append(datetime.now())
            self.camera.capture(path)
            sleep(2)
            if len(self.comparison_dates) == 2:
                self.ready_to_compare = True

        except:
            print(f'Camera.takeComparisionShot() Error:\n{traceback.format_exc()}')
    
    def compareShots(self):
        if self.ready_to_compare:
            cmp_0_path = '/home/pi/ROAM_calls/images/cmp/cmp_0.jpg'
            cmp_1_path = '/home/pi/ROAM_calls/images/cmp/cmp_1.jpg'
            cmp_0 = imread(cmp_0_path)
            cmp_1 = imread(cmp_1_path)
            cmp_0 = imutils.resize(cmp_0, width=500)
            cmp_1 = imutils.resize(cmp_1, width=500)
            
            gray_cmp_0 = cvtColor(cmp_0, cv2.COLOR_BGR2GRAY)
            gray_cmp_0 = cv2.GaussianBlur(gray_cmp_0, (21, 21), 0)
            gray_cmp_1 = cvtColor(cmp_1, cv2.COLOR_BGR2GRAY)
            gray_cmp_1 = cv2.GaussianBlur(gray_cmp_1, (21, 21), 0)

            frame_delta = absdiff(gray_cmp_0 , gray_cmp_1)
            thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)
            for c in contours:
                print(cv2.contourArea(c))

    