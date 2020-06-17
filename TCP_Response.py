from socketserver import BaseRequestHandler, ThreadingUDPServer
from MemberNode import PID
from time import time
from setting import *
from enum import Enum
import socket

# Standard TCP message has two type: Join request / Delete(Leave) notice
class messageType(Enum):
    Join = 1
    Delete = 2

# Reponse for standard TCP message received
class TCP_Response(BaseRequestHandler):

    def handel(self):
        # Receive TCP message, decode from byte into string, stop at "\n"
        msg_str = ""
		while True:
			msg = socket.recv(1024).decode()
			msg_str = msg_str + msg
			if '\n' in msg:
				break
		msg_str = msg_str.strip()

        # Deserialize TCP message string into object
        msg_obj = json.loads(msg_str)
        print(msg_str)
        msg_type = msg_obj["type"]
            
        # If the message is a Join request
        if(msg_type == messageType.Join.name):
            pid_str = msg_obj["pid_str"]

            # Creat join node's pid
            pid = PID(msg_obj["ip"], time(), msg_obj["TPort"], msg_obj["UPort"])
            
            # Adding one more position in ring structure
            setting.serverOrder[pid_str] = msg_obj["index"]
            
            # Update(Add) the pid into current node's own membership list
            setting.memberList[pid_str] = pid

            # Add the new node into serverList for further calculate predecessor & surcessor
            setting.serverList.append(pid)
            print("serverlist: "+setting.serverList)

        
        # If the message is Leave or delete request
        elif(msg_type == messageType.Delete.name):
            pid_str = msg_obj["pid_str"]
            try:
                # Delete node in memebership list
                pid = setting.memberList[pid_str]
                del setting.memberList[pid_str]
                # Remove node from server list
                setting.removeServer(pid)
            except:
                print(pid_str+" not in membership list")
            
            try:
                # Delete node in ring structure
                del serverOrder[pid_str]
            except:
                print(pid_str+" not in serverOrder")

        else:
            print("invalid message type")

        # Send Acknowledgment back to request node
        self.request.sendall("ack\n".encode())



