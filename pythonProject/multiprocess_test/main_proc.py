import time
import multiprocessing
import socket
import struct
import math

fmt = '=I3d'

class Env(object):
    def __init__(self):
        self.reward = multiprocessing.Value('d', 0.0)
        self.s1 = multiprocessing.Value('d', 0.0)
        self.s2 = multiprocessing.Value('d', 0.0)
    def calangle(self, r_lon, r_lat, b_lon, b_lat):
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

    def udp_server(self):
        try:
            # 变量声明
            port = 12046
            r_data = [1e-4, 1e-4, 1e-4]
            b_data = [2e-5, 2e-5, 2e-5]
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 重复使用绑定信息
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            address = ("127.0.0.1", port)
            server_socket.bind(address)
            while True:
                receive_data, client_address = server_socket.recvfrom(4096)
                unpack_data = struct.unpack(fmt, receive_data)
                # 判断是否为我机id
                if unpack_data[0] == 1:
                    r_data = unpack_data[1:]
                else:
                    b_data = unpack_data[1:]

                self.s1.value = self.calangle(r_data[0], r_data[1], b_data[0], b_data[1])
                self.s2.value = r_data[2]
                temp_reward = -math.fabs(self.s1.value - self.s2.value)
                self.reward.value = temp_reward if temp_reward > -math.pi else -(math.pi*2+temp_reward)
                # print(self.reward.value)

        finally:
            server_socket.close()




if __name__ == "__main__":
    # 数据子线程
    env = Env()
    p1 = multiprocessing.Process(target=env.udp_server)
    p2 = multiprocessing.Process(target=env.udp_server)

    p1.start()
    p2.start()

    # 训练主线程
    while True:
        print(env.reward.value)


