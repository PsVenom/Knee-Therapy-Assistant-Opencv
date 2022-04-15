# Knee-Therapy-Assistant-Opencv
A project utilising openCV, mediapipe and tkinter to create a simple fitness assistant for people currently going through physiotherapy for Traumatic Arthritis

Overview:
The program counts the number of succesful reps done by the user, and then returns some useful stats that help the user with progress tracking
But there are some ground rules that need to be set up
A 'rep' only counts if:
  The knee reaches an angle < 140 degrees
  stays in that position for 8 seconds or more
  the knee is extended back to an angle> 140 degrees
  
With this in mind, we have developed the following algorithm
How it works:
We use mediapipe to create a pose object, which finds 32 unique points, or 'landmarks' on the human body. These landmarks are then used to create vectors to represent the femur and the calf muscle.
We use these vectors to find the angle of thr right knee using the cosine formula:

![image](https://user-images.githubusercontent.com/99831413/163581437-43b55ee3-b38e-44da-905c-5bfaaa0f4533.png)

where a and b are femur and calf vectors
Now that we have our angle, we can use it to find out if our rep was successful or not.
Once the angle reduces to <140 degrees, we activate a timer to keep track of the duration of the rep.
Rest of the program works in accordance to the above definition of a rep

I've also used tkinter to make the program more organised 
![Screenshot (20)](https://user-images.githubusercontent.com/99831413/163581893-f4ce1451-b019-4789-be3e-392447ab7c64.png)
the opening screen

![Screenshot (21)](https://user-images.githubusercontent.com/99831413/163582468-75e0a9ac-59a5-4c04-90fa-3e2a3f1d69f0.png)
output screen, when angle> 140

![Screenshot (22)](https://user-images.githubusercontent.com/99831413/163582603-bb4a45f9-af24-49f0-b7e4-4987b724699e.png)
output screen, with angle<140 (notice that the timer has been activated)
