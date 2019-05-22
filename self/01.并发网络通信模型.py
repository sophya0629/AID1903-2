"""
1. 创建监听套接字
2. 等待接收客户端请求
3. 客户端连接创建新的进程处理客户端请求
4. 原进程继续等待其他客户端连接
5. 如果客户端退出,则销毁对应的进程

基于fork的多进程网络并发
重点代码
一般情况下用sys.exit()就行；os._exit()可以在os.fork()产生的子进程里使用。
"""
from socket import *
import os,sys
from signal import *

def handle(c):
    print("客户端:",c.getpeername())
    while True:
        data=c.recv(1024)
        if not data:
            break
        print(data.decode())
        msg=input("输入:")
        c.send(msg.encode())
    c.close()



# 创建监听套接字
HOST="0.0.0.0"
PORT=9999
ADDR=(HOST,PORT)

sockfd=socket()#tcp套接字
sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
sockfd.bind(ADDR)
sockfd.listen(3)

# 僵尸进程的处理
signal(SIGCHLD,SIG_IGN)
print("Listen the port 9999")
# 循环等待子进程
while True:
    try:
        connfd,addr=sockfd.accept()
    except KeyboardInterrupt:
        sys.exit("服务器退出")
    except Exception as e:
        print(e)
        continue

    # 创建子进程处理客户端请求
    pid=os.fork()
    if pid==0:
        sockfd.close() #子进程不需要监听,所以关闭sockfd
        handle(connfd) #具体处理客户请求
        os._exit(0)
    # 父进程实际只用来处理客户端连接
    else:
        connfd.close()  #父进程不需要与客户端通信所以关闭connfd
        pass
