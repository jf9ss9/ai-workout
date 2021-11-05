# ai-workout
This repository was created for my final year project. This is a pose detection and AI based personal trainer application.

Abstract:

Workout at home gathered popularity in the last years as more and more mobile applications were developed which helped people to work
out almost everywhere. With the Covid-19 virus, this trend became more popular since most of the gyms were closed so it's clear that this
topic should be in focus. These applications helped their clients by showing them animations of the different exercises and had the possibility
of monitoring the progress by manually adding the number of repetitions/ sets. A person can choose the type of exercise then press a start
button which started a timer for the given exercise. This approach of workout has almost no control over the correctness of the exercise, it
relies just on the animation shown at the beginning which can be harmful. Furthermore, it's inconvenient for the user to manually count it's
repetitions/ sets etc.
My software would improve mainly in these two areas. I will create a software based on computer vision and artificial intelligence which can
detect the user's pose from a live camera feed (like smartphone camera or webcam) and can give feedback of the correctness of the
exercise and also count the number of repetitions. With this approach the user does not rely only just on some animations (which is
necessary) but gets real time feedback just as with a personal trainer.

The application was developed purely in Python and the Kivy gui framework. It uses mediapipe's pose module to determine the human pose in real time
and opencv to process the camera feed. A user can log in or register securely since I use bcrypt encryption with a salt to store
the passwords. After the login the user can choose whether to exercise or check his/ her faults. There are many exercises to choose from
and after a short animation of the workout type, the user can start to exercise and see himself in real time with the estimated pose
shown on the camera feed. Repetitions are calculated by the software but only if they are made correctly. Faults are detected
automatically and saved mainly as a (screenshot, description) pair in an MSSQL database among with workout and user data. 
Faults can be checked after the workout as a screenshot of the exact frame when the fault was made and the fault description.
I used SqlAlchemy's ORM for the connection with the database, and I have a custom logger so debugging is a lot easier.
Check out the source code to see my coding/ designing skills and have a deeper sight of the application.

Tech stack I used so far: Python, MSSQL, SqlAlchemy, Mediapipe, OpenCV, Kivy, logging and more..

![giphy](https://user-images.githubusercontent.com/43384813/140485156-52e516f9-7717-4b90-9ff7-d0647a88cd74.gif)
![giphy (1)](https://user-images.githubusercontent.com/43384813/140485798-2719f8c5-6dde-47d8-87d0-c2e0fea58e3f.gif)
