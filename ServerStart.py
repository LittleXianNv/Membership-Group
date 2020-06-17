import subprocess
import shlex
import os
from threading import Timer
import sys
from GatewayNode import GatewayNode
from MemberNode import *
from time import time
import setting
gate_ip = '52.14.170.52'


class ServerStart():
    
    def __init__(self):
        self.isGateNode = False

    
    def getCommand(self, argv):
        
        def get_local_ip():
            command1 = shlex.split("curl http://169.254.169.254/latest/meta-data/public-ipv4")
            process = subprocess.Popen(command1,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            
            stdout, stderr = process.communicate()
            return(stdout)
        
        arg = argv
        
        if len(arg) == 4 and 'g' in arg:
            # gatenode initialization
            gateNode = GatewayNode(gate_ip,arg[2],arg[3]) #parse
            gateNode.startGateNode()

        else:
            # Normal server setup
            local_ip = get_local_ip().decode()
            memberNode = MemberNode(gate_ip,local_ip,arg[1],arg[2])
            memberNode.startNormalNode()


            
    


if __name__ == '__main__':
    setting.init()
    s = ServerStart()
    argv = sys.argv
    s.getCommand(argv)