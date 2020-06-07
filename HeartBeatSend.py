from time import time, ctime, sleep
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
from threading import Lock, Thread, Event

dest_ip = '3.136.11.181'
UDP_PORT = 20001
BeatWait = 0.5

s = socket(AF_INET, SOCK_DGRAM)
print("client sending to ip "+dest_ip)
while True:
    s.sendto('message', (dest_ip, UDP_PORT)
    print(ctime())
    sleep(BeatWait)
