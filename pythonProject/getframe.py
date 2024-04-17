from grabscreen import *
import numpy as np
import time
import matplotlib.pyplot as plt
from getreward import *


window_region = (159,131,801,453)
# 截取四帧画面 (4, 84, 84)
def get4frame(isinitial):
    if isinitial:
        img_1 = cv2.imread('img_1.png')
        img_2 = cv2.imread('img_2.png')
        img_3 = cv2.imread('img_3.png')
        img_4 = cv2.imread('img_4.png')

        gray_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
        gray_1 = cv2.resize(gray_1, (84, 84))
        gray_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)
        gray_2 = cv2.resize(gray_2, (84, 84))
        gray_3 = cv2.cvtColor(img_3, cv2.COLOR_BGR2GRAY)
        gray_3 = cv2.resize(gray_3, (84, 84))
        gray_4 = cv2.cvtColor(img_4, cv2.COLOR_BGR2GRAY)
        gray_4 = cv2.resize(gray_4, (84, 84))
        state = np.stack([gray_1, gray_2, gray_3, gray_4], axis=0)
        return state

    else:
        img_1 = grab_screen(window_region)
        time.sleep(0.02)
        img_2 = grab_screen(window_region)
        time.sleep(0.02)
        img_3 = grab_screen(window_region)
        time.sleep(0.02)
        img_4 = grab_screen(window_region)
        gray_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
        gray_1 = cv2.resize(gray_1, (84, 84))
        gray_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)
        gray_2 = cv2.resize(gray_2, (84, 84))
        gray_3 = cv2.cvtColor(img_3, cv2.COLOR_BGR2GRAY)
        gray_3 = cv2.resize(gray_3, (84, 84))
        gray_4 = cv2.cvtColor(img_4, cv2.COLOR_BGR2GRAY)
        gray_4 = cv2.resize(gray_4, (84, 84))
        state = np.stack([gray_1, gray_2, gray_3, gray_4], axis=0)
        return state

if __name__ == "__main__":

    img_1 = cv2.imread('img_1.png')
    img_2 = cv2.imread('img_2.png')
    img_3 = cv2.imread('img_3.png')
    img_4 = cv2.imread('img_4.png')

    gray_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
    gray_1 = cv2.resize(gray_1, (84, 84))
    gray_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)
    gray_2 = cv2.resize(gray_2, (84, 84))
    gray_3 = cv2.cvtColor(img_3, cv2.COLOR_BGR2GRAY)
    gray_3 = cv2.resize(gray_3, (84, 84))
    gray_4 = cv2.cvtColor(img_4, cv2.COLOR_BGR2GRAY)
    gray_4 = cv2.resize(gray_4, (84, 84))

    plt.imshow(gray_1, plt.cm.gray)
    plt.show()
    state = np.stack([gray_1,gray_2,gray_3,gray_4], axis=0)
    print(state.shape)
