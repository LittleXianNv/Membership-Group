from time import time
import socket
from threading import Thread
import json

def convertJoinMsg(type, pid_str,ip,TPort,UPort,index):
    joinDict = {"type": type,"pid_str":pid_str, "ip":ip, "TPort":TPort, "UPort":UPort, "index":index }
	join_msg = json.dumps(joinDict)+'\n'
    return join_msg


def sendJoinMsg(pid, msg_str):
	if sendTCP(pid, msg_str) is None:
		pid_str = pid.pid_str
        try:
            del setting.memberList[pid_str]
            setting.removeServer(pid)
			print("join request failed")
        except:
            print(pid_str+" not in membership list")
            
        try:
            del serverOrder[pid_str]
        except:
            print(pid_str+" not in serverOrder")

def sendTCP(pid, msg_str):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect(pid.ip, pid.TPort)
		s.sendall(msg_str.encode())
		data = s.recv(1024).decode()
		return 1
	except:
		return None
	finally:
		s.close()