import subprocess
import shlex
import os
from threading import Timer
import sys
from MemberNode import PID, MemberNode
from socketserver import BaseRequestHandler, ThreadingUDPServer
import socket
import json
from threading import Lock, Thread, Event
from time import time, ctime, sleep
import threading
from enum import Enum
import TCP_Response
import * from HeartBeat
import * from UserChoice
MAX_SERVER_NUMBER = 8
BeatWait = 0.5

class messageType(Enum):
	List = 1
    Join = 2
    Delete = 3

# class tcp_com(BaseRequestHandler):
# 	def handle(self):
# 		msg_str = ""
# 		while True:
# 			msg = socket.recv(1024).decode()
# 			msg_str = msg_str + msg
# 			if '\n' in msg:
# 				break
# 		msg_str = msg_str.strip()
# 		msg_obj = json.loads(msg_str)
# 		print("GatewayHandler: request from "+ msg_obj["rid"])
# 		print(msg_str)
# 		setting.index += 1
# 		reply_strcture = {"membership":setting.memberList, "serverOrder":setting.serverOrder, "index":setting.index}
# 		reply_str = json.dumps(reply_strcture)+'\n'
# 		self.request.sendall(reply_str.encode())
# 		self.request.recv(1024)

class GatewayNode(MemberNode):
	
	def __init__(self,gate_ip,TPort, UPort):
		self.local_ip = gate_ip
		self.pid = PID(gate_ip,time(),TPort, UPort)
		self.TPort = TPort
		self.UPort = UPort
		print('Gateway pid created: ' + self.pid.pid_str)

	def startGateNode(self):
		setting.serverList.append(pid)
		setting.memberList[self.pid.pid_str] = self.pid
		setting.serverOrder[self.pid.pid_str] = 0
		print("Gateway node started")

		#Run TCP thread listening for join request
		#message_dict = {"msgType": messageType.Join.name, "msgParam": [1, 2, 3], "msgContent": ["ip1", "ip2", "ip3"]}
		#json_string = json.dumps(message_dict)

		TCP_serv = TCPServer((self.local_ip, TPort),TCP_Response)
		for i in range(MAX_SERVER_NUMBER):
			t = Thread(target = TCP_serv.serve_forever)
			t.daemon = True
			t.start()

		hbserv=ThreadingUDPServer(('',self.UPort),HBReceiver)
		Thread(target = hbserv.serve_forever).start()
		Thread(target = sendHB).start()
		Thread(target = UserChoice).start()

		# t1 = threading.Thread(target=self.tcp_com, args=())
		# t1.start()
		# while(1):
		#     print('Main program running\n')
		#     sleep(2)

		# t1.join()








