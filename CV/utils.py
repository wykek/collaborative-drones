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

# Table for estimating object width (distance: pixels per cm)

pixelToCm = {"9": 65.00,
             "10": 56.00,
             "11": 49.06,
             "12": 43.12,
             "13": 36.56,
             "14": 33.50,
             "15": 31.15,
             "16": 29.71,
             "17": 28.00,
             "18": 26.03,
             "19": 24.52,
             "20": 23.77,
             "21": 22.95,
             "22": 22.13,
             "23": 21.31,
             "24": 20.48,
             "25": 19.67,
             "26": 18.92,
             "27": 18.16,
             "28": 17.41,
             "29": 16.65,
             "30": 15.90,
             "31": 15.54,
             "32": 15.18,
             "33": 14.82,
             "34": 14.46,
             "35": 14.10,
             "36": 13.73,
             "37": 13.37,
             "38": 13.01,
             "39": 12.65,
             "40": 12.29,
             "41": 11.85,
             "42": 11.41,
             "43": 10.96,
             "44": 10.52,
             "45": 10.08,
             "46": 9.64,
             "47": 9.20,
             "48": 8.75,
             "49": 8.31,
             "50": 7.87,
             "51": 7.42

             }

def draw_grid(frame, obj_width = 50, resolution = (800,450), size = (16,9)):
    """
    pass
    """
    # x_points = [x for x in range((resolution[0]//size[0]), resolution[0] + (resolution[0]//size[0]), (resolution[0]//size[0]))]
    #
    # y_points = [y for y in range((resolution[1]//size[1]), resolution[1] + (resolution[1] // size[1]), (resolution[1] // size[1]))]

    x_points = [x for x in range(obj_width, resolution[0] - obj_width + 1,
                                 obj_width)]

    y_points = [y for y in range(obj_width, resolution[1] - obj_width + 1,
                                 obj_width)]

    # print(x_points)
    # print(y_points)

    # Draw vertical lines
    for x in x_points:
        frame = cv2.line(frame, (x,0), (x,resolution[1]), blue, 1)

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

    # print(len(y_points))
    for y in y_points:

        y_count += 1
        y_coord = (y_points[y_count]) + (resolution[1]//size[1]) // 2  # center
        # print("y_count", y_count)

        # for y in y_points:
        #     y_coord = (resolution[1] // size[1]) // 2 # center
        #     y_count += 1
        #     print("y_count", y_count)

        # print(len(x_points))
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


# Returns closed contours with a specified number of corners and a minimum area
def get_contours(frame, cannyThr=[100, 100], showEdge=False,
                 minArea=5000, filter=0, draw=False):
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameBlur = cv2.GaussianBlur(frameGray, (5, 5), 1)
    frameCanny = cv2.Canny(frameBlur, cannyThr[0], cannyThr[1])
    kernel = np.ones((5, 5))
    frameDilate = cv2.dilate(frameCanny, kernel, iterations=2)
    frameThreshold = cv2.erode(frameDilate, kernel, iterations=2)
    if showEdge: cv2.imshow('Edge detection', frameThreshold)

    contours, hierarchy = cv2.findContours(frameThreshold,
                                           cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2:]

    finalContours = []

    if len(contours) > 0:
        for i in contours:
            area = cv2.contourArea(i)
            if area > minArea:
                peri = cv2.arcLength(i, True)  # perimeter
                corners = cv2.approxPolyDP(i, 0.02 * peri, True)  # corner points
                bounds = cv2.boundingRect(corners)  # bounding box
                if filter > 0:
                    if len(corners) == filter:
                        finalContours.append([len(corners), area, corners, bounds, i])
                else:
                    finalContours.append([len(corners), area, corners, bounds, i])

        # Sorts closed contours according to size (biggest first)
        finalContours = sorted(finalContours, key=lambda x: x[1], reverse=True)

        # Draws contours onto image
        if draw:
            for contours in finalContours:
                cv2.drawContours(frame, contours[4], -1, (0, 0, 255), 3)

        return frame, finalContours

    else:
        return frame, finalContours


def obs_width(frame, bounds, dist, widthScale, draw=False, cm=False):
    if len(bounds) > 0:

        xMin = bounds[0]
        xMinCoord = (bounds[0], bounds[1])

        xMax = xMin + bounds[2]
        xMaxCoord = (xMax, bounds[1])

        width = xMax - xMin
        cmWidth = 1.0

        coords = (xMinCoord, xMaxCoord)

        # Draws line connecting points in question
        if draw:
            if len(xMinCoord) == 2 and len(xMinCoord) == 2:
                cv2.line(frame, xMinCoord, xMaxCoord, (255, 0, 255), 3)
                if cm:
                    if dist >= 10 and dist <= 50:
                        distance = dist  # Distance to object
                        pixelRatio = pixelToCm.get(str(distance))
                        cmWidth = round(width * widthScale / pixelRatio, 1)

                        cv2.putText(frame, 'width(cm): ' + str(cmWidth), (bounds[0], bounds[1] - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

                    else:
                        cv2.putText(frame, 'Target out of range', (bounds[0], bounds[1] - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                else:
                    cv2.putText(frame, 'width(p): ' + str(width), (bounds[0], bounds[1] - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

        return frame, width, cmWidth, coords

    else:
        return frame

def pixel_width_hor(frame, contours, draw=False):
    if len(contours) > 0:
        # print(contours)
        xMin = contours[0][0][0]
        xMinCoord = contours[0]
        # print(xMin)
        xMax = contours[0][0][0]
        xMaxCoord = contours[0]
        # print(xMax)

        for cnt in contours:
            # print(cnt)
            if cnt[0][0] < xMin:
                xMin = cnt[0][0]
                xMinCoord = cnt[0]
            elif cnt[0][0] > xMax:
                xMax = cnt[0][0]
                xMaxCoord = cnt[0]

        width = xMax - xMin

        xMinCoord = tuple(xMinCoord)  # Leftmost pixel
        xMaxCoord = tuple(xMaxCoord)  # Rightmost pixel
        coords = (xMinCoord, xMaxCoord)

        # Draws points in question
        if draw:
            if len(xMinCoord) == 2 and len(xMinCoord) == 2:
                cv2.circle(frame, xMinCoord, 5, (255, 0, 255), -1)
                cv2.circle(frame, xMaxCoord, 10, (255, 0, 255), -1)

        return frame, width, coords

    else:
        return frame

def shapeclassify(frame, minShapeArea=2500, showEdge=False):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 1)
    canny = cv2.Canny(blur, 50, 50)
    if showEdge: cv2.imshow('Shape Edge Detection', canny)

    contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2:]

    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(f'Area of shape:{area}')
        if area > minShapeArea:
            cv2.drawContours(frame, cnt, -1, (255, 0, 0), 2)
            peri = cv2.arcLength(cnt, True)


            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            # print(len(approx))
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)

            if objCor == 3:
                objectType = "Triangle"

            elif objCor == 4:
                aspRatio = w / float(h)
                if aspRatio > 0.95 and aspRatio < 1.05:
                    objectType = "Square"
                else:
                    objectType = "Rectangle"

            # elif objCor == 5:
            #     objectType = "Pentagon"
            # elif objCor == 6:
            #     objectType = "Hexagon"
            # elif objCor == 7:
            #     objectType = "Heptagon"
            # elif objCor == 8:
            #     objectType = "Octagon"
            # else:
            #     objectType = "Ellipse"

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(frame, objectType, (x + (w // 2) - 10, y + (h // 2) - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                        (255, 0, 255), 1, cv2.LINE_AA)


