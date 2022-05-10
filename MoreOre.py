#!/usr/bin/env python
# -*- encoding: utf-8

'''A bot that automatically clicks on critical spots if you hold down the specified button.
You have to unlock them first for the bot to work.
https://syns.studio/more-ore/'''

import numpy as np
import cv2 as cv
import pyscreenshot as ImageGrab
from keyboard import read_key
from pyautogui import moveTo, click

while True:
    if read_key() == "ü": # set the key to start the program.
        im=ImageGrab.grab(bbox=(950,550,1300,900))
        im.save('tmp.png')

        img = cv.imread('tmp.png',0)
        img = cv.medianBlur(img,5)
        cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
        circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,20,
                            param1=20,param2=11,minRadius=10,maxRadius=13)
        try:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                # draw the outer circle
                cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
            # cv.imshow('detected circles',cimg)
            # cv.waitKey(0)
            for i in circles[0,:]:
                moveTo(950+i[0], 550+i[1])
                click()
        except Exception:
            pass
        moveTo(950, 550)
