# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv

mpl.rcParams['legend.fontsize'] = 10
# Configure the figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set up the plot
g1, = plt.plot([] ,[], [])

# Set size of axes
plt.axis([0, 600, 0, 400])

ax.set_zlim(0, 400)
z = []
counter = 0

line_x = []
line_y = []
line_z = []

def update_line(g1, x, y, z):
    ax.scatter(float(x),float(y),float(z),c='r', marker='_')

def create_line(x,y,z):
    line_x.append(float(x))
    line_y.append(float(y))
    line_z.append(float(z))
    return ax.plot(line_x, line_y, line_z, c='b')

def update_sphere(u, v, x, y, z):
    spherex = float(x) + (10 * np.outer(np.cos(u), np.sin(v)))
    spherey = float(y) + (10 * np.outer(np.sin(u), np.sin(v)))
    spherez = float(z) + (10 * np.outer(np.ones(np.size(u)), np.cos(v)))
    surfaceobject = create_sphere(spherex, spherey, spherez)
    return surfaceobject

def create_sphere(x,y,z):
    sphere = ax.plot_surface(x,y,z,rstride=4, cstride=4, color='b', linewidth=0, alpha=0.5)
    return sphere

def main():
	global counter
	# To hold the x,y,z coordinates of the ball
	ball = {}

	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video",
		help="path to the (optional) video file")
	ap.add_argument("-b", "--buffer", type=int, default=64,
		help="max buffer size")
	args = vars(ap.parse_args())

	# define the lower and upper boundaries of the "green"
	# ball in the HSV color space, then initialize the
	# list of tracked points
	greenLower = (29, 86, 6)
	greenUpper = (64, 255, 255)
	pts = deque(maxlen=args["buffer"])

	# if a video path was not supplied, grab the reference
	# to the webcam
	if not args.get("video", False):
		camera = cv2.VideoCapture(0)

	# otherwise, grab a reference to the video file
	else:
		camera = cv2.VideoCapture(args["video"])
		# keep looping


	while True:
		# grab the current frame
		(grabbed, frame) = camera.read()
		frame = cv2.flip(frame, 1)
		# if we are viewing a video and we did not grab a frame,
		# then we have reached the end of the video
		if args.get("video") and not grabbed:
			break

		# resize the frame, blur it, and convert it to the HSV
		# color space
		frame = imutils.resize(frame, width=600)
		# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		# construct a mask for the color "green", then perform
		# a series of dilations and erosions to remove any small
		# blobs left in the mask
		mask = cv2.inRange(hsv, greenLower, greenUpper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
		# find contours in the mask and initialize the current
		# (x, y) center of the ball
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)[-2]
		center = None

		# only proceed if at least one contour was found
		if len(cnts) > 0:
			# find the largest contour in the mask, then use
			# it to compute the minimum enclosing circle and
			# centroid
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

			# only proceed if the radius meets a minimum size
			if radius > 10:
				# draw the circle and centroid on the frame,
				# then update the list of tracked points
				cv2.circle(frame, (int(x), int(y)), int(radius),
					(0, 255, 0), 2)
				cv2.circle(frame, center, 5, (0, 0, 255), -1)

		# update the points queue
		pts.appendleft(center)

		if len(cnts) > 0:
			y = int(cv2.contourArea(c))
			y_scaled = (y/15000)*500

			ball['x'] = float(int(pts[0][0]))
			ball['z'] = float(400 - int(pts[0][1]))
			ball['y'] = float(int(y_scaled))
			# print("x: " + str(ball['x']) + " y: " + str(ball['y']) + " z: " + str(ball['z']))
			update_line(g1, ball['x'], ball['y'], ball['z'])
			u = np.linspace(100, 100 + (2 * np.pi), 100)
			v = np.linspace(100, 100 + np.pi, 100)

			if counter == 0:
				counter = 1
			else:
				surface.remove()
				line.pop(0).remove()

			surface = update_sphere(u,v, ball['x'], ball['y'], ball['z'])
			line = create_line(ball['x'], ball['y'], ball['z'])
			plt.pause(0.001)

		# loop over the set of tracked points
		# for i in range(1, len(pts)):
			# if either of the tracked points are None, ignore
			# them
			# if pts[i - 1] is None or pts[i] is None:
				# continue

			# otherwise, compute the thickness of the line and
			# draw the connecting lines
			# thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
			# cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

		# show the frame to our screen
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# if the 'q' key is pressed, stop the loop
		if key == ord("q"):
			break

	# cleanup the camera and close any open windows
	camera.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':

	main()
