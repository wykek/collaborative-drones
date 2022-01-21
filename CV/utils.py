"""
Author: Sharome Burton
Date: 01/20/2022

"""
import cv2
import numpy as np

from rich import print

# Green color in BGR
green = (0, 255, 0)
blue = (255, 0, 0)

def draw_grid(frame, resolution = (800,450), size = (16,9)):
    """
    pass
    """
    x_points = [x for x in range((resolution[0]//size[0]), resolution[0] + (resolution[0]//size[0]), (resolution[0]//size[0]))]

    y_points = [y for y in range((resolution[1]//size[1]), resolution[1] + (resolution[1] // size[1]), (resolution[1] // size[1]))]

    # print(x_points)
    # print(y_points)

    # Draw vertical lines
    for x in x_points:
        frame = cv2.line(frame, (x,0), (x,resolution[1]), blue, 2)

    # Draw horizontal lines
    for y in y_points:
        frame = cv2.line(frame, (0,y), (resolution[0],y), blue, 2)

    return frame, x_points, y_points

def fill_grid(viewport, frame, x_points, y_points, resolution = (800,450), size = (16,9)):
    """
    pass
    """
    x_count = -1
    y_count = -1

    print(viewport.view.shape)

    # for x in x_points:
    #     x_coord = (resolution[0]//size[0]) // 2 # center
    #     x_count += 1
    #     print("x_count", x_count)

    print(len(y_points))
    for y in y_points:

        y_count += 1
        y_coord = (y_points[y_count]) + (resolution[1]//size[1]) // 2  # center
        # print("y_count", y_count)

        # for y in y_points:
        #     y_coord = (resolution[1] // size[1]) // 2 # center
        #     y_count += 1
        #     print("y_count", y_count)

        print(len(x_points))
        for x in x_points:
            x_count += 1
            x_coord = (x_points[x_count]) + (resolution[0] // size[0]) // 2  # center
            # print("x_count", x_count)

            if viewport.view[y_count][x_count] != 0:
                frame = cv2.circle(frame, (x_coord, y_coord) , 7, green, thickness=3)
            else:
                print(f"object at {y_count}, {x_count}")


        x_count = -1
    y_count = -1

    return frame




