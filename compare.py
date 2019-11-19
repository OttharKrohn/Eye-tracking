# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 12:53:41 2019

@author: OA
"""

import csv

#Open the data files you are comparing
t1 = open('data.csv', 'r')
t2 = open('data/KlippMedBilder.csv', 'r')

#read through both
fileone = t1.readlines()
filetwo = t2.readlines()
t1.close()
t2.close()

#open file that can be written to if wanted
outFile = open('update.csv', 'w')

#Set counter and x/y differance
x = 0
xTot = 0
yTot = 0

#For-loop that checks if the lines in the files are the same
for i in fileone:
    if i != filetwo[x]:
        try:
#           Getting the coordinates from my csv-file
            block = fileone[x]
            coordinatesUnorderly = block.split(',')
            x1 = float(coordinatesUnorderly[1])
            y1 = float(coordinatesUnorderly[2])
      
#           Getting coordinates from eyeRecToo's csv-file
            block2 = filetwo[x]
            coordinatesUnorderly2 = block2.split(',')
            coord2= [0,0]
            coord2[0]= coordinatesUnorderly2[1]
            coord2[1]= coordinatesUnorderly2[2]
            x2 = float(coord2[0])
            y2 = float(coord2[1])
            
#            Checking the difference between my numbers and eyeRecToo's numbers, adding t together
            df= [x1-x2, y1-y2]
            diffx = str(df[0])
            diffy = str(df[1])
            xTot = xTot + df[0]
            yTot = yTot + df[1]
            row = [diffx, diffy]
            
#            If you want to write the differance of each point into a csv-file, uncomment:
#            outFile.write(row[0] + ' ')
#            outFile.write(row[1] + '\n')
            
#        Exception if my segmentation has given us 0,0 or -1, aka. error or shut eye.
        except:
            print('not comparing that line, due to error in segmenting/eye shut')
            
    x += 1

#Divide by x to get average offset.     
avgOffsetX = xTot/x
avgOffsetY = yTot/x
#Print if you want
print(avgOffsetX)
print(avgOffsetY)

outFile.close()