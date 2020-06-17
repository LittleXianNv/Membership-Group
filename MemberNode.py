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
# import SocketServer
# import daemon
import * from HeartBeat
HEARTBEAT_TIME_OUT = 2
MAX_SERVER_NUMBER = 8


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

class PID():
	def __init__(self, ip, timestamp,TPort, UPort):
		self.ip = ip
		self.TPort = TPort
		self.UPort = UPort
		self.pid_str = str(ip) + '_' + str(timestamp)



class MemberNode():
    
    def __init__(self,gatenode_ip,server_ip,TPort, UPort):
    	self.self_id = PID(str(server_ip),time(),TPort, UPort)
    	self.TPort = TPort
		self.UPort = UPort
    	self.gatenode_ip = gatenode_ip
    	#self.gatenode_id = PID(self.gatenode_ip,0)
    	print('Normal node pid created:' + self.self_id.pid_str)
    	print('GateNode ip = ' + self.gatenode_ip)
    	

    def startNormalNode(self):
    	print("Normal node started")
		# setup udp send 
		

		TCP_serv = TCPServer((self.local_ip, int(self.TPort)),TCP_Response)
		for i in range(MAX_SERVER_NUMBER):
			t = Thread(target = TCP_serv.serve_forever)
			t.daemon = True
			t.start()

		hbserv=ThreadingUDPServer(('',self.UPort),HBReceiver)
		Thread(target = hbserv.serve_forever).start()
		Thread(target = sendHB).start()
		Thread(target = UserChoice).start()

    	# Connect to gateNode using tcp, 
    	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	s.connect((self.gatenode_ip, 20002))
		list_request = json.dumps({"pid_str":self.self_id.pid_str})+'\n'
    	s.sendall(list_request.encode())
    	data = ""
		msg_str = ""
		while True:
			msg = s.recv(1024).decode()
			msg_str = msg_str + msg
			if '\n' in msg:
				break
		data = msg_str.strip()
    	# Get the membership list
    	print('Receive from server: ', repr(data))

		# Add to local list
		dataObj = json.loads(data)
		memberList = dataObj["membership"]
		serverOrder = dataObj["serverOrder"s]
		index = dataObj["index"]

		# Send Join msg to every nodes
		joinDict = {"type": messageType.Join.name,"pid_str":self.self_id.pid_str, "ip":self.self_id.ip, "TPort":self.self_id.TPort, "UPort":self.self_id.UPort, "index":index }
		join_msg = json.dumps(joinDict)+'\n'
		threads = []
		for key in memberList:
			t = Thread(target=sendJoinMsg, args=(memberList[key],join_msg))
			threads.append(t)
			t.start()
		
		for th in threads:
			th.join()
		s.sendall("Join finish \n".encode())
		s.close()
		setting.memberList[self.self_id.pid_str] = self.self_id
		setting.serverOrder[self.self_id.pid_str] = index
		setting.addServer(self.self_id)
		if len(setting.getPredecessor(self.self_id))>0:
			while True:
				Thread(target = HBD.serverNoHeartbeat, args=(HEARTBEAT_TIME_OUT,self_id)).start()

    	# Add to the ring network

    	#start runniing (recv/send heartbeat)
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
	
	

#    def runNode(self):


