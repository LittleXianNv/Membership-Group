from socketserver import BaseRequestHandler, ThreadingUDPServer
from MemberNode import PID
from time import time
from setting import *
from enum import Enum
import socket

class messageType(Enum):
    List = 1
    Join = 2
    Delete = 3

class TCP_Response(BaseRequestHandler):
    def handel(self):
        msg_str = ""
		while True:
			msg = socket.recv(1024).decode()
			msg_str = msg_str + msg
			if '\n' in msg:
				break
		msg_str = msg_str.strip()


        msg_obj = json.loads(msg_str)
        print(msg_str)
        msg_type = msg_obj["type"]
        
        if (msg_type == messageType.List.name):
		    print("GatewayHandler: request from "+ msg_obj["pid_str"])
		    print(msg_str)
		    setting.index += 1
		    reply_strcture = {"membership":setting.memberList, "serverOrder":setting.serverOrder, "index":setting.index}
		    reply_str = json.dumps(reply_strcture)+'\n'
		    self.request.sendall(reply_str.encode())
		    self.request.recv(1024)
            
        # Join request
        elif(msg_type == messageType.Join.name):
            pid_str = msg_obj["pid_str"]
            # update membership list
            setting.serverOrder[pid_str] = msg_obj["index"]
            pid = PID(msg_obj["ip"], time(), msg_obj["TPort"], msg_obj["UPort"])
            setting.memberList[pid_str] = pid
            setting.serverList.append(pid)
            print("serverlist: "+setting.serverList)
            # the origin last value
        
        elif(msg_type == messageType.Delete.name):
            pid_str = msg_obj["pid_str"]
            try:
                pid = setting.memberList[pid_str]
                del setting.memberList[pid_str]
                setting.removeServer(pid)
            except:
                print(pid_str+" not in membership list")
            
            try:
                del serverOrder[pid_str]
            except:
                print(pid_str+" not in serverOrder")

        else:
            print("invalid")

        self.request.sendall("ack\n".encode())



