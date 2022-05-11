#!/usr/bin/env python
# -*- encoding: utf-8

'''A bot that automatically clicks on critical spots if you hold down the specified button.
You have to unlock them first for the bot to work.
https://syns.studio/more-ore/'''

import time
import numpy as np
import cv2 as cv
import mss
from keyboard import read_key
import mouse
from selenium import webdriver

def main():
    xscreen, yscreen, offset, window = get_ore_loc()
    autoclicker(xscreen, yscreen, offset, window)

def get_ore_loc():
    driver = webdriver.Chrome(executable_path="D:\Program Files\Chromedriver\chromedriver.exe")
    driver.implicitly_wait(0.5)
    driver.maximize_window()
    driver.get("https://syns.studio/more-ore/")
    #identify element
    l= driver.find_element_by_xpath("//*[@class='ore-wrapper']")
    #get x, y coordinates
    loc = l.location
    #get height, width
    s = l.size
    driver.close()
    offset = 25
    xscreen = loc['x']-offset
    yscreen = loc['y']+(s['height']//2)-offset
    window = {"top": yscreen, "left": xscreen, "width": s['width']+2*offset, "height": s['height']+2*offset}
    return xscreen, yscreen, offset, window

def autoclicker(xscreen, yscreen, offset, window):
    while True:
        if read_key() == "ü": # set the key to start the program.
            tstart = time.time()
            img = np.array(mss.mss().grab(window))
            colourimg = img[:, :, ::-1].copy() # Convert RGB to BGR
            colourimg = cv.medianBlur(colourimg,5)
            greyimg = cv.cvtColor(colourimg,cv.COLOR_BGR2GRAY) # Convert BGR to grey

            circles = cv.HoughCircles(greyimg,cv.HOUGH_GRADIENT,1,20,
                                param1=20,param2=14,minRadius=10,maxRadius=13)

            try:
                circles = np.uint16(np.around(circles))
                '''
                for i in circles[0,:]:
                    # draw the outer circle
                    cv.circle(colourimg,(i[0],i[1]),i[2],(0,255,0),2)
                    # draw the center of the circle
                    cv.circle(colourimg,(i[0],i[1]),2,(0,0,255),3)
                cv.imshow('detected circles',colourimg)
                cv.waitKey(0)
                '''
                for i in circles[0,:]:
                    mouse.move(xscreen+i[0], yscreen+i[1])
                    mouse.click()
            except Exception:
                # cv.imshow('unidentifyable screenshot',colourimg)
                # cv.waitKey(0)
                pass

            mouse.move(xscreen-2*offset, yscreen-2*offset)
            # print(time.time() - tstart)
            time.sleep(0.36)

        # exit()

if __name__ == '__main__':
    main()
