"""
Author: Sharome Burton
Date: 01/20/2022

"""

# imports
import numpy as np
import cv2
import time
import utils
import map

from rich import print

# Video Resolution
resW = 800	    # Resolution width and
resH = (resW//16)*9	# Height	(aspect ratio must be 16:9)

# Video capture object
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, resW)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resH)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

def process_frame(cap, map):
    """
    main function
    """
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        end_prog(cap)
        exit(0)

    # # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # draw grid
    frame, x_points, y_points = utils.draw_grid(frame, (resW,resH))

    # process grid info
    map.viewport.rand_update(2)
    # time.sleep(0.25)

    # fill grid
    frame = utils.fill_grid(map.viewport, frame, x_points, y_points)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        end_prog(cap)
        exit(0)

def end_prog(cap):
    """
    Exits program
    """
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

# utils.draw_grid(cap)
new_map = map.Map()
# new_map.show_map()
new_map.show_view()



while True:
    process_frame(cap, new_map)




