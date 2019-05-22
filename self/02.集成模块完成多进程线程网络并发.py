"""
1. 使用方法
import socketserver
通过模块提供的不同的类的组合完成多进程或者多线程,tcp或者udp的网络并发模型
2. 常用类说明
TCPServer 创建tcp服务端套接字
UDPServer 创建udp服务端套接字
StreamRequestHandler 处理tcp客户端请求
DatagramRequestHandler 处理udp客户端请求
ForkingMixIn 创建多进程并发
ForkingTCPServer ForkingMixIn + TCPServer
ForkingUDPServer ForkingMixIn + UDPServer
ThreadingMixIn 创建多线程并发
ThreadingTCPServer ThreadingMixIn + TCPServer
ThreadingUDPServer ThreadingMixIn + UDPServer
3. 使用步骤
【1】 创建服务器类,通过选择继承的类,决定创建TCP或者UDP,多进程或者多线程的并发服务器
模型。
【2】 创建请求处理类,根据服务类型选择stream处理类还是Datagram处理类。重写handle方法,做
具体请求处理。
【3】 通过服务器类实例化对象,并绑定请求处理类。
【4】 通过服务器对象,调用serve_forever()启动服务

"""
import socketserver
