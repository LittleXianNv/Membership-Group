import subprocess
import shlex
import os
import sys
from time import time, ctime, sleep
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
from threading import Lock, Thread, Event
import threading
#import SocketServer
#import daemon
UDP_PORT = 20001
HEARTBEAT_TIME_OUT = 2
BeatWait = 0.5
ipDict = {'18.191.220.124':0, '18.216.188.252':1}
serverList = ['18.191.220.124', '18.216.188.252']

class HeartBeatSend():
    def __init__(self,ipDict,serverList,local_ip):
        self.ipDict = ipDict
        self.serverList = serverList
		self.local_ip = local_ip
    
    def sendHB(self):
        
        def get_key(val):
            for key, value in self.ipDict.items():
                if val == value:
                    return key
                                
            return "key doesn't exist"
        
        
        index = self.ipDict[self.local_ip]
        if index+1 < len(serverList):
            dest_ip = get_key(index+1)
        else:
            dest_ip = get_key(index+1-len(serverList))

        s = socket(AF_INET, SOCK_DGRAM)
        print("client sending to ip "+dest_ip)
        while True:
            s.sendto('message', (dest_ip, UDP_PORT))
            print(time())
            sleep(BeatWait)


class HeartBeatDict():
	def __init__(self):
		self.HDict = {}
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
		self. HLock.release()

	def serverNoHeartbeat(self, HEARTBEAT_TIME_OUT):
		noResList = []
		when = time() - HEARTBEAT_TIME_OUT
		self.HLock.acquire()
		for key in self.HDict.keys():
			if self.HDict[key] <when:
				noResList.append(key)

		self. HLock.release()
		return noResList


class HBReceiver(Thread):
	def __init__(self, curEvent, updateDict, UDP_PORT):
		Thread.__init__(self)
		self.updateDict = updateDict
		self.curEvent = curEvent
		self.port = UDP_PORT
		self.recSocket = socket(AF_INET, SOCK_DGRAM)
		self.recSocket.bind(('', self.port))

	def __repr__(self):
		print("Heartbeat Server on port: %d\n" % self.port)

	def run(self):
		while self.curEvent.isSet():
			data, address = self.recSocket.recvfrom(6)
			print("reciving from "+ str(address))
			self.updateDict(address[0])


def recHeartBeat():
	curEvent = Event()
	curEvent.set()
	HeartBeatObj = HeartBeatDict()
	HBRecThread = HBReceiver(curEvent, HeartBeatObj.update, UDP_PORT)
	HBRecThread.start()
	print("server listening on port "+str(UDP_PORT))
	while True:
		try:
			print("Beat Dict")
			print(str(HeartBeatObj))
			noResList = HeartBeatObj.serverNoHeartbeat(HEARTBEAT_TIME_OUT)
			if noResList:
				print("silent")
				print(noResList)
			sleep(HEARTBEAT_TIME_OUT)
		except KeyboardInterrupt:
			print("Exit...")
			curEvent.clear()
			HBRecThread.join()

def call_to_send():
	print(ipDict)
    send = HeartBeatSend(ipDict,serverList)
    send.sendHB()

                     
if __name__ == '__main__':
    t1 = threading.Thread(target=recHeartBeat, args=())
    t2 = threading.Thread(target=call_to_send, args=())
	t1.start()
    t2.start()
	t1.join()
	t2.join()
