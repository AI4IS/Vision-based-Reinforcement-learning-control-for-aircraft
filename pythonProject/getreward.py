from grabscreen import *
import numpy as np
import time

# 计算面积，去除面积小的连通域
def Filter(contours):
    sum = 0
    a = []
    for i,area in enumerate(contours):
        if cv2.contourArea(area)>100:
            a.append(contours[i])
            sum+=1
    return sum, a

def getRedN(hsv):
    # 红机掩码
    lower_r = np.array([0, 234, 228])  # 2 239 233
    upper_r = np.array([7, 244, 238])

    mask_r = cv2.inRange(hsv, lower_r, upper_r)
    kernel = np.ones((5, 5), np.uint8)

    # 闭运算，消除数字孔洞
    cvclose_r = cv2.morphologyEx(mask_r, cv2.MORPH_CLOSE, kernel)

    # 查找轮廓
    contours_r, hierarchy_r = cv2.findContours(cvclose_r, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 绘制轮廓
    sum_r, contours_1_r = Filter(contours_r)
    return sum_r, contours_1_r


def getBlueN(hsv):
    # 蓝机掩码
    lower_b = np.array([118, 208, 195])
    upper_b = np.array([128, 218, 205])

    mask_b = cv2.inRange(hsv, lower_b, upper_b)
    kernel = np.ones((5, 5), np.uint8)

    # 闭运算，消除数字孔洞
    cvclose_b = cv2.morphologyEx(mask_b, cv2.MORPH_CLOSE, kernel)

    # 查找轮廓
    contours_b, hierarchy_b = cv2.findContours(cvclose_b, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 绘制轮廓

    sum_b, contours_1_b = Filter(contours_b)
    return sum_b, contours_1_b

if __name__ == "__main__":
    # 截取屏幕区域
    window_region = (384,87,1675,820)
    # 程序计时
    last_time = time.time()

    while (True):
        img = grab_screen(window_region)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        sum_r, _ = getRedN(hsv)
        sum_b, _ = getBlueN(hsv)

        # contour_image = cv2.drawContours(img.copy(), contours_1_r, -1, (0, 255, 0), 2)
        # contour_image = cv2.drawContours(img.copy(), contours_1_b, -1, (0, 0, 255), 3)

        print("我机数量：", sum_r, " ", "敌机数量：", sum_b)

        # 测试时间用
        print('loop took {} seconds'.format(time.time() - last_time))
        last_time = time.time()

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

