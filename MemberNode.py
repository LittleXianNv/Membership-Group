import subprocess
import shlex
import os
import sys
import time
import socket
import threading
import SocketServer
import daemon
import HeartBeat

class PID():
	def __init__(self, ip, timestamp):
		self.ip = ip
		self.pid_str = ip+"_"+timestamp


class MmberNode():
#    HEARTBEAT_TIME_OUT = 2
#    UDP_PORT = 20001
#    TCP_PORT = 10000
#    self_id 
#    gatenode_id
#
#
#    def __init__(self,gatenode_ip,server_ip):
#        self.initMemberList()
#        self.self_id = PID(server_ip, time.time())
#        print("[MAIN] [INFO] [" + time.time() + "] : node created with id : " + self_id.pid_str)
#        self.gatenode_id = PID(gatenode_ip,0)
#        self.memberList[gatenode_id.pid_str] = True
#        print("[MAIN] [MEM_ADD] ["+time.time()+"] : "+gatenode_id.pid_str)
#
#
#
#
#    def startNode(self):
#        # Create a TCP/IP socket
#        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        # Bind the socket to the port
#        server_address = ('localhost', 10000)
#
#        return self.runNode()
#        
#
#    def initMemberList(self):
#        memberList = {}
#        TCP_Buffer = {}
#        gatenode_id = PID("",0)
#        #GateNode_Boolean = false
#
#
#    def runNode(self):

