"""
ftp文件服务器_客户端

1. 功能
【1】 分为服务端和客户端,要求可以有多个客户端同时操作。
【2】 客户端可以查看服务器文件库中有什么文件。
【3】 客户端可以从文件库中下载文件到本地。
【4】 客户端可以上传一个本地文件到文件库。
【5】 使用print在客户端打印命令输入提示,引导操作

"""

from socket import *
from threading import Thread
import sys
from time import sleep

ADDR = ('0.0.0.0', 9999)


# 具体功能
class FtpClient:
    def __init__(self, s):
        self.s = s

    def do_list(self):
        self.s.send(b'L')  # 发送请求
        # 等待回复
        data = self.s.recv(1024).decode()
        # ok表示请求成功
        if data == 'OK':
            print("请求成功")
            data = self.s.recv(4096)
            # while True:
            #     data=self.s.recv(4096)
            #     if data==b'##':
            #         break
            print(data.decode())
        else:
            print(data)

    def do_quit(self):
        self.s.send(b'Q')
        self.s.close()
        sys.exit("谢谢使用")

    def do_download(self, filename):
        self.s.send(b'G ' + filename.encode())
        # 等待回复
        data = self.s.recv(128).decode()
        if data == 'OK':
            fd = open(filename, 'wb')
            # 接收内容，写入文件
            while True:
                data = self.s.recv(1024)
                if data == b'##':
                    break
                fd.write(data)
            fd.close()
        else:
            print(data)

    def do_upload(self, filename):
        try:
            fd = open(filename, 'rb')
        except Exception:
            print("没有该文件")
            return
            # 发送请求
        filename = filename.split('/')[-1]
        self.s.send(b'P ' + filename.encode())
        # 等待回复
        data = self.s.recv(1024).decode()
        if data == 'OK':
            while True:
                data = fd.read(1024)
                if not data:
                    sleep(0.1)
                    self.s.send(b"##")
                    return
                self.s.send(data)
            fd.close()
        else:
            print(data)


# 发起请求
def request(s):
    # 创建实例化对象处理文件
    ftp = FtpClient(s)
    while True:
        try:
            print('\n=========命令选项==========')
            print('**********list************')
            print('********get file**********')
            print('********put file**********')
            print('**********quit************')
            print('=========命令选项==========')

            cmd = input("输入命令:")
            if cmd.strip() == 'list':
                # s.send(cmd.encode())
                ftp.do_list()
            elif cmd[:3] == 'get':
                filename = cmd.strip().split(' ')[-1]
                ftp.do_download(filename)
            elif cmd[:3] == 'put':
                filename = cmd.strip().split(' ')[-1]
                ftp.do_upload(filename)
            elif cmd.strip() == 'quit':
                ftp.do_quit()
        except KeyboardInterrupt:
            sys.exit("退出服务")


# 网络链接
def main():
    s = socket()

    while True:
        try:
            s.connect(ADDR)
        except KeyboardInterrupt:
            sys.exit("退出服务")
        except Exception as e:
            print("链接服务器失败")
            return
        else:
            print("""********************************
 DATA   FILE   IMAGE
********************************
            """)
        cls = input("输入文件种类:")
        if cls not in ['DATA', 'FILE', 'IMAGE']:
            print("Sorry input error")
            return
        else:
            s.send(cls.encode())
            request(s)
        msg = s.recv(1024)
        print("msg", msg.decode())
    s.close()


if __name__ == '__main__':
    main()
