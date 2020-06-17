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

BeatWait = 0.5			# Set heartbeat sending frequency as 0.5 second

class GatewayNode(MemberNode):
	
	# GateWay Node initialization
	def __init__(self,gate_ip,TPort, UPort):
		self.local_ip = gate_ip
		self.pid = PID(gate_ip,time(),TPort, UPort)
		self.TPort = TPort
		self.UPort = UPort
		print('Gateway pid created: ' + self.pid.pid_str)

	# GateWay node running
	# Thread #1: Standard TCP response for Join/Delete request
	# Thread #2: TCP response only for initial join request(asking for membership list)
	# Thread #3: UDP Heartbeat receiving
	# Thread #4: UDP Heartbeat sending
	# Thread #5: User input to access node (Leaving/print memebrship list)
	def startGateNode(self):
		# Adding itself into membership list / ring structure
		setting.serverList.append(self.pid)
		setting.memberList[self.pid.pid_str] = self.pid
		setting.serverOrder[self.pid.pid_str] = 0
		print("Gateway node started")

		# Start Thread #1
		TCP_serv = TCPServer((self.local_ip, int(self.TPort)),TCP_Response)
		th = Thread(target = TCP_serv.serve_forever)
		th.daemon = True
		th.start()

		# Start Thread #2
		TCP_serv = TCPServer(('',20002),tcp_com)
		TCP_serv.serve_forever()
		
		# Start Thread #3
		hbserv=ThreadingUDPServer(('',int(self.UPort)),HBReceiver)
		Thread(target = hbserv.serve_forever).start()
		# Start Thread #4
		Thread(target = sendHB).start()

		# Start Thread #5
		Thread(target = UserChoice).start()


# Callback function: only for gateway node to deal with new join request by TCP
# Receive message: {"pid_str": joinNode's pid}
# Send message: {"membership": current membership list dictionary, "serverOrder": structure dictionary, 
# 					"index": new node's position in the network}
class tcp_com(BaseRequestHandler):

	def handle(self):
		msg_str = ""
		# Receive message, decode from byte into string, stop at "\n"
		while True:
			msg = self.request.recv(1024).decode()
			msg_str = msg_str + msg
			if '\n' in msg:
				break
		msg_str = msg_str.strip()
		# Deserialize message string into object
		msg_obj = json.loads(msg_str)
		print("GatewayNode log: request from "+ msg_obj["pid_str"])
		print(msg_str)
		# Increment the ring structure length by 1, assign the last position to new node
		setting.index += 1

		# Assemble the reply message, majorly send back the membership list 
		reply_structure = {"membership":setting.memberList, "serverOrder":setting.serverOrder, "index":setting.index}
		# Serialize the messsage 
		reply_str = json.dumps(reply_structure)+'\n'
		# Encode and send message
		self.request.sendall(reply_str.encode())




