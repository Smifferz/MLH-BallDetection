# Python script that has live trackbars for color selection
#!/usr/bin/python
import cv2
import numpy as np
import imutils

def nothing(x):
    pass

def calibrate():
    # carpetPictures = "frame.jpg"
    cv2.namedWindow('image',2)
    # create trackbars for color change
    cv2.createTrackbar('Hl','image',0,179,nothing)
    cv2.createTrackbar('Sl','image',0,255,nothing)
    cv2.createTrackbar('Vl','image',0,255,nothing)
    cv2.createTrackbar('Hu','image',179,179,nothing)
    cv2.createTrackbar('Su','image',255,255,nothing)
    cv2.createTrackbar('Vu','image',255,255,nothing)

    # img = cv2.imread("frame1.jpg",1)
    camera = cv2.VideoCapture(0)

    # time.sleep(2)
    # img = cv2.medianBlur(img,3)

    while True:
        # Get frame
        (grabbed, img) = camera.read()

        # Get current positions of trackbars
        Hl = cv2.getTrackbarPos('Hl','image')
        Sl = cv2.getTrackbarPos('Sl','image')
        Vl = cv2.getTrackbarPos('Vl','image')

        Hu = cv2.getTrackbarPos('Hu','image')
        Su = cv2.getTrackbarPos('Su','image')
        Vu = cv2.getTrackbarPos('Vu','image')

        lower = np.array([Hl,Sl,Vl])
        upper = np.array([Hu,Su,Vu])

        print("Lower: " + str(lower) + "Higher: " + str(upper) )

        # convert from BGR to HSV colorspace
        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        # Threshold the HSV image to get only selected colors
        mask = cv2.inRange(hsv, lower, upper)
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(img,img, mask= mask)
        # show the image
        cv2.imshow('Mask',mask)
        # cv2.imshow('Picture',res)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break


    cv2.destroyAllWindows()
    # p.terminate()

if __name__ == '__main__':
    calibrate()
    # p = multiprocessing.Process(target = stream.start)
    # p.start()
    # img = imutils.resize(img, width=400)
    # objClass = GA.objectClassification()
    # cali  = calibrateCameras()
    # cali.calibrate()
    # p.terminate()
