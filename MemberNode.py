import subprocess
import shlex
import os
import sys
from time import time
import socket
import threading
# import SocketServer
# import daemon
# import HeartBeat
HEARTBEAT_TIME_OUT = 2
UDP_PORT = 20001
TCP_PORT = 65432

class PID():
	def __init__(self, ip, timestamp):
		self.ip = ip
		self.pid_str = str(ip) + '_' + str(timestamp)


class MemberNode():
    
    
#    self_id 
#    gatenode_id
#
#
    def __init__(self,gatenode_ip,server_ip):
    	self.self_id = PID(server_ip,time())
    	self.TCP_PORT = 65432
    	self.gatenode_ip = gatenode_ip
    	self.gatenode_id = PID(self.gatenode_ip,0)
    	print('Normal node pid created:' + self.self_id.pid_str)
    	print('GateNode ip = ' + self.gatenode_ip)
    	self.initMemberList()
    	self.memberList[self.gatenode_id.pid_str] = True
    	#print(self.memberList)


    def initMemberList(self):
    	self.memberList = {}
    	self.TCP_Buffer = {}

    def startNormalNode(self):
    	print("Normal node started")

    	# Connect to gateNode using TCP, 
    	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	s.connect((self.gatenode_ip, self.TCP_PORT))
    	s.sendall(b'Membership List Request')
    	data = s.recv(1024)
    	# Get the membership list
    	print('Receive from server: ', repr(data))

		
		s.close()
    	# Add to local list

    	# Send Join msg to designated nodes(3 predesessor + 3 successors)

    	# Add to the ring network

    	#start runniing (recv/send heartbeat)

#    def runNode(self):


