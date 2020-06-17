import subprocess
import shlex
import os
import sys
from time import time, ctime, sleep
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
from threading import Lock, Thread, Event
import threading
import * from setting 
HBD = HeartBeatDict()
import sendTCP from MemberNode
import setting
#import SocketServer
#import daemon

HEARTBEAT_TIME_OUT = 2
BeatWait = 0.5

def sendThread(s,port,ip,pid_str):
	pid_str_encoded = pid_str.encode()
	s.sendto(pid_str_encoded, (ip,port))
    print(time())

def sendHB(pid):
	successor_list = []
    successor_list=setting.getSuccessor(pid)

    s = socket(AF_INET, SOCK_DGRAM)
	while True:
		for ip in successor_list:
            t = threading.Thread(target=sendThread, args=(s,pid.UPort,ip,pid.pid_str))
			t.start()
		sleep(BeatWait)

    

class HeartBeatDict():
	def __init__(self):
		self.HDict = {} #key = pid_str, value = time()
		self.HLock = Lock()


	def __repr__(self):
		list = ''
		self.HLock.acquire()
		for key in self.HDict.keys():
			list = "IP address: "+key+" - Last time: "+ctime(self.HDict[key])
		self. HLock.release()
		return list

	def update(self, entry):
		self.HLock.acquire()
		self.HDict[entry] = time()
		self.HLock.release()

	def serverNoHeartbeat(self, HEARTBEAT_TIME_OUT,self_id):
		when = time() - HEARTBEAT_TIME_OUT
		self.HLock.acquire()
		for key in self.HDict.keys():
			if self.HDict[key] <when:
				print("die "+key)
				die_pid = setting.memberList[key]
				msg_structure = {"type": messageType.Delete.name,"pid_str":die_pid.pid_str, "ip":die_pid.ip, "index":index }
				msg_str = json.dumps(msg_structure)+'\n'
				for key in setting.memberList:
					if key != self_id.pid_str and key != die_pid.pid_str:
						Thread(target = sendTCP, args = (setting.memberList[key],msg_str))

		self. HLock.release()
	


class HBReceiver(BaseRequestHandler):
	def handel(self):
		msg, socket = self.request 
		pid_str = msg.decode().strip(s)
		HBD.update(pid_str)






