import subprocess
import shlex
import os
import sys
from time import time
import socket
from threading import Thread
from socketserver import BaseRequestHandler, ThreadingUDPServer, TCPServer
from enum import Enum
import json
from TCP_Response import TCP_Response,messageType
from SendJoinRequest import convertJoinMsg, sendJoinMsg, sendTCP
# import SocketServer
# import daemon
import * from HeartBeat
HEARTBEAT_TIME_OUT = 2

# PID structure for each node, include IP address/TCP port/UDP port/pid (ip+Time stamp)
class PID():
	def __init__(self, ip, timestamp,TPort, UPort):
		self.ip = ip
		self.TPort = TPort
		self.UPort = UPort
		self.pid_str = str(ip) + '_' + str(timestamp)


class MemberNode():
    
    # Normal Node initialization
    def __init__(self,gatenode_ip,server_ip,TPort, UPort):
    	self.self_id = PID(str(server_ip),time(),TPort, UPort)
    	self.TPort = TPort
		self.UPort = UPort
    	self.gatenode_ip = gatenode_ip
    	print('Normal node pid created:' + self.self_id.pid_str)
    	print('GateNode ip = ' + self.gatenode_ip)
    	
    # Normal Node running
    # Thread #1: Standard TCP response for Join/Delete request
	# Thread #2: UDP Heartbeat receiving
	# Thread #3: UDP Heartbeat sending
	# Thread #4: User input to access node (Leaving/print memebrship list)
	# Thread #5: Detecting if any predecessor node fail
    def startNormalNode(self):
    	print("Normal node started")

		# Start Thread #1
		TCP_serv = TCPServer((self.local_ip, int(self.TPort)),TCP_Response)
		t = Thread(target = TCP_serv.serve_forever)
		t.daemon = True
		t.start()

    	# Connect to GateWay Node using TCP
    	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	s.connect((self.gatenode_ip, 20002))
		list_request = json.dumps({"pid_str":self.self_id.pid_str})+'\n'
    	s.sendall(list_request.encode())
    	# Receive the TCP message from GateWay Node
    	data = ""
		msg_str = ""
		while True:
			msg = s.recv(1024).decode()
			msg_str = msg_str + msg
			if '\n' in msg:
				break
		data = msg_str.strip()
    	print('Receive from server: ', repr(data))

		# Get the membership list
		dataObj = json.loads(data)
		# Add the receive membership info into its own membership list
		memberList = dataObj["membership"]
		# Get the ring structure
		serverOrder = dataObj["serverOrder"]
		# Get the last position in ring structure
		index = dataObj["index"]

		# Send Join message to every other nodes
		join_msg = convertJoinMsg(messageType.Join.name, self.self_id.pid_str, self.self_id.ip, self.self_id.TPort, self.self_id.UPort, index)
		threads = []
		for key in memberList:
			t = Thread(target = sendJoinMsg, args = (memberList[key], join_msg))
			threads.append(t)
			t.start()
		for th in threads:
			th.join()

		# Join finish, close connection with GateWay Node
		s.close()

		# Adding itself into the membership list and ring structure
		setting.memberList[self.self_id.pid_str] = self.self_id
		setting.serverOrder[self.self_id.pid_str] = index
		# Append itself to the severList for predecessor/successor calculation later
		setting.addServer(self.self_id)

		# Start Thread #2 (UDP receving)
		hbserv=ThreadingUDPServer(('',self.UPort),HBReceiver)
		Thread(target = hbserv.serve_forever).start()
		# Start Thread #3 (UDP sending)
		Thread(target = sendHB).start()
		# Start Thread #4 User input to access node (Leaving/print memebrship list)
		Thread(target = UserChoice).start()

		# StartThread #5 (Detecting if any predecessor node fail)
		if len(setting.getPredecessor(self.self_id))>0:
			while True:
				Thread(target = HBD.serverNoHeartbeat, args=(HEARTBEAT_TIME_OUT,self_id)).start()

    	