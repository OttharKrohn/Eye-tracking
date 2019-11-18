# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 12:57:09 2019

@author: OA
"""
import videoReader
import eyePicHandler
import cv2
import numpy as np
import tkinter
from tkinter import filedialog
import csv
import os
import shutil



#   GUI class
class Window(tkinter.Frame):
    
    def __init__(self, master=None):
       tkinter.Frame.__init__(self, master)
       self.master = master
       self.init_window()
       
    def init_window(self):
        
        self.master.title("E-Motion")
        
        self.pack(fill=tkinter.BOTH, expand=1)
        
#       Drawingbutton
        drawButton = tkinter.Button(self, text = "Draw Trajectory", width = 12, height = 1, command = self.drawTrajectory)
        drawButton.place(x=0, y=65)

#        Filechooser button       
        chooseButton = tkinter.Button(self, text = "Select video", width = 12, height = 1, command = self.video)
        chooseButton.place(x=0, y=5)
        
#        Segmentation button
        segButton = tkinter.Button(self, text = "Segment video", width = 12, height = 1, command = self.segment)
        segButton.place(x=0, y=35)
    
#       Add textbox called tutorial wich describes what and how
        tutorial = tkinter.Text(root, height=10, width=42, bg='lightgrey')
        text = """1. Select video, and wait for feedback 
2. Segment or draw trajectory to get your 
wanted file. 
3. Save data.csv or traj.jpg in separate 
folder before proceeding"""
        tutorial.insert('1.0',text)
        tutorial.place(x=100, y=5)
        
#        closing method
    def client_exit(self):
        root.destroy()
        
#        video selection method, calls upon videoReader class. Saves every frame as a jpg file in /frames
    def video(self):
        root.filename =  tkinter.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("mp4 files", "*.mp4"),("jpeg files","*.jpg"),("all files","*.*") ))
        videoPath = root.filename
        v1 = videoReader.videoReader(videoPath)
        v1.read()
        
#        Prints the videos location
#        print( videoPath)
        
#        segmentation method, calls upon eyePicReader class for every picture in /frames. 
    def segment(self):
        count = 0

        directory = 'frames/'
 
#        Figures out how many pictures are in the /frames folder, so we can use that later in the for-loop
        number_of_files = len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])
        max = number_of_files
#        print(max)
 
    
#        for-loop that iterates through the pictures in /frames, creates an eyePicHandler object with it, and segments it
#        Gives us the coordinates of the centre of the pupil
#        Writes the frame number in collumn 1 and coordinates in collumn 2, in a csv file data.csv
#        writes 0 as the centre coordinates if the eye is shut, or -1 if we have an error
        count = 0
        for var in range(1,max):
            temp = eyePicHandler.eyePicHandler('frames/frame%d.jpg' % count)
            try:
                data = temp.segment()
                print(data)
                x = float(data[0])
                y = float(data[1])
                row = [count, x, y]
            except:
                row = [count, -1]
                print('cannot segment this one')
            with open('data.csv', 'a', newline='') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow(row)
                writeFile.close()
            count += 1
            if cv2.waitKey(10) == 27:                     # exit if Escape is hit
                break
            
#        some feedback that we are done
        print('done segmenting')
            
        
#       method for drawing trajectory of the pupil, also uses the segmentation, and eyePicHandler class
#       in the same way as the segment method, but uses the data(centre coordinates), to draw
#       lines between the pupils position  
    def drawTrajectory(self):
        traj = np.zeros(shape=[240, 360, 3], dtype=np.uint8)
        count = 0
        import os
        directory = 'frames/'
        cv2.imshow('result', traj)
        cv2.waitKey(0)

#        Figures out how many pictures are in the /frames folder, so we can use that later in the for-loop
        number_of_files = len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])
        max = number_of_files
#        print(max)
        
        f0 = eyePicHandler.eyePicHandler('frames/frame0.jpg')
        starter = f0.segment()
        startia= [0,0]
        startia[0] = int(starter[0])
        startia[1] = int(starter[1])
        
        count = 1
        start = [startia[0],startia[1]]
        endi = [0,0]
        starti = [0,0]
        for var in range(1,max):
            temp = eyePicHandler.eyePicHandler('frames/frame%d.jpg' % count)
            
            try:
                end = temp.segment()
                print(end)
            except:
                print('big opsie')
            if start[0] > 0:
                try:
#                    print('go')    
            
                    endi[0] = int(end[0])
                    endi[1] = int(end[1])
                    if endi[0] > 0 :
                        
                        starti[0] = int(start[0])
                        starti[1] = int(start[1])
                        startPoint = (starti[0], starti[1])
                        endPoint = (endi[0], endi[1])
                        thickness = 1
                        red = (0,0,255)
                        green = (0,255,0)
                        axes = (1,1)
                
#                        draws a dot in every point the pupil is, commented out, may not be necessary
                        cv2.ellipse(traj, startPoint, axes, 0, 0, 360, red, 1)
                        
#                        Draws the line between the pupil positions
                        cv2.line(traj, startPoint, endPoint, green, thickness)
                        frame = cv2.imread('frames/frame%d.jpg' % count)
                        ellipse = cv2.imread('fittedEllipse.jpg')
                        
#                        two versions of stiching together the frames into one, i chose hstack
                        numpy_horizontal = np.hstack((frame, ellipse, traj))
#                        numpy_horizontal_concat = np.concatenate((frame, ellipse, traj), axis=1)
                        cv2.imshow('Input, segmentation, output', numpy_horizontal)
                        cv2.waitKey(16)
                except:
                    print('not drawing')
            if end[0] > 0:
                start = end
            if cv2.waitKey(10) == 27:                     # exit if Escape is hit
                break
        
            
            
            count += 1
#        save the trajectory-picture, and we are done
        cv2.ellipse(traj, (endi[0], endi[1]), axes, 0, 0, 360, green, 1)
        cv2.imwrite('traj.jpg', traj)                
        print ('done drawing')    
        cv2.destroyAllWindows()            
            
root = tkinter.Tk()

#size i guess
root.geometry("450x150")

#creates an instance
app = Window(root)

#mainloop
root.mainloop()

