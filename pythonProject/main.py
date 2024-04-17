from getreward import *
import socket
import struct
import multiprocessing
fmt = '=I3dI'

# calculate area, remove connected domains with small area
def Filter(contours):
    sum = 0
    a = []
    for i,area in enumerate(contours):
        if cv2.contourArea(area)>600:
            a.append(contours[i])
            sum+=1
    return sum, a


def udp_server(missle_count):
    try:
        # 变量声明
        PORT = 12046
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 重复使用绑定信息
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        address = ("127.0.0.1", PORT)
        server_socket.bind(address)
        while True:
            # print('server waiting')
            receive_data, client_address = server_socket.recvfrom(4096)
            unpack_data = struct.unpack(fmt, receive_data)
            # print("from:%s data:%s" % (client_address, unpack_data))
            # judge if it is red aircraft id
            if unpack_data[0] == 1:
                missle_count.value = unpack_data[4]
    finally:
        server_socket.close()



if __name__ == "__main__":
    # capture screen region
    # window_region = (384,87,1675,820)
    window_region = (159,131,801,453)

    last_time = time.time()
    missle_count = multiprocessing.Value('I', 0)
    p1 = multiprocessing.Process(target=udp_server,args=(missle_count,))
    p1.start()
    while (True):
        img = grab_screen(window_region)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        sum_r, contours_1_r = getRedN(hsv)
        sum_b, contours_1_b = getBlueN(hsv)

        contour_image = cv2.drawContours(img, contours_1_r, -1, (0, 255, 0), 2)
        contour_image = cv2.drawContours(img, contours_1_b, -1, (0, 0, 255), 3)
        cv2.imshow('window1', contour_image)

        print("red aircraft number：", sum_r, " ", "blue aircraft number：", sum_b)
        if missle_count.value != 0:
            print("missile hit prob：", (2-sum_b)/missle_count.value)

        print('loop took {} seconds'.format(time.time() - last_time))
        last_time = time.time()

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break


    cv2.waitKey()  # quit with by taping any key
    cv2.destroyAllWindows()


