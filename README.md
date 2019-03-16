# Producer Consumer Lab
For this lab I implemented a trivial producer-consumer system using
python threads where all coordination is managed by counting and binary
semaphores for a system of two producers and two consumers. The producers and
consumers will form a simple rendering pipeline using multiple threads. One
thread will read frames from a file, a second thread will take those frames
and convert them to grayscale, and the third thread will display those
frames. The threads will run concurrently.

## How to run
Run the following command:
```
$ python3 ExtractAndDisplay.py
```

## ExtractAndDisplay.py
This file loads a series of frames from a video contained in 'clip.mp4',
converts them to grayScale, and displays them with a 42ms delay.

First the video is broken down into frames. Each frame will be extracted in
the method `extractFrames()`, and then it will be converted to grayscale in
the method `convertFrames()`. After being converted, it will be displayed in a
video in the method `displayFrames()`.

