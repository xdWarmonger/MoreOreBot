#!/usr/bin/env python
# -*- encoding: utf-8

import time
import numpy as np
import cv2 as cv
import mss
import mouse
import win32gui
import webbrowser
from keyboard import read_key, is_pressed
from tkinter import *
from configparser import ConfigParser
from threading import Thread

def main():
    handle = win32gui.GetForegroundWindow()
    wrect = win32gui.GetWindowRect(handle)   # posx, posy, width + posx, height + posy
    critclicker(wrect)

def infobox():
    guictrl = Tk()
    app = Window(guictrl)
    guictrl.wm_title("MoreOreBot autoclicker settings")
    guictrl.geometry("350x100")
    guictrl.mainloop()
class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)        
        self.master = master
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = Menu(menu, tearoff=False)
        menu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="save", command=self.savecontrols)
        fileMenu.add_command(label="load", command=self.loadcontrols)

        helpMenu = Menu(menu, tearoff=False)
        menu.add_cascade(label="Help", menu=helpMenu)
        helpMenu.add_command(label="GitHub", command=self.openGithub)
        helpMenu.add_command(label="More Ore Website", command=self.openMoreOreWebsite)
        
        focuslbl = Label(self, text='Focus: ', borderwidth=1 ).grid(row=0,column=0)
        critlbl = Label(self, text='Crits (Hold down): ', borderwidth=1 ).grid(row=1,column=0)

        focusbtn = Button(self, text=focuskey, borderwidth=1 ).grid(row=0,column=1, sticky="news")
        critbtn = Button(self, text=critkey, borderwidth=1 ).grid(row=1,column=1, sticky="news")

        self.pack(fill=BOTH, expand=1)

    def openGithub(self):
        webbrowser.open_new(r"https://github.com/xdWarmonger/MoreOreBot")

    def openMoreOreWebsite(self):
        webbrowser.open_new(r"https://syns.studio/more-ore/")

    def savecontrols(self):
        config = ConfigParser()
        config.add_section('main')
        config.set('main', 'focus', str(focuskey))
        config.set('main', 'crit', str(critkey))
        with open('config.ini', 'w', encoding='utf-8') as f:
            config.write(f)
    
    def loadcontrols(self):
        config = ConfigParser()
        config.read('config.ini', encoding='utf-8')
        focuskey = config.get('main', 'focus')
        critkey = config.get('main', 'crit')

def critclicker(wrect):
    middlex, middley = wrect[0] + (wrect[2] - wrect[0] - 250)/2, wrect[1] + (wrect[3] - wrect[1])/2
    posx, posy = middlex - 225, middley - 175
    window = {"top": int(posy), "left": int(posx), "width": 400, "height": 400}

    while True:
        if read_key() == critkey: # critkey from the config file
            img = np.array(mss.mss().grab(window))
            colourimg = img[:, :, ::-1].copy() # Convert RGB to BGR
            colourimg = cv.medianBlur(colourimg,3)
            greyimg = cv.cvtColor(colourimg,cv.COLOR_BGR2GRAY) # Convert BGR to grey

            circles = cv.HoughCircles(greyimg,cv.HOUGH_GRADIENT,1,20,
                                param1=100,param2=25,minRadius=8,maxRadius=20)

            try:
                circles = np.uint16(np.around(circles))
                for i in circles[0,:]:
                    mouse.move(posx+i[0], posy+i[1])
                    mouse.click()
            except Exception:
                pass

            mouse.move(posx, posy)
            time.sleep(0.36)

        if read_key() == focuskey: # focuskey from the config file
            img = np.array(mss.mss().grab(window))
            colourimg = img[:, :, ::-1].copy() # Convert RGB to BGR
            colourimg = cv.medianBlur(colourimg,3)
            greyimg = cv.cvtColor(colourimg,cv.COLOR_BGR2GRAY) # Convert BGR to grey

            circles = cv.HoughCircles(greyimg,cv.HOUGH_GRADIENT,1,20,
                                param1=100,param2=25,minRadius=8,maxRadius=20)

            try:
                circles = np.uint16(np.around(circles))
                 
                '''for i in circles[0,:]:
                    # draw the outer circle
                    cv.circle(colourimg,(i[0],i[1]),i[2],(0,255,0),2)
                    # draw the center of the circle
                    cv.circle(colourimg,(i[0],i[1]),2,(0,0,255),3)
                cv.imshow('detected circles',colourimg)
                cv.waitKey(0)'''
                
                for i in circles[0,:]:
                    mouse.move(posx+i[0], posy+i[1])
                    # mouse.click()
            except Exception:
                '''cv.imshow('unidentifyable screenshot',colourimg)
                cv.waitKey(0)'''
                pass

            time.sleep(0.36)

if __name__ == '__main__':
    config = ConfigParser()
    config.read('config.ini', encoding='utf-8')
    focuskey = config.get('main', 'focus')
    critkey = config.get('main', 'crit')
    Thread(target=infobox).start()
    main()
