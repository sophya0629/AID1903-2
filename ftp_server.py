"""
ftp文件服务器_服务器端
1. 功能
【1】 分为服务端和客户端,要求可以有多个客户端同时操作。
【2】 客户端可以查看服务器文件库中有什么文件。
【3】 客户端可以从文件库中下载文件到本地。
【4】 客户端可以上传一个本地文件到文件库。
【5】 使用print在客户端打印命令输入提示,引导操作
1技术点分析:
 并发模型 多线程并发模式
 数据传输 tcp传输
2结构设计
 客户端发起请求,打印请求提示界面
 文件传输功能,封装为类
3功能
    网络搭建
    查看文件库信息
    下载文件
    上传文件
    客户端退出
4协议
L   表示请求文件列表
Q   表示退出
G   表示下载
P   表示上传

"""
from socket import *
from threading import Thread
import sys
import os
from time import sleep
# 全局变量
HOST = '0.0.0.0'
PORT = 9999
ADDR = ('0.0.0.0', 9999)
FTP = '/home/tarena/PythonNet/day11/FTP/'


# 将服务端请求功能封装为类
class FtpServer:
    def __init__(self, c, path):
        self.c = c
        self.path = path

    def do_list(self):
        # 获取文件列表
        files = os.listdir(self.path)
        if not files:
            self.c.send("该文件类别列表为空".encode())
            return
        else:
            self.c.send(b"OK")
            sleep(0.1)
        f=''
        for file in files:
            if file[0] != '.' and os.path.isfile(self.path+file):
                f+=file+'\n'
        self.c.send(f.encode())
        self.c.send(b'##')
        
    def do_download(self,filename):
        try:
            f=open(self.path+filename,'rb')
        except Exception:
            self.c.send("文件不存在".encode())
            return 
        else:
            self.c.send(b"OK")
            sleep(0.1)
        # 发送文件内容
        while True:
            data=f.read(1024)
            if not data:
                sleep(0.1)
                self.c.send(b'##')
                return 
            self.c.send(data)
    
    def do_upload(self,filename):
        if os.path.exists(self.path+filename):
            self.c.send("该文件已经存在".encode())
            return
        self.c.send(b'OK')
        fd = open(self.path + filename, 'wb')
        # 接收文件
        while True:
            data=self.c.recv(1024)
            if data==b'##':
                return
            fd.write(data)
        fd.close()

    
def handle(c):
    cls = c.recv(1024).decode()
    FTP_PATH = FTP + cls + '/'
    ftp = FtpServer(c, FTP_PATH)
    print("Connect from", c.getpeername())
    while True:
        data = c.recv(1024).decode()
        if not data or data[0]=='Q':
            return 
        elif data[0] == 'L':
            ftp.do_list()
        # filename=input("请输入上传文件名称:")
        # f=open(filename,'wb')
        # c.send(b'ok')
        elif data[0]=='G' :
            filename=data.split(' ')[-1]
            ftp.do_download(filename)
        elif data[0]=='P':
            filename = data.split(' ')[-1]
            ftp.do_upload(filename)
    # c.close()


# 网络搭建
def main():
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)
    print("listen the port %d" % PORT)
    while True:
        try:
            c, addr = s.accept()
        except KeyboardInterrupt:
            sys.exit("退出服务")
        except Exception as e:
            print(e)
            continue
        print("连接的客户端:", addr)
        # 创建线程处理请求
        client = Thread(target=handle, args=(c,))
        client.setDaemon(True)
        client.start()


if __name__ == '__main__':
    main()
