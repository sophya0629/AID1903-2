from socket import socket

sockfd=socket()
ADDR=('0.0.0.0',9999)
sockfd.connect(ADDR)
while True:
    try:
        data = input("输入:")
        sockfd.send(data.encode())
    except KeyboardInterrupt:
        print("退出服务")
        break
       
    msg=sockfd.recv(1024)
    print("msg",msg.decode())
    
sockfd.close()