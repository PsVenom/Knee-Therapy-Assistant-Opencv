#so the program follows the following logic
#we create a rep counter to keep track of the number of reps
#as soon as the left leg starts bending, we start the timer
#if the angle between the thigh and calves DECREASES or REMAINS SAME, we let the timer progress till 8 secs, after which the counter is incremented by 1
#if the angle increases significantly in a shorter time, we cancel the timer
#to avoid unexpected behaviour due to cropped-in frames, we need to take into consideration the average rate of change in angle
import cv2
import mediapipe as mp
import time
import numpy as np
import math
from tkinter import *
import tkinter as tk
from statistics import mean
cap = cv2.VideoCapture('KneeBendVideo.mp4') #for recording the video
counter = 0 #this will return the number of reps
coslist = [] #returns a list of all knee angles(will be explained later)
timeref = 0 #for measuring time
timelist = [] # a list for storing the time taken to complete each rep


#to proceed with the entirety of this code, we first need to figure out a way to find the angle between the right femur and right calf
#the simplest method is to use the cosine rule, which states that the cosine of two vectors is the dot-product of the said vectors, divided by the product of their magnitudes
#for that we need to find a way to calculate the dot product of two vectors, and the magnitude of a vector



def modulus(a): #to find the magnitude
 return math.sqrt(a[0]**2 + a[1]**2)
def multiply(a,b):  #for dot multiplication
    return a[0]*b[0]+a[1]*b[1]
def angle(a,b):  #to find the cosine using cosinge rule, and then using math.acos to find the subsequent angle
    try:
     return math.acos(multiply(a,b)/(modulus(a)*modulus(b)))*180/3.1415926
    except:
        return 0 # passing a random value incase of an exception

#now we'll focus on the main function itself. this function will be passed on to a tkinter window to make the program a little more interactive
def start_loop():
 global counter, coslist, timeref, timelist #calling all global variables
 mpPose = mp.solutions.pose
 pose = mpPose.Pose()   #for pose recognition. It will detect all our landmarks, using which we'll find the angle
 mpDraw = mp.solutions.drawing_utils #for drawing all landmarks
 #next we'll define lists to store co-ordinates of landmark 23,25, and 27
 list_23 = []
 list_25 = []
 list_27 = []
 timerState = False  # to initialise the timer

 while True:
  try:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB )  # 'results' store all the landmarks and their co-ordinates (for each frame)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark): #to access individual landmark
            h, w, c = img.shape
            if id == 23:
                list_23.append([int(lm.x * w), h-int(lm.y * h)]) #lm.x and lm.y are scaled to be < 1. Hence we multiply them by w and h to get the actual co-ordinates
                cv2.circle(img, (int(lm.x * w), int(lm.y * h)), 10, (0,255,0), cv2.FILLED )
            if id == 25:
                list_25.append([int(lm.x * w), h-int(lm.y * h)])
                cv2.circle(img, (int(lm.x * w), int(lm.y * h)), 10, (0, 255, 0), cv2.FILLED)
            if id == 27:
                list_27.append([int(lm.x * w), h-int(lm.y * h)])
                cv2.circle(img, (int(lm.x * w), int(lm.y * h)), 10, (0, 255, 0), cv2.FILLED)
        list_23a = np.array(list_23[-1])
        list_25a = np.array(list_25[-1])
        list_27a = np.array(list_27[-1])
        diff1 = list(np.subtract(list_23a,list_25a)) #creates a vector with endpoints list_23a and list_25a
        diff2 = list(np.subtract(list_27a, list_25a))#creates a vector with endpoints list_27a and list_25a
        coslist.append(angle(diff2,diff1))
    cv2.putText(img, f'Angle of knee: {coslist[-1]}',(450,50),cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 3) #displays the angle

    #now we need to time each rep to check if it's valid or not. Hence we make use of timerState and the time module to keep track of duration
    if timerState is False :
        try:
            theta1 = coslist[-7]
            if theta1< 140:
                timerState = True
                timeref = time.time()
        except:
            pass
    elif timerState is True:
        timea = time.time()-timeref
        cv2.putText(img, f'Time: {timea}', (0, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
        theta2 = coslist[-1]
        if timea<8.0 and theta2> 140:   #unsuccessful rep
            print(" HOLD YOUR REP")
            timerState = False
            timeref = time.time()
        elif timea>=8 and theta2>140:  #sucessful rep
            timerState = False
            counter+=1
            timelist.append(timea)
            timeref = time.time()
        else:
            pass
    cv2.putText(img, f'number of reps: {counter}', (500, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
  except:
      print("breakpoint reached")
      break

#now we define some tkinter functions to make the gui more interactive
def starting_screen():
    parent = tk.Tk()
    text1 = tk.Label(parent, text = "welcome to the Knee detection tracker! press the button to start your fitness journey")
    text1.pack()
    btn = tk.Button(parent, text = 'Start', command = start_loop)
    btn1 = tk.Button(parent, text = 'Exit', command = parent.destroy)
    btn.pack()
    btn1.pack(side = BOTTOM)
    parent.mainloop()
def result_screen(timel , c ): #will create a seperate window to display the users' stats
    page = tk.Tk()
    text1 = tk.Label(page, text = f"Awesome!!! You just finished your workout in {int((time.time()-timeref)/60)} minutes!!! \n Here are your stats : \n\n\n number of proper reps : {c} \n average rep time: {int(mean(timel))} seconds\n target reps: {c+1}  \n\n ALL THE BEST ON YOUR FITNESS JOURNEY! Time to smash those PRs!!!")
    text1.pack()
    page.mainloop()
#__main__
starting_screen()
result_screen(timel = timelist, c = counter)

#funny how the actual program is just two lines long :p