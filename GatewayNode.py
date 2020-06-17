import subprocess
import shlex
import os
from threading import Timer
import sys
from MemberNode import PID, MemberNode
from socketserver import BaseRequestHandler, ThreadingUDPServer, TCPServer
import socket
import json
from threading import Lock, Thread, Event
from time import time, ctime, sleep
import threading
from enum import Enum
from setting import *
from TCP_Response import TCP_Response, messageType
import * from HeartBeat
import * from UserChoice
MAX_SERVER_NUMBER = 8
BeatWait = 0.5



class tcp_com(BaseRequestHandler):
	def handle(self):
		msg_str = ""
		while True:
			msg = self.request.recv(1024).decode()
			msg_str = msg_str + msg
			if '\n' in msg:
				break
		msg_str = msg_str.strip()
		msg_obj = json.loads(msg_str)
		print("GatewayHandler: request from "+ msg_obj["pid_str"])
		print(msg_str)
		setting.index += 1
		reply_structure = {"membership":setting.memberList, "serverOrder":setting.serverOrder, "index":setting.index}
		reply_str = json.dumps(reply_structure)+'\n'
		self.request.sendall(reply_str.encode())
		self.request.recv(1024)

class GatewayNode(MemberNode):
	
	def __init__(self,gate_ip,TPort, UPort):
		self.local_ip = gate_ip
		self.pid = PID(gate_ip,time(),TPort, UPort)
		self.TPort = TPort
		self.UPort = UPort
		print('Gateway pid created: ' + self.pid.pid_str)

	def startGateNode(self):
		setting.serverList.append(self.pid)
		setting.memberList[self.pid.pid_str] = self.pid
		setting.serverOrder[self.pid.pid_str] = 0
		print("Gateway node started")

		TCP_serv = TCPServer((self.local_ip, int(self.TPort)),TCP_Response)
		for i in range(MAX_SERVER_NUMBER):
			t = Thread(target = TCP_serv.serve_forever)
			t.daemon = True
			t.start()

		TCP_serv = TCPServer(('',20002),tcp_com)
		TCP_serv.serve_forever()
		hbserv=ThreadingUDPServer(('',int(self.UPort)),HBReceiver)
		Thread(target = hbserv.serve_forever).start()
		Thread(target = sendHB).start()
		Thread(target = UserChoice).start()

		# t1 = threading.Thread(target=self.tcp_com, args=())
		# t1.start()
		# while(1):
		#     print('Main program running\n')
		#     sleep(2)

		# t1.join()








