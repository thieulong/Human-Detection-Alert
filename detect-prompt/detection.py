import cv2
import mediapipe as mp
import pyttsx3
import threading
import time
import os

engine = pyttsx3.init()
engine.setProperty('rate', 150)

def person_detected():

    engine.say('Hello there! The system has detected that you have arrived at the time my creator is away or he is in his deep sleep. If you have anything to say, raise your right hand and a note will pop up on the screen for you to write your message. Raise your left hand if you want me to repeat. Thank you!')
    engine.runAndWait()

def right_raised():
    engine.say('You have raised your right hand! A note editor will pop up right after, please write anything you want to say to my creator. After that you leave the message there and I will handle the rest. Have a good day and many thanks for your visit!')
    engine.runAndWait()

def left_raised():
    engine.say('Ok! The system has detected that you have arrived at the time my creator is away or he is in his deep sleep. If you have anything to say, raise your right hand and a note will pop up on the screen for you to write your message. Thank you!')
    engine.runAndWait()

detected_thread = threading.Thread(target=person_detected)
confirm_thread = threading.Thread(target=right_raised)
repeat_thread = threading.Thread(target=left_raised)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
        success, image = cap.read()
        image_height, image_width, _ = image.shape

        if not success:
            print("Ignoring empty camera frame.")
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            
            x_cordinate = list()
            y_cordinate = list()

            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                x_cordinate.append(cx)
                y_cordinate.append(cy)
                
            cv2.rectangle(img= image,
                        pt1= (min(x_cordinate), max(y_cordinate)),
                        pt2 = (max(x_cordinate), min(y_cordinate)-20),
                        color= (0,0,255),
                        thickness= 2)

            cv2.imwrite('detect.png', image)

            right_side = [results.pose_landmarks.landmark[28].y * image_height,
                        results.pose_landmarks.landmark[26].y * image_height,
                        results.pose_landmarks.landmark[24].y * image_height,
                        results.pose_landmarks.landmark[12].y * image_height,
                        results.pose_landmarks.landmark[0].y * image_height,
                        results.pose_landmarks.landmark[16].y * image_height
                        ]

            left_side = [results.pose_landmarks.landmark[27].y * image_height,
                        results.pose_landmarks.landmark[25].y * image_height,
                        results.pose_landmarks.landmark[23].y * image_height,
                        results.pose_landmarks.landmark[11].y * image_height,
                        results.pose_landmarks.landmark[0].y * image_height,
                        results.pose_landmarks.landmark[15].y * image_height]

            right_up = all(i > j for i, j in zip(right_side, right_side[1:]))
            left_up = all(i > j for i, j in zip(left_side, left_side[1:]))

            if not right_up and not left_up:
                
                try:
                    detected_thread.start()
                    detected_thread.join()
                except RuntimeError:
                    continue

            if right_up and not left_up:
                
                cv2.rectangle(img= image,
                pt1= (min(x_cordinate), max(y_cordinate)),
                pt2 = (max(x_cordinate), min(y_cordinate)-20),
                color= (0,255,0),
                thickness= 2)

                cv2.imwrite('right_raise.png', image)

                confirm_thread.start()
                confirm_thread.join()

                os.system("gedit note.txt")

                break

            if left_up and not right_up:
                cv2.rectangle(img= image,
                pt1= (min(x_cordinate), max(y_cordinate)),
                pt2 = (max(x_cordinate), min(y_cordinate)-20),
                color= (255,0,0),
                thickness= 2)

                cv2.imwrite('left_raise.png', image)

                try:       
                    repeat_thread.start()
                    repeat_thread.join()
                except RuntimeError:
                    continue

            x_cordinate.clear()
            y_cordinate.clear()

        cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))

        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()