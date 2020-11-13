import cv2

# use webcam to catch image
Vid_cap = cv2.VideoCapture(0)
Vid_cap.set(3, 640)
Vid_cap.set(4, 480)

key = cv2.waitKey(10) & 0XFF
esc = 27

def empty(a):
    pass


window_name = "Outline_Filter"

# trackbar
cv2.namedWindow(window_name)
cv2.resizeWindow(window_name, 640, 560)
cv2.createTrackbar("Canny 1", window_name, 52, 255, empty)
cv2.createTrackbar("Canny 2", window_name, 50, 255, empty)


def filter(mode_number):
    GBlur = cv2.GaussianBlur(vid, (7, 7), 0)  # smooth the Vid_Gray
    Gray = cv2.cvtColor(GBlur, cv2.COLOR_BGR2GRAY)  # convert BGR to gray
    Canny = cv2.Canny(Gray, c_1, c_2)  # find edges
    filter_list = [GBlur, Gray, Canny]
    mode_number = -1
    return filter_list[mode_number]


def recorder_avi(file_name, framerate):
    if file_name == None:
        file_name = "out.avi"
    elif framerate == None:
        framerate = 29
    else:
        print(file_name, framerate)
        pass

    # fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
    fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    resolution = (vid.shape[1], vid.shape[0])  # (640, 480)
    print(resolution)

    # VideoOutPut = cv2.VideoWriter(filename, codec, framerate, resolution)
    output_movie = cv2.VideoWriter(file_name, fourcc, framerate, resolution)
    return output_movie


def frames(vid, Filter):
    thresh, mask = cv2.threshold(Filter, 240, 255, cv2.THRESH_BINARY)
    # Use Vid_Canny to make mask
    F_mask = cv2.bitwise_and(Filter, Filter, mask=mask)
    F_bgr = cv2.cvtColor(F_mask, cv2.COLOR_GRAY2BGR)
    Outline = cv2.add(vid, F_bgr)  # mix video with filter
    return Outline

def rec():
    while key == ord('r'):
        recorder = recorder_avi("out.avi", 29)
        frames(vid, Filter)
        recorder.write(Outline)
        if key == ord('s'):
            recorder.release()
            break
        elif key == esc:
            break
        else:
            pass

while True:
    get, vid = Vid_cap.read()

    rows, cols, channels = vid.shape
    F_place = vid[0:rows, 0:cols]
    c_1 = cv2.getTrackbarPos("Canny 1", window_name)
    c_2 = cv2.getTrackbarPos("Canny 2", window_name)

    filter(3)

    '''
    Vid_GBlur = cv2.GaussianBlur(vid, (7, 7),0) # smooth the Vid_Gray
    Vid_Gray = cv2.cvtColor(Vid_GBlur, cv2.COLOR_BGR2GRAY) # convert BGR to gray
    Vid_Canny = cv2.Canny(Vid_Gray, c_1, c_2) # find edges
    '''

    Filter = filter(3)

    '''
    thresh, mask = cv2.threshold(Filter, 240, 255, cv2.THRESH_BINARY)
    #Use Vid_Canny to make mask
    F_mask = cv2.bitwise_and(Filter, Filter, mask=mask)
    F_bgr = cv2.cvtColor(F_mask,cv2.COLOR_GRAY2BGR)
    Outline = cv2.add(vid, F_bgr) # mix video with filter
    #cv2.imshow("Camera", vid)
    '''
    Outline = frames(vid, Filter)
    cv2.imshow(window_name, Outline)

    key = cv2.waitKey(10) & 0XFF
    esc = 27

    if key == esc:
        break