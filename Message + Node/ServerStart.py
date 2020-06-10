import subprocess
import shlex
import os
from threading import Timer
import sys
from GatewayNode import GatewayNode
from MemberNode import PID, MemberNode
from time import time
gate_ip = #TODO get ip

class ServerStart():
    
    def __init__(self):
        self.serverList=[]
        self.isGateNode = False
        self.ipDict={} 

    
    def getCommand(self, argv):
        
        def get_local_ip():
            command1 = shlex.split("curl http://169.254.169.254/latest/meta-data/public-ipv4")
            process = subprocess.Popen(command1,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            
            stdout, stderr = process.communicate()
            return(stdout)
        
        arg = argv
        
        if len(arg) == 2 and 'g' in arg:
            # gatenode initialization
            
            print(gate_ip)
            isGateNode = True
            
            self.ipDict[gate_ip] = len(self.serverList)
            #self.serverList.append(pid)

            gateNode = GatewayNode(gate_ip) #parse
            gateNode.startGateNode()
#            restart = gateNode.startGateNode()
#            while restart:
#              restart = gateNode.startGateNode()

        else:
            # Normal server setup
            local_ip = get_local_ip()
            #self.ipDict[local_ip] = len(self.serverList)
            #self.serverList.append(pid)
            memberNode = MemberNode(gate_ip,local_ip)
            memberNode.startNormalNode()
#            self.ring.insert(memberNode)
#            restart = MemberNode.startNode()
#            while restart:
#              restart = MemberNode.startNode()

            
    


if __name__ == '__main__':
    s = ServerStart()
    argv = sys.argv
    s.getCommand(argv)
    #print(ServerStart.serverList)