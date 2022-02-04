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

# Obstacle measurement function
widthScale = resW/480.0

# Video capture object
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, resW)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resH)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

def process_frame(cap, curr_map):
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

    # classify shape
    # utils.shapeclassify(frame, showEdge=True)

    frame, contours = utils.get_contours(
        frame,
        # cannyThr=[50,50],
        showEdge=True,
        minArea=1000,
        filter=4,
        draw=True
    )
    print(f'Objects detected: {len(contours)}')

    # get object width
    width = 55
    if len(contours) > 0:
        frame, width, cmWidth, coords = utils.obs_width(
                        frame,
                        contours[0][3],
                        # int(float((distance))),
                        50.0,
                        widthScale,
                        draw=True
                        )

    # draw grid
    frame, x_points, y_points = utils.draw_grid(frame,
                                                obj_width=width,
                                                resolution=(resW, resH)
                                                )

    # viewport matrix size
    m_size = [len(x_points) - 2, len(y_points)]
    print(f"Matrix size: {m_size}")
    # m_size = [(resW // width) - 3, (resH // width) - 2]
    if m_size[0] < 1 or m_size[1] < 1:
        m_size = [12,7]
    print(f"Matrix size: {m_size}")

    # Resize viewport matrix
    curr_map.viewport = map.ViewPort(size=tuple(m_size))
    # curr_map.viewport.show_view()

    if len(contours) != 0:
        obj_x, obj_y, obj_w, obj_h = contours[0][3]
        # print(obj_x)
        obj_center_x = obj_x + (obj_w//2)
        obj_center_y = obj_y + (obj_h//2)
        print(f"obj_center_x: {obj_center_x} obj_center_y: {obj_center_y}")

        mat_col = ((obj_center_x - width) // width)
        mat_row = ((obj_center_y - width) // width)
        print(f"mat_row: {mat_row} mat_col: {mat_col}")


        # update viewport matrix
        try:
            curr_map.viewport.view[mat_row][mat_col] = 9
        except IndexError:
            print("Index out of range")

    # Show viewport matrix
    curr_map.viewport.show_view()



    # process grid info
    # curr_map.viewport.rand_update(2)
    # time.sleep(0.25)

    # fill grid
    # frame = utils.fill_grid(curr_map.viewport, frame, x_points, y_points)

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




