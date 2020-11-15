import cv2
import numpy as np
# use webcam to catch image
Vid_cap = cv2.VideoCapture(0)
Vid_cap.set(3, 640)
Vid_cap.set(4, 480)
window_name = "outline_filter"

def empty(a):
    pass
def trackbar_set(window_name, bar1_name, bar2_name, bar3_name, bar4_name):
    cv2.namedWindow(window_name)
    #cv2.resizeWindow(window_name, 640, 160)
    cv2.createTrackbar(bar1_name, window_name, 52, 255, empty)
    cv2.createTrackbar(bar2_name, window_name, 50, 255, empty)
    cv2.createTrackbar(bar3_name, window_name, 50, 255, empty)
    cv2.createTrackbar(bar4_name, window_name, 4, 4, empty)
    return bar1_name,bar2_name, bar3_name, bar4_name
def filter(mode_number):
    Origin = vid
    GBlur = cv2.GaussianBlur(vid, (7, 7), 0)  # smooth the Vid_Gray
    B_Gray = cv2.cvtColor(GBlur, cv2.COLOR_BGR2GRAY)  # convert BGR to gray
    Canny = cv2.Canny(B_Gray, c_1, c_2)  # find edges

    Gray = cv2.cvtColor(vid, cv2.COLOR_BGRA2GRAY)

    sobel_x = cv2.Sobel(Gray, cv2.CV_64F, 1, 0)  # 利用捲積的方式描取X方向輪廓。
    sobel_y = cv2.Sobel(Gray, cv2.CV_64F, 0, 1)  # 利用捲積的方式描取Y方向輪廓。
    sobelx = np.uint8(np.absolute(sobel_x))  # 將sobel_x影像矩陣的數值加上絕對值。
    sobely = np.uint8(np.absolute(sobel_y))  # 將sobel_y影像矩陣的數值加上絕對值。
    Sobel = cv2.bitwise_or(sobelx, sobely)  # 聯集X方向和Y方向所取得的輪廓。

    filter_list1 = [Origin, GBlur, Gray, Canny, Sobel]
    filter_list2 = ["Origin", "GBlur", "Gray", "Canny", "Sobel"]

    Filter = filter_list1[mode_number]
    if mode_number == 3:
        Outline = mask_canny(vid, Filter, mode_number)
        cv2.imshow(window_name, Outline)
    elif mode_number == 4:
        Outline = mask_sobel(vid, Filter, mode_number)
        cv2.imshow(window_name, Outline)
    else:
        Outline = Filter
        cv2.imshow(window_name, Outline)
    return Outline, filter_list2[mode_number]
def mask_canny(vid, Filter, mode_number):
    thresh, mask = cv2.threshold(Filter, 240, 255, cv2.THRESH_BINARY)
    # Use Vid_Canny to make mask
    F_mask = cv2.bitwise_and(Filter, Filter, mask=mask)
    F_bgr = cv2.cvtColor(F_mask, cv2.COLOR_GRAY2BGR)
    Outline = cv2.add(vid, F_bgr)  # mix video with filter
    if mode_number == 3:
        return Outline
def mask_sobel(vid, Filter, mode_number):
        thresh, mask = cv2.threshold(Filter, s_1, 255, cv2.THRESH_BINARY)
        # Use Vid_Canny to make mask
        F_mask = cv2.bitwise_and(Filter, Filter, mask=mask)
        F_bgr = cv2.cvtColor(F_mask, cv2.COLOR_GRAY2BGR)
        Outline = cv2.add(vid, F_bgr)  # mix video with filter
        if mode_number == 4:
            return Outline

def save_img(path, img_name,img_type,filter_number, i):
    set_path = str(path+str(i)+"_"+filter(filter_number)[1]+"_"+img_name+"."+img_type)
    cv2.imwrite(set_path, filter(filter_number)[0])
    print(set_path, i)
trackbar = trackbar_set(window_name, "Canny 1", "Canny 2", "Sobel", "FilterMode")
save_path = "./../picture/"
i = 0
while True:
    get, vid = Vid_cap.read()
    rows, cols, channels = vid.shape
    F_place = vid[0:rows, 0:cols]
    c_1 = cv2.getTrackbarPos(trackbar[0], window_name)
    c_2 = cv2.getTrackbarPos(trackbar[1], window_name)
    s_1 = cv2.getTrackbarPos(trackbar[2], window_name)
    filter_number = cv2.getTrackbarPos(trackbar[3], window_name)
    filter(filter_number)
    key = cv2.waitKey(10) & 0XFF
    esc = 27
    if key == esc:
        break
    elif key == ord("r"):
        i = i + 1
        save_img(save_path,"picture","png", filter_number, i)
        continue
    else:
        pass
Vid_cap.release()
cv2.destroyAllWindows()