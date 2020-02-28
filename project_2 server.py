"""
chat room
env:python3
socket and fork exercise
"""

from socket import  *
import os,sys

# 全局变量

ADDR=('0.0.0.0',8636)
user={}

def do_chat(s,name,content):
    msg='\n%s: %s'%(name,content)
    for i in user:
        if  i !=name:
            s.sendto(msg.encode(),user[i])


def do_login(s,name,addrs):
    if name in user:
        s.sendto(b'Fail',addrs)
    else:
        s.sendto(b'OK',addrs)

    #通知其他人
    msg ='\n欢迎 %s 进入聊天室'%name
    for i in user:
        s.sendto(msg.encode(),user[i])
    user[name]=addrs
    print(user)

def do_quit(s,name):
    msg='\n%s 退出聊天室'%name
    for i in user:
        if i!=name:
            s.sendto(msg.encode(),user[i])
        else:
            s.sendto(b'EXIT',ADDR)
            sys.exit()
    del user[name]
# 基本结构
def main():
    s =socket(AF_INET,SOCK_DGRAM)
    s.bind(ADDR)

    pid=os.fork()
    if pid<0:
        print('Erro')
    elif pid==0:
        while 1:
            content=input('管理员消息：')
            msg='C %s %s'%('管理员消息',content)
            s.sendto(msg.encode(),ADDR)
    else:
        while 1:
            data,addr=s.recvfrom(1024)
            print('接收到的请求：',data.decode())
            data=data.decode().split(' ',2)
            if data[0]=='L':
                do_login(s,data[1],addr)
            elif data[0]=='C':
                do_chat(s,data[1],data[2])
            elif data[0]=='Q':
                do_quit(s,data[1])
if  __name__ == '__main__':
    main()