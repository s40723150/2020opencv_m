import cv2
import numpy as np
Vid_cap = cv2.VideoCapture(0) # use webcam to catch image
Vid_cap.set(3,640)
Vid_cap.set(4,480)

def empty(a):
    pass

#kernel = np.ones((2, 2),np.uint8)

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("Canny Min", "TrackBars", 52, 255, empty)
cv2.createTrackbar("Canny Max", "TrackBars", 50, 255, empty)

while True:
    get,vid = Vid_cap.read()

    rows, cols, channels = vid.shape
    F_place = vid[0:rows, 0:cols]
    c_min = cv2.getTrackbarPos("Canny Min", "TrackBars")
    c_max = cv2.getTrackbarPos("Canny Max", "TrackBars")


    #print(c_min, c_max)
    Vid_Gray = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY) # convert BGR to gray
    Vid_GBlur = cv2.GaussianBlur(Vid_Gray, (7, 7),0) # smooth the Vid_Gray
    Vid_Canny = cv2.Canny(Vid_GBlur, c_min, c_max) # find edges
    #Vid_Dialation = cv2.dilate(Vid_Canny, kernel, iterations=1)

    Filter = Vid_Canny

    thresh, mask = cv2.threshold(Filter, 240, 255, cv2.THRESH_BINARY)
    #Use Vid_Canny to make mask
    F_mask = cv2.bitwise_and(Filter, Filter, mask=mask)
    F_bgr = cv2.cvtColor(F_mask,cv2.COLOR_GRAY2BGR)
    dst = cv2.add(vid, F_bgr) # mix video with filter

    #cv2.imshow("Camera_Filter", Vid_Canny)
    # cv2.imshow("Camera_GBlur", Vid_GBlur)
    # cv2.imshow("Camera_GBlur2", Vid_GBlur2)
    # #cv2.imshow("Mask", mask)
    cv2.imshow("dst", dst)
    #cv2.imshow("Camera", vid)

    key = cv2.waitKey(10) & 0XFF
    esc = 27
    if key == esc:
        break