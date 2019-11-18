# Eye-tracking


Intro:

This is my eyetracking software.
Hope it is not to difficult to use :)
The following is a short guide on how to start, and use it. Along with some important information.

1. Installation
2. Start
3. Use
4. Important info
5. Further descriptions

------------------------------------------
1. INSTALLATION:

You will need a series of libraries, which I
will explain further.

Libraries:

Versions I used:
Python 3.7.3
Pip 19.0.3
NumPy 1.16.4
tkinter 8.6
openCV 4.1.0


Installation of the libraries:

Python: 
Downloading and installing python is not 
the most difficult step. There are many ways to do this.
I installed python through anaconda. 
But if you google install python, you can download and run
wichever installation you want.
Anaconda comes with many libraries and programs.
Most importantly it includes python, pip, and numpy.

pip:
Using the console you can write 'python get-pip.py'
This is used to install other libraries later.

Numpy:
Using console again. Write 'pip install numpy'

openCV:
Using their website 'opencv.org', you can easily chose 
and download the correct version for your OS.
Or: use console again 'pip install opencv-python'

tkinter, csv and os:
I also use these libraries. 
They are inculded in the python package.
The import lines should therefore be enough.

2. START:

Create a project in your preferred IDE, and add all the .py files.
Create an empty folder called "frames"
Open the window.py file, and run

3. USE:

Select a video using the "select video"-button, wait for the console to give feedback.
Segment or draw trajectory, to get your wanted file. 
Save your wanted file.

4. Important info:

The videoreader may delete the "frames"-folder and not create a new one. 
Simply create a new folder and try again.
It is important to know that the data.csv-file will be written in the buttom of, 
if you preform more than one segmentation. To avid this, it is smarter to move and rename the file after segmentation.
You will then have data from only one segmentation in the file.
The traj.jpg is the drawn trajectory. This is overwritten if you segment again. Move and save this one between segmentations.

5. Descriptions:

There are three main classes, I will briefly explain these: Window.py, videoReader.py, eyePicHandler.py.
The window-class is the "main" class. It starts everything, and opens up the GUI. It is connected to the other classes.
The videoreader-class reads thorugh a selected video, and saves each frame as a picture in the "frames"-folder.
The eyePicHandler-class is the core of the program. This is where the segmentation algorithm is. 
