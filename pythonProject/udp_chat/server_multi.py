import socket
import struct
import math
from multiprocessing import Process
import sys, os

fmt = '=I3d'
R_DATA = [2e-2,2e-2,2e-2]
B_DATA = [1e-2,1e-2,1e-2]
G_ANGLE = 0
def my_fun():
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
            # 判断是否为我机id
            if unpack_data[0] == 1:
                # 赋予全局变量
                global R_DATA
                R_DATA = unpack_data[1:]
            else:
                global B_DATA
                B_DATA = unpack_data[1:]

            G_ANGLE = calangle(R_DATA[0], R_DATA[1], B_DATA[0], B_DATA[1])
            delta = math.fabs(R_DATA[2] - G_ANGLE)
            print('delta:',delta)
            # server_socket.sendto(bytes("hello , if you want to exit the dialog,input quit please!".encode('utf-8')),
            #                      client_address, )
            # if (str(receive_data, 'utf8') == 'quit'):
            #    print('client exit')
            #     break
    finally:
        server_socket.close()


def calangle(r_lon,r_lat,b_lon,b_lat):
        if b_lat < r_lat:
            # 第三象限
            if b_lon <= r_lon:
                m_angle = math.atan((b_lon - r_lon) * math.cos(b_lat) / (
                        b_lat - r_lat)) - math.pi
            # 第四象限
            elif b_lon > r_lon:
                m_angle = math.pi + math.atan(
                    (b_lon - r_lon) * math.cos(b_lat) / (
                                b_lat - r_lat))

        else:
            # 一二象限
            m_angle = math.atan((b_lon - r_lon) * math.cos(b_lat) / (
                        b_lat - r_lat))
        return m_angle


def works(func1, arg, worknum):
    proc_record = []
    for i in range(worknum):
        p = Process(target=func1)
        p.start()
        proc_record.append(p)
    for p in proc_record:
        p.join()


if __name__ == '__main__':
    arg = 5
    procs = 2
    # procs = 4   #进程个数
    # works(timetask, arg, procs)
    works(my_fun, arg, procs)


