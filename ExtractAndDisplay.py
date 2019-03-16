#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import queue

# filename of clip to load
fileName = 'clip.mp4'
BUF_SIZE = 10
buf = queue.Queue(BUF_SIZE) # buffer for original video
bufGray = queue.Queue(BUF_SIZE) # buffer for grayscale video
# create semaphores
sem1 = threading.Semaphore(BUF_SIZE)
sem2 = threading.Semaphore(BUF_SIZE)

def extractFrames():
    # Initialize frame count
    count = 0
    # open video file
    vidcap = cv2.VideoCapture(fileName)
    # read first image
    success,image = vidcap.read()
    print("Reading frame {} {} ".format(count, success))
    while success:
        jpgAsText = encodeFrame(image)
        # add the frame to the buffer
        buf.put(jpgAsText)
        sem1.acquire()
        success,image = vidcap.read()
        print('Reading frame {} {}'.format(count, success))
        count += 1
    print("Frame extraction complete")
    # add end of queue string
    buf.put("end")
    sem1.acquire()

def convertFrames():
    # initialize frame count
    count = 0
    frameAsText = ""
    # go through each frame in the buffer until the buffer is empty
    while True:
        # get the next frame
        frameAsText = buf.get()
        if(frameAsText == "end"):
            break
        sem1.release()
        img = decodeFrame(frameAsText)
        print("Converting frame {}".format(count))
        grayscaleJpgAsText = convertToGrayscaleAndEncode(img)
        # add the frame to the buffer
        bufGray.put(grayscaleJpgAsText)
        sem2.acquire()
        count += 1
    print("Finished converting all frames")
    # add end of queue string
    bufGray.put("end")
    sem2.acquire()


def displayFrames():
    # initialize frame count
    count = 0
    frameAsText = ""

    # go through each frame in the buffer until the buffer is empty
    while True:
        # get the next frame
        frameAsText = bufGray.get()
        if(frameAsText == "end"):
            break
        sem2.release()
        img = decodeFrame(frameAsText)
        print("Displaying frame {}".format(count))
        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow("Video", img)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break
        count += 1
    print("Finished displaying all frames")
    # cleanup the windows
    cv2.destroyAllWindows()

def decodeFrame(frameAsText):
    # decode the frame
    jpgRawImage = base64.b64decode(frameAsText)
    # convert the raw frame to a numpy array
    jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)
    # get a jpg encoded frame
    img = cv2.imdecode( jpgImage ,cv2.IMREAD_UNCHANGED)
    return img

def convertToGrayscaleAndEncode(img):
    # convert the image to grayscale
    grayscaleFrame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # encode
    grayscaleJpgAsText = encodeFrame(grayscaleFrame)
    return grayscaleJpgAsText

def encodeFrame(image):
    # get a jpg encoded frame
    success, jpgImage = cv2.imencode('.jpg', image)
    #encode the frame as base 64 to make debugging easier
    jpgAsText = base64.b64encode(jpgImage)
    return jpgAsText

# extract the frames thread
extractThread = threading.Thread(target=extractFrames)
# convert the frames thread
convertThread = threading.Thread(target=convertFrames)
# display the frames thread
displayThread = threading.Thread(target=displayFrames)

# run threads
extractThread.start()
convertThread.start()
displayThread.start()
