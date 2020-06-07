import subprocess
import shlex
import os
import sys
from time import time, ctime, sleep
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
from threading import Lock, Thread, Event
#import SocketServer
#import daemon
UDP_PORT = 20001
HEARTBEAT_TIME_OUT = 2

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


if __name__ == '__main__':
    recHeartBeat()
