# act as GateNode, listen for new node, provide/send current membership list


import socket
import json
from threading import Lock, Thread, Event
from time import time, ctime, sleep
import threading
from enum import Enum

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
class messageType(Enum):
    Join = 1
    Leave = 2
    Failed = 3
    List = 4

#membership_list = {"ip1" , "ip2", "ip3"}
message_dict = {"msgType": messageType.Join.name, "msgParam": [1, 2, 3], "msgContent": ["ip1", "ip2", "ip3"]}


json_string = json.dumps(message_dict)
print('Local print' + json_string)

def tcp_com():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                #conn.sendall(data)
                conn.sendall(bytes(json_string,encoding="utf-8"))

t1 = threading.Thread(target=tcp_com, args=())
t1.start()
while(1):
    print('AB\n')
    sleep(2)

t1.join()
