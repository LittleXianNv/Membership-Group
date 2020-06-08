import subprocess
import shlex
import os
from threading import Timer
import sys
from MemberNode import PID, MemberNode

import socket
import json
from threading import Lock, Thread, Event
from time import time, ctime, sleep
import threading
from enum import Enum


class messageType(Enum):
    Join = 1
    Leave = 2
    Failed = 3
    List = 4


class GatewayNode(MemberNode):
	HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
	PORT = 65432 
	def tcp_com(self):
	    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	        s.bind(('127.0.0.1', 65432))
	        s.listen()
	        conn, addr = s.accept()
	        with conn:
	            print('Connected by', addr)
	            while True:
	                data = conn.recv(1024)
	                print(data)
	                if not data:
	                    break
	                conn.sendall(data)
	                #conn.sendall(bytes(json_string,encoding="utf-8"))

	def __init__(self,gate_ip):
		self.pid = PID(gate_ip,time())
		print('Gateway pid created: ' + self.pid.pid_str)

	def startGateNode(self):
		print("Gateway node started")

		#Run TCP thread listening for join request
		message_dict = {"msgType": messageType.Join.name, "msgParam": [1, 2, 3], "msgContent": ["ip1", "ip2", "ip3"]}
		json_string = json.dumps(message_dict)

		print('Local print' + json_string)

		t1 = threading.Thread(target=self.tcp_com, args=())
		t1.start()
		while(1):
		    print('Main program running\n')
		    sleep(2)

		t1.join()








