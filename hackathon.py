#!/usr/bin/env python3

from pathlib import Path
import cv2
import depthai as dai
import numpy as np
import time
import argparse
import serial
from time import sleep
import time
import datetime
from hanging_threads import start_monitoring

#start_monitoring(seconds_frozen = 10, test_interval= 20)

start_time = time.time()

upload_speed = 30

ser = serial.Serial ("/dev/ttyS0", 9600, timeout = 1) 

nnPathDefault = str((Path(__file__).parent / Path('depthai-python/examples/models/mobilenet-ssd_openvino_2021.2_6shave.blob')).resolve().absolute())
parser = argparse.ArgumentParser()
parser.add_argument('nnPath', nargs='?', help="Path to mobilenet detection network blob", default=nnPathDefault)
parser.add_argument('-s', '--sync', action="store_true", help="Sync RGB output with NN output", default=False)
args = parser.parse_args()

if not Path(nnPathDefault).exists():
    import sys
    raise FileNotFoundError(f'Required file/s not found, please run "{sys.executable} install_requirements.py"')

# MobilenetSSD label texts
labelMap = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
            "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

# Create pipeline
pipeline = dai.Pipeline()
pipeline.setOpenVINOVersion(dai.OpenVINO.Version.VERSION_2021_2)

# Define sources and outputs
camRgb = pipeline.createColorCamera()
nn = pipeline.createMobileNetDetectionNetwork()
xoutRgb = pipeline.createXLinkOut()
nnOut = pipeline.createXLinkOut()

xoutRgb.setStreamName("rgb")
nnOut.setStreamName("nn")

# Properties
camRgb.setPreviewSize(300, 300)
camRgb.setInterleaved(False)
camRgb.setFps(40)
# Define a neural network that will make predictions based on the source frames
nn.setConfidenceThreshold(0.5)
nn.setBlobPath(args.nnPath)
nn.setNumInferenceThreads(2)
nn.input.setBlocking(False)

# Linking
if args.sync:
    nn.passthrough.link(xoutRgb.input)
else:
    camRgb.preview.link(xoutRgb.input)

camRgb.preview.link(nn.input)
nn.out.link(nnOut.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    # Output queues will be used to get the rgb frames and nn data from the outputs defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
    qDet = device.getOutputQueue(name="nn", maxSize=4, blocking=False)

    frame = None
    detections = []
    filterSize = 145
    objectsPerFrame = [0] * filterSize
    currentFilterIndex = 0
    startTime = time.monotonic()
    counter = 0
    color2 = (255, 255, 255)
    currentLabel = ""
    objectCount = 0
    lastLoopCount = 0
    
    

    # nn data (bounding box locations) are in <0..1> range - they need to be normalized with frame width/height
    def frameNorm(frame, bbox):
        normVals = np.full(len(bbox), frame.shape[0])
        normVals[::2] = frame.shape[1]
        return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)

    def displayFrame(name, frame, currLabel):
        color = (255, 0, 0)
        lastLabel = "";
        objectToDetect = "car"
        global objectsPerFrame
        global currentFilterIndex
        global filterSize
        currentLoopCount = 0;
        for detection in detections:
            if labelMap[detection.label] == "car" or labelMap[detection.label] == "bus" or labelMap[detection.label] == "motorbike" or labelMap[detection.label] == "person":
                currentLoopCount += 1
                lastLabel = labelMap[detection.label];
#                 bbox = frameNorm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
#                 cv2.putText(frame, f"{int(detection.confidence * 100)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color)
#                 cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
#         # Show the frame
#         cv2.imshow(name, frame)
        objectsPerFrame[currentFilterIndex] = currentLoopCount
        currentFilterIndex += 1
        if currentFilterIndex >= filterSize:
            currentFilterIndex = 0
        return lastLabel
    
    
    
    def calculateObjectsPerFrame (objPerFrame, filterSize, serialPort):
        #median approach
        global objectCount
        global lastLoopCount
        np.sort(objPerFrame)
        currentLoopCount = objPerFrame[int(filterSize/2)]#gets the mid point of sorted array
        global start_time
        difference  = time.time() - start_time
        #print("time difference: ", difference)
        if (difference) >= upload_speed:
            start_time = time.time()
            print('serial count=' + str(objectCount));
            #Send new count to raspberry pi serial port
            serialPort.write((str(objectCount) + '\n').encode())
                    
        if currentLoopCount > lastLoopCount:
            objectCount += (currentLoopCount - lastLoopCount)
            print('object count=' + str(objectCount));
            if objectCount > 65535:
                objectCount = 0
            #serialPort.write((str(objectCount) + '\n').encode())
        lastLoopCount = currentLoopCount
        
    while True:
        if args.sync:
            # Use blocking get() call to catch frame and inference result synced
            inRgb = qRgb.get()
            inDet = qDet.get()
        else:
            # Instead of get (blocking), we use tryGet (nonblocking) which will return the available data or None otherwise
            inRgb = qRgb.tryGet()
            inDet = qDet.tryGet()

        if inRgb is not None:
            frame = inRgb.getCvFrame()
            cv2.putText(frame, "NN fps: {:.2f}".format(counter / (time.monotonic() - startTime)),
                        (2, frame.shape[0] - 4), cv2.FONT_HERSHEY_TRIPLEX, 0.4, color2)

        if inDet is not None:
            detections = inDet.detections
            counter += 1

        # If the frame is available, draw bounding boxes on it and show the frame
        if frame is not None:
            currentLabel = displayFrame("rgb", frame, currentLabel)
            calculateObjectsPerFrame(objectsPerFrame, filterSize, ser)

        if cv2.waitKey(1) == ord('q'):
            break