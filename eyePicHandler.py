# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 12:59:43 2019

@author: OA
"""
#EyeSegmenter class

import cv2
import numpy as np
import tkinter
from tkinter import filedialog

class eyePicHandler:
        
        #constructor
    def __init__(self, pic):
        self.pic = pic
        
        #show default picture
    def showDefaultFrame(self, pic):
        imgC = cv2.imread(self.pic, 1)
        cv2.imshow(imgC)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        #Segmentation method
    def segment(self):
        
        # Load a color image in grayscale(0) regular(1) or negative(-1)
        img = cv2.imread(self.pic,0)
        cv2.imwrite('greyscale.jpg', img)
        img2 = cv2.imread(self.pic, 1)

       
        strict = (20,20,20)
        medium = (30,30,30)
        loose=(51,51,51)
        
        black = (0, 0, 0)
        dark = strict
        #Defines what is presumably the colors of the pupil from completely black, to quite dark
        #It is possible to adjust the dark parameter, and may be necessary depending on the video
        #Making it less strict will make the alghorithm more robust, but less accurate
        

        #using openCV
        eye = cv2.cvtColor( img, cv2.COLOR_BGR2RGB)

        #make a mask that implements the colors of the pupil, often cale a threshold
        pupil = cv2.inRange(eye, black, dark)
        
        #save and read the picture, nice to be able to see this step in a pic
        cv2.imwrite('Pupil.jpg',pupil)
        pupil1 = cv2.imread('Pupil.jpg',1)

        #MORPHOLOGY        
        #elliptical kernel used to morph the pupil with dilating and closing methods
        area = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7) )
        #area = np.ones((9,9),np.uint8)  
        dilation = cv2.dilate(pupil1, area,iterations = 1)
        closed = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, area)
        cv2.imwrite('segmentation.jpg', closed)
        
        fittedEllipse = self.fitEllipsen()
        centre = (0,0)
        
        try:
            centre = self.newCentre(fittedEllipse) 
#            print(centre)
        except:
            print('no centre, move on')
            
        return centre;
       
#    Method for finding the largest contour(white spot) in the segmentation
    def largestContour(self):
        image = cv2.imread('segmentation.jpg', 0)
        ret, thresh = cv2.threshold(image, 127,255,0)

        contours,hierarchy = cv2.findContours(thresh, 1, 2)
#       cnt = contours[0]
        if not contours:
            print('no contours found')
            return 0
        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        cnt=contours[max_index]
        
        return cnt
    
#    Method for drawing an ellipse around the largest contour
    def fitEllipsen(self):
        image = cv2.imread('segmentation.jpg', 0)
        ret, thresh = cv2.threshold(image, 127,255,0)
        
        canny_output = cv2.Canny(image, 127, 255)
        img = cv2.imread(self.pic, 0)

        contours,hierarchy = cv2.findContours(thresh, 1, 2)
#       cnt = contours[0]
        if not contours:
            print('No contours found, eye may be closed')
#            print (0)
            return 0
        
        minEllipse = [None]*len(contours)
        
        try:  
            for i, c in enumerate(contours):
                minEllipse[i] = cv2.fitEllipse(c)
        except:
            print('cannot draw ellipse with this')
            
        drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)

        color = (255,255,255)
        largest = self.largestContour()
        ellipse = cv2.fitEllipse(largest)
        cv2.ellipse(drawing, ellipse, color, -1 )
        
#        Find the centre of the ellipse
        try:
            centreNew = self.newCentre(drawing)
            a = centreNew[0]
            b = centreNew[1]
            x = int(a)
            y = int(b)
            centreInt = (x, y)
            red = (0, 0, 255)
            axesLength = (2, 2) 
            angle = 0
            startangle = 0
            end = 0
             
            cv2.ellipse(drawing, centreInt, axesLength, angle, startangle, end, red, 2)
            cv2.imwrite('fittedEllipse.jpg', drawing)
        except:
            print('no centre, move on')
     
        
#        Draw a red dot in the centre of the ellipse,save, and return it all
       
        return drawing
    
#########  Method for finding largest label/contour/moment     #######

    def largest(self):
        image = cv2.imread('segmentation.jpg', cv2.IMREAD_UNCHANGED)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        
        ret, labels = cv2.connectedComponents(binary)
        
        #look through the different white dots "labels" by unncommenting the openCV-lines
        for label in range(ret):
            mask = np.array(labels, dtype=np.uint8)
            mask[labels == label] = 255
        if labels.any():
            defi = 0
        else: 
            #error:error
            return (0,0)

        connectivity = 4
        #Collects stats from connectedComponents
        data = cv2.connectedComponentsWithStats(binary, connectivity, cv2.CV_32S)
        #saves a set of statistics about the components, stored in the forth cell
        stats = data[2] 

        #check the size of the different connected components, the biggest will (most likely) always be the pupil
        largestSize = -1
        largestLabel = -1
        
        for label in range(ret):
    
            size = stats[label, cv2.CC_STAT_AREA]
            if(largestSize < size): 
                largestSize = size
                largestLabel = label
                
        return largestLabel        
                


#    Centre method for calculating centre of the pupil     
    def newCentre(self, drawing):
        gray = cv2.cvtColor(drawing, cv2.COLOR_BGR2GRAY)
        binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        ret, labels = cv2.connectedComponents(binary)
        
        #look through the different white dots "labels" by unncommenting the openCV-lines
        for label in range(ret):
            mask = np.array(labels, dtype=np.uint8)
            mask[labels == label] = 255
            #cv2.imshow('component',mask)
            #cv2.waitKey(0)
            
        
        #cv2.destroyAllWindows() 
        connectivity = 4
        #Collects stats from connectedComponents
        data = cv2.connectedComponentsWithStats(binary, connectivity, cv2.CV_32S)
        #centroids, aka centre of the different components, is stored in the forth cell
        centres = data[3]
        largestLabel = self.largest() 
#       print(largestLabel)
        centreOfPupil = centres[largestLabel +1]
        
        return centreOfPupil
    
