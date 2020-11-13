import cv2

# use webcam to catch image
Vid_cap = cv2.VideoCapture(0)
Vid_cap.set(3, 640)
Vid_cap.set(4, 480)
window_name = "outline_filter"

def empty(a):
    pass
def trackbar_set(window_name, bar1_name, bar2_name):
    cv2.namedWindow(window_name)
    cv2.resizeWindow(window_name, 640, 560)
    cv2.createTrackbar(bar1_name, window_name, 52, 255, empty)
    cv2.createTrackbar(bar2_name, window_name, 50, 255, empty)
    return bar1_name,bar2_name
def filter(mode_number):
    GBlur = cv2.GaussianBlur(vid, (7, 7), 0)  # smooth the Vid_Gray
    Gray = cv2.cvtColor(GBlur, cv2.COLOR_BGR2GRAY)  # convert BGR to gray
    Canny = cv2.Canny(Gray, c_1, c_2)  # find edges

    filter_list = [GBlur, Gray, Canny]
    mode_number = -1

    Filter = filter_list[mode_number]
    Outline = frames(vid, Filter)
    cv2.imshow(window_name, Outline)
    return Outline
def frames(vid, Filter):
    thresh, mask = cv2.threshold(Filter, 240, 255, cv2.THRESH_BINARY)
    # Use Vid_Canny to make mask
    F_mask = cv2.bitwise_and(Filter, Filter, mask=mask)
    F_bgr = cv2.cvtColor(F_mask, cv2.COLOR_GRAY2BGR)
    Outline = cv2.add(vid, F_bgr)  # mix video with filter
    return Outline
def save_img(path, img_name,img_type,  i):
    set_path = str(path+img_name+str(i)+"."+img_type)
    cv2.imwrite(set_path, filter(3))
    print(set_path, i)
'''
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
'''

trackbar = trackbar_set(window_name, "Canny 1", "Canny 2")
save_path = "./../picture/"
i = 0
while True:
    get, vid = Vid_cap.read()
    rows, cols, channels = vid.shape
    F_place = vid[0:rows, 0:cols]
    c_1 = cv2.getTrackbarPos(trackbar[0], window_name)
    c_2 = cv2.getTrackbarPos(trackbar[1], window_name)

    filter(3)
    key = cv2.waitKey(10) & 0XFF
    esc = 27
    if key == esc:
        break
    elif key == ord("r"):
        i = i + 1
        save_img(save_path,"picture","png",i)
        continue
    else:
        pass
Vid_cap.release()
cv2.destroyAllWindows()