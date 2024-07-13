

import cv2
import numpy as np

def get_masked(img, lower, upper):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_hsv, np.array(lower), np.array(upper))
    img_mask = cv2.bitwise_and(img, img, mask=mask)
    return img_mask

def get_processed(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (7, 7), 7)
    img_canny = cv2.Canny(img_blur, 50, 50)
    kernel = np.ones((7, 7))
    img_dilate = cv2.dilate(img_canny, kernel, iterations=2)
    img_erode = cv2.erode(img_dilate, kernel, iterations=2)
    return img_erode

def get_contours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return [cnt for cnt in contours if cv2.contourArea(cnt) > 500]

def get_centeroid(cnt):
    length = len(cnt)
    sum_x = np.sum(cnt[..., 0])
    sum_y = np.sum(cnt[..., 1])
    return int(sum_x / length), int(sum_y / length)

def get_pt_at_angle(pts, pt, ang):
    angles = np.rad2deg(np.arctan2(*(pt - pts).T))
    angles = np.where(angles < -90, angles + 450, angles + 90)
    found= np.rint(angles) == ang
    if np.any(found):
        return pts[found][0]
        
def get_distances(img, cnt1, cnt2, center, step):
    angles = dict()
    for angle in range(0, 360, step):
        pt1 = get_pt_at_angle(cnt1, center, angle)
        pt2 = get_pt_at_angle(cnt2, center, angle)
        if np.any(pt1) and np.any(pt2):
            d = round(np.linalg.norm(pt1 - pt2))
            cv2.putText(img, str(d), tuple(pt1), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 0))
            cv2.drawContours(img, np.array([[center, pt1]]), -1, (255, 0, 255), 1)
            angles[angle] = d
            
    return img, angles

img = cv2.imread("img/2.jpg")
img=cv2.resize(img,(640,480))


img_green = get_masked(img, [10, 0, 0], [70, 255, 255])
img_blue = get_masked(img, [70, 0, 0], [179, 255, 255])

img_green_processed = get_processed(img_green)
img_blue_processed = get_processed(img_blue)

img_green_contours = get_contours(img_green_processed)
img_blue_contours = get_contours(img_blue_processed)

for cnt_blue, cnt_green in zip(img_blue_contours, img_green_contours[::-1]):
    center = get_centeroid(cnt_blue)
    img, angles = get_distances(img, cnt_green.squeeze(), cnt_blue.squeeze(), center, 30)
    print(angles)

cv2.imshow("Image", img)
cv2.waitKey(0)
