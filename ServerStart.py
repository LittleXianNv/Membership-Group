import subprocess
import shlex
import os
from threading import Timer
import sys
from GatewayNode import GatewayNode
from MemberNode import *
from time import time
import setting

# GateWay node is public for all server
gate_ip = '52.14.170.52'

# Server initialization process
class ServerStart():
    
    def __init__(self):
        self.isGateNode = False

    # Create Gateway/normal node 
    def getCommand(self, argv):
        
        # Helper function to get server local ip address
        def get_local_ip():
            command1 = shlex.split("curl http://169.254.169.254/latest/meta-data/public-ipv4")
            process = subprocess.Popen(command1,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            return(stdout)
        
        arg = argv
        
        # Enter program as GateWay node 
        # arg[0] ServerStart.py
        # arg[1] g
        # arg[2] TCP_port_num
        # arg[3] UDP_port_num
        if len(arg) == 4 and 'g' in arg:
            # GateWay node Initialization
            gateNode = GatewayNode(gate_ip,arg[2],arg[3]) 
            # GateWay Node start running
            gateNode.startGateNode()

        # Enter program Normal server 
        # arg[0] ServerStart.py
        # arg[1] TCP_port_num
        # arg[2] UDP_port_num
        else:
            # Get server local ip address
            local_ip = get_local_ip().decode()
            # Normal node Initialization
            memberNode = MemberNode(gate_ip,local_ip,arg[1],arg[2])
            # Normal Node start running
            memberNode.startNormalNode()


# Program access point
if __name__ == '__main__':
    # Initialize the network structure 
    setting.init()

    # Server initialization by using user input argument
    s = ServerStart()
    argv = sys.argv
    s.getCommand(argv)