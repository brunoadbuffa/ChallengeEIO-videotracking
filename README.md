# ChallengeEIO-videotracking
Repository for video tracking in Python.

In this repository, you can find the files to run a program to track different objects in a video. To do this, the following steps must be carried out:

## Docker Build
```sh
$ docker-compose build
```

## Run the Program & Save the Output
```sh
$ docker-compose up
```

## Multiple Object Tracking with OpenCV - Python

### Program

This program accepts as **input parameters** the video, which is going to be processed, and a JSON file where the initial position of each of the objects to be tracked is defined. The JSON file contains the bounding box of each object in tuple format *(x, y, width, height)* where x and y represent the coordinates of the pixels in the upper left corner of the bounding box, width and height are the width and height, in pixels, of the bounding box.

To run the program, the "main.py" file (in directory: '/model') is executed in a docker container. A video is generated as **output** with the data obtained from tracking. This video shows for each frame the bounding boxes obtained for each of the defined objects. By default, the output video is saved in '/data' directory.

### Algorithm

The method followed here to perform the tracking is based on the OpenCV library and its implementation in Python language. In particular, OpenCV version 4.5.5 was used here.

First, a Python class was defined to carry out the proposed task. This class is used to create the model in charge of tracking each object, defining the output video parameters, and passing the inputs of our model (video to be tracked and initial positions of the objects).

Once this is done, we proceed to start with the tracking. To do this, choose the object tracker to be used for the tracking of each particular object (there are several options for this, see: https://docs.opencv.org/4.5.1/d0/d0a/classcv_1_1Tracker.html#a22cb8a580dbbf280ceef21a04463c307). By default, the CSRT-Tracker is chosen due to its balance between accuracy and speed (see for references: https://www.researchgate.net/publication/310953390_Discriminative_Correlation_Filter_with_Channel_and_Spatial_Reliability). 

Then the tracking process is initialized in which the initial bounding boxes are defined for each object to be tracked. This information is passed to the previously defined tracker and the location of the object in the next frame is obtained. This process is iterated until the frames of the video entered as input are consumed.

*Note: To get faster and more efficient object tracking, we will need to leverage multiple processes and spread the computational load across 
multiple cores of our processor.*
