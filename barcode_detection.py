# import the necessary packages
import numpy as np
import cv2
import os
import imutils 

def detectvid(image):

	# convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# compute the Scharr gradient magnitude representation of the images
	# in both the x and y direction using OpenCV 2.4
    ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
    gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)
	# subtract the y-gradient from the x-gradient
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

	# blur the image
    blurred = cv2.blur(gradient, (9, 9))

    #threshold the image
    (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

	# construct a closing kernel and apply it to the thresholded image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

	# perform a series of erosions and dilations
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)

	# find the contours in the thresholded image, then sort the contours
    # by their area, keeping only the largest one
    cnts,hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2:]

	# if no contours were found, return None
    if len(cnts) == 0:
        return None

    c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

    # compute the rotated bounding box of the largest contour
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))

    
    return box

def detectimage(image):
    
	# convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    p = os.path.sep.join(['static\shots', "gray.png"])
    cv2.imwrite(p, gray)

	# compute the Scharr gradient magnitude representation of the images
	# in both the x and y direction using OpenCV 2.4
    ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
    gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)
	# subtract the y-gradient from the x-gradient
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)
    p = os.path.sep.join(['static\shots', "gradient-sub.png"])
    cv2.imwrite(p, gradient)

	# blur the image
    blurred = cv2.blur(gradient, (9, 9))
    p = os.path.sep.join(['static\shots', "blur.png"])
    cv2.imwrite(p, blurred)

    #threshold the image
    (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)
    p = os.path.sep.join(['static\shots', "threshold.png"])
    cv2.imwrite(p, thresh)

	# construct a closing kernel and apply it to the thresholded image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    p = os.path.sep.join(['static\shots', "morphology.png"])
    cv2.imwrite(p, closed)

	# perform a series of erosions and dilations
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)
    p = os.path.sep.join(['static\shots', "erode_dilate.png"])
    cv2.imwrite(p, closed)

	# find the contours in the thresholded image, then sort the contours
    # by their area, keeping only the largest one
    cnts,hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2:]

	# if no contours were found, return None
    if len(cnts) == 0:
        return None

    c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

    # compute the rotated bounding box of the largest contour
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))

    cv2.drawContours(image, [box], -1, (0, 255, 0), 3)

    p = os.path.sep.join(['static\shots', "Detected.png"])
    cv2.imwrite(p, image)
    
    return