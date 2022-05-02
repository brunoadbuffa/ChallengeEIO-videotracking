#Imports:
import cv2
import numpy as np
import json
import logging


# Set logging config

log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt)
logger = logging.getLogger(__name__)


class ObjectTracker():
    '''MULTIPLE OBJECT TRACKER: 
    
    Class to perform multiple object tracking using OpenCV. 
    To achieve our multi-object tracking task, we use the 
    cv2.MultiTracker_Create function of OpenCV ("legacy" 
    package in fact). This method allows us to instantiate 
    single object trackers and then add them to a class that 
    updates the object locations for us. Finally, the frames 
    with the tracked objects are stored in an output video.
    '''

    def __init__(self, cv2_tracker, fps_out, video_path, initial_cond):
        """ Init
        
        :param cv2_tracker: name of the single object tracker.
        :type statistics: str
        :param fps_out: frames per second in output video.
        :type fps_out: integer
        :param video_path: input video path.
        :type video_path: str
        :param initial_cond: path of the input JSON file for initial conditions.
        :type initial_cond: str
        """
        self.cv2_tracker = cv2_tracker
        self.fps_out = fps_out
        self.video_path = video_path
        self.initial_cond_file = initial_cond

    def run_model(self, display=False, out_video_path = 'data/video_tracking.avi'):
        """Execute the Multiple Object Tracking model
        
        :param display: display the traking frames for each step.
        :type statistics: bool
        :param out_video_path: path for the output video.
        :type statistics: str
        """

        TrDict = {'csrt': cv2.legacy.TrackerCSRT_create,
         'kcf' : cv2.legacy.TrackerKCF_create,
         'boosting' : cv2.legacy.TrackerBoosting_create,
         'mil': cv2.legacy.TrackerMIL_create,
         'tld': cv2.legacy.TrackerTLD_create,
         'medianflow': cv2.legacy.TrackerMedianFlow_create,
         'mosse':cv2.legacy.TrackerMOSSE_create}
        
        logger.info("Initializing MultiTracker object")
        trackers = cv2.legacy.MultiTracker_create()
        v = cv2.VideoCapture(self.video_path)

        # load the initial bounding boxes from a JSON file
        logger.info("Loading initial conditions")
        with open(self.initial_cond_file) as f:
            data = json.load(f)
        bboxes = [obj['coordinates'] for obj in data]
        
        # create the initial bounding boxes for the objects to track
        logger.info("Creating the initial bounding boxes")
        ret, frame = v.read()
        k = len(bboxes)
        for i in range(k):
            bb = bboxes[i]
            tracker = TrDict[self.cv2_tracker]()
            trackers.add(tracker,frame,bb)

        #prepare the output video
        logger.info("Preparing the output video")
        height, width, layers = frame.shape
        size = (width, height)
        out = cv2.VideoWriter(out_video_path, cv2.VideoWriter_fourcc(*'DIVX'), self.fps_out, size)

        # loop over frames from the video
        logger.info("Iterating over frames from the video")
        while True:
            ret, frame = v.read()
            if not ret:
                break
            (success, boxes) = trackers.update(frame)
            for box in boxes:
                (x,y,w,h) = [int(a) for a in box]
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2) #color for the bbox:RED
            
            # display on
            if display:
                cv2.imshow('Frame',frame)

            #write the actual frame to de output video
            out.write(frame) 

        v.release()
        out.release()
        cv2.destroyAllWindows()
        
        logger.info(f'The video with the tracked objects was successfully saved in the file: {out_video_path}')
        
        return

