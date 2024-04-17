import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:

    msg = input("请输入要发送的内容：")

    server_address = ("127.0.0.1", 9999)

    client_socket.sendto(msg.encode(), server_address)

    receive_data, server_address = client_socket.recvfrom(1024)

    print("recv server %s data:%s" % (server_address, receive_data.decode()))

    if (msg == 'exit'):
        break

client_socket.close()