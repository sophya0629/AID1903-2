"""
【1】 分为服务端和客户端,要求可以有多个客户端同时操作。
【2】 客户端可以查看服务器文件库中有什么文件。
【3】 客户端可以从文件库中下载文件到本地。
【4】 客户端可以上传一个本地文件到文件库。
【5】 使用print在客户端打印命令输入提示,引导操作
"""
from socket import *
from time import sleep
from threading import Thread
import os
import sys

class FtpServer:
    pass

def main():
    HOST='0.0.0.0'
    PORT=9999
    ADDR=(HOST,PORT)
    s=socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)
    
    while True:
        c, addr = s.accept()
        
    