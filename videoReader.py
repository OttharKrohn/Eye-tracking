# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 12:58:30 2019

@author: OA
"""
import os
import cv2
import numpy as np
import tkinter
from tkinter import filedialog
import shutil


#videoReader class
class videoReader:
    
#    constructor
    def __init__(self, video):
        self.video = video
    
#    Reader: Takes a video as input. Gives us all the frames as jpg-files in the folder: /frames    
    def read (self):
        foldername = 'frames'
        
        try: 
            shutil.rmtree(foldername)
            os.mkdir(foldername)
            print('reading video...')
        except:
            print('whoopsie, create a "frames"-folder and try again')
            
        eyeVideo = cv2.VideoCapture(self.video)
        success,image = eyeVideo.read()
        count = 0
        success = True
        while success:
            success,image = eyeVideo.read()
            cv2.imwrite("frames/frame%d.jpg" % count, image)     # save frame as JPEG file
            if cv2.waitKey(10) == 27:                     # exit if Escape is hit
                break
            count += 1
        print('done reading the video')
