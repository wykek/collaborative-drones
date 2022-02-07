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
from random import randint

# frame delay
delay = 0.1

# Font
font = cv2.FONT_HERSHEY_COMPLEX

# Video Resolution
resW = 1600	    # Resolution width and
resH = (resW//16)*9	# Height	(aspect ratio must be 16:9)

# Obstacle measurement function
widthScale = resW/480.0

# Video capture object
cap = cv2.VideoCapture(1)

# QR Code Detector
det = cv2.QRCodeDetector()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, resW)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resH)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

def key_input(cap, curr_map, wait=1):
    if cv2.waitKey(wait) == ord('q'):
        end_prog(cap)
        return 'q'

    if cv2.waitKey(wait) == ord('w'):
        curr_map.move_cam('up', 2)
        print("UP pressed")
        return 'w'

    if cv2.waitKey(wait) == ord('s'):
        return 's'

    if cv2.waitKey(wait) == ord('a'):
        return 'a'

    if cv2.waitKey(wait) == ord('d'):
        return 'd'

    return None


def process_frame(cap, curr_map, det, key):
    """
    main function
    """

    # test: shift map
    new_coords = curr_map.viewport.coords

    if key == 'w':
        new_coords = curr_map.move_cam('up', 1)
        print(f"\n\nNEW CAM COORDS: {new_coords}")

    if key == 's':
        new_coords = curr_map.move_cam('down', 1)
        print(f"\n\nNEW CAM COORDS: {new_coords}")

    if key == 'a':
        new_coords = curr_map.move_cam('left', 1)
        print(f"\n\nNEW CAM COORDS: {new_coords}")

    if key == 'd':
        new_coords = curr_map.move_cam('right', 1)
        print(f"\n\nNEW CAM COORDS: {new_coords}")

    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        end_prog(cap)
        exit(0)

    # # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    orig_frame = frame

    # classify shape
    # utils.shapeclassify(frame, showEdge=True)

    frame, contours = utils.get_contours(
        frame,
        # cannyThr=[50,50],
        showEdge=True,
        min_area=1000,
        max_area=100000,
        filter=4,
        draw=True
    )
    print(f'Objects detected: {len(contours)}')

    # get object width
    width = 80
    dist = ""
    if len(contours) > 0:
        frame, width, cmWidth, coords = utils.obs_width(
                        frame,
                        contours[0][3],
                        # int(float((distance))),
                        50.0,
                        widthScale,
                        draw=True
                        )

        # Filter out small widths
        if width < 150:
            width = 150

        # Draw ROI
        ROI = utils.get_ROI(orig_frame, bounds=contours[0][3])

        print(f"width: {width}")
        print(f"distance to: {3000/width}")
        dist = str("distance to: " + str(round(3000/width)) + "cm")


        ### Establish reference cell in grid ###

        qr = utils.scan_qr(ROI, det)
        if qr != None:
            print(f"VALID QR! message: {qr}")
            try:
                qr_id = int(qr[-1])
            except IndexError:
                qr_id = 9

            # draw grid
            frame, x_points, y_points, closest_x, closest_y = utils.draw_grid(frame,
                                                        contours[0][3],
                                                        obj_width=width,
                                                        resolution=(resW, resH)
                                                        )
            # display estimated distance
            cv2.putText(frame, dist, (contours[0][3][0], contours[0][3][1]-20), font, 0.5,
                        (255, 0, 255), 1, cv2.LINE_AA)

            # viewport matrix size
            m_size = [len(x_points) - 1, len(y_points) - 1]
            print(f"Matrix size: {m_size}")
            # m_size = [(resW // width) - 3, (resH // width) - 2]
            if m_size[0] < 1 or m_size[1] < 1:
                m_size = [3,3]
            # print(f"Matrix size: {m_size}")

            # Resize viewport matrix
            if new_coords != None:
                curr_map.viewport = map.ViewPort(new_coords, size=tuple(m_size))
            else:
                curr_map.viewport = map.ViewPort(curr_map.viewport.coords, size=curr_map.viewport.view.shape)
            # curr_map.viewport.show_view()

            if len(contours) != 0:
                obj_x, obj_y, obj_w, obj_h = contours[0][3]
                # print(obj_x)
                obj_center_x = obj_x + closest_x + ((obj_w)//2)
                obj_center_y = obj_y + closest_y + ((obj_h)//2)
                print(f"obj_center_x: {obj_center_x} obj_center_y: {obj_center_y}")

                mat_col = ((obj_center_x - width) // width)
                mat_row = ((obj_center_y - width) // width)
                print(f"mat_row: {mat_row} mat_col: {mat_col}")

                # update viewport matrix
                try:
                    curr_map.viewport.view[mat_row][mat_col] = 9
                except IndexError:
                    print("Index out of range")

                frame, curr_map.viewport.view = utils.gen_ROI_grid(frame,
                                                                   m_size,
                                                                   ref_loc= (mat_row, mat_col),
                                                                   ref_qr = qr_id,
                                                                   det = det,
                                                                   bounds = contours[0][3],
                                                                   draw=True)

            # Show viewport matrix
            curr_map.viewport.show_view()


            # Show full map matrix
            # print(f"UPDATING MAP: coords: {curr_map.viewport.coords}")
            curr_map.update_map()
            curr_map.show_map()





    # process grid info
    # curr_map.viewport.rand_update(2)
    # time.sleep(0.25)

    # fill grid
    # frame = utils.fill_grid(curr_map.viewport, frame, x_points, y_points)

    cv2.putText(frame, dist, (resW - 1500, 50), font, 0.5,
                (255, 255, 255), 1, cv2.LINE_AA)

    # Display the resulting frame

    cv2.imshow('frame', frame)

    time.sleep(delay)


    # if cv2.waitKey(1) == ord('q'):
    #     end_prog(cap)
    #     exit(0)

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


test_cam_directions = ['w', 's', 'a', 'd', None]

while True:
    key = key_input(cap, new_map, wait=100)
    if key == None:
        key = test_cam_directions[randint(0, len(test_cam_directions) - 1)]
        print(f'\n\nKEY: {key}')

    process_frame(cap, new_map, det, key)






