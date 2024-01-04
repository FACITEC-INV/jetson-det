# MIT License
# Copyright (c) 2019-2022 JetsonHacks

# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2
import time
from jetson_utils import videoSource, cudaFromNumpy
from jetson_inference import detectNet


def detect(display=False):
    window_title = "CSI Detect"

    net = detectNet("trafficcamnet", threshold=0.3)
    net.SetTrackingEnabled(True)
    net.SetTrackingParams(minFrames=3, dropFrames=15, overlapThreshold=0.5)

    video_capture = cv2.VideoCapture("/home/jetson/Downloads/mapy.mp4")

    # used to record the time when we processed last frame 
    prev_frame_time = 0
    
    # used to record the time at which we processed current frame 
    new_frame_time = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    if video_capture.isOpened():
        try:
            window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
            while True:
                ret_val, frame = video_capture.read()

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

                cudaImg = cudaFromNumpy(frame)

                detections = net.Detect(cudaImg, overlay='none')

                for detection in detections:                    
                    color = (255, 0, 0) 
                     
                    thickness = 2
                    
                    # Using cv2.rectangle() method 
                    # Draw a rectangle with blue line borders of thickness of 2 px 
                    frame = cv2.rectangle(frame, (int(detection.Left),int(detection.Top)) , (int(detection.Right),int(detection.Bottom)), color, thickness)
                    if detection.TrackStatus >= 0:  # actively tracking
                        print(f"object {detection.TrackID} at ({detection.Left}, {detection.Top}) has been tracked for {detection.TrackFrames} frames")
                        cv2.putText(frame, str(detection.TrackID), (int(detection.Left), int(detection.Top)), font, 1, (255, 255, 0), 3, cv2.LINE_AA) 
                    else:  # if tracking was lost, this object will be dropped the next frame
                        print(f"object {detection.TrackID} has lost tracking")

                # time when we finish processing for this frame 
                new_frame_time = time.time() 
            
                # Calculating the fps 
            
                # fps will be number of frame processed in given time frame 
                # since their will be most of time error of 0.001 second 
                # we will be subtracting it to get more accurate result 
                fps = 1/(new_frame_time-prev_frame_time) 
                prev_frame_time = new_frame_time 
            
                # converting the fps into integer 
                fps = int(fps) 
            
                # converting the fps to string so that we can display it on frame 
                # by using putText function 
                fps = str(fps)
                print("FPS: "+fps)

               
                
                cv2.putText(frame, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA) 

                # Check to see if the user closed the window
                # Under GTK+ (Jetson Default), WND_PROP_VISIBLE does not work correctly. Under Qt it does
                # GTK - Substitute WND_PROP_AUTOSIZE to detect if window has been closed by user
                if(display):
                    if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                        cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
                        cv2.setWindowProperty(window_title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                        cv2.imshow(window_title, frame)
                    else:
                        break 
                    keyCode = cv2.waitKey(10) & 0xFF
                    # Stop the program on the ESC key or 'q'
                    if keyCode == 27 or keyCode == ord('q'):
                        break
        finally:
            video_capture.release()
            cv2.destroyAllWindows()
    else:
        print("Error: Unable to open camera")


if __name__ == "__main__":
    detect(display=True)
