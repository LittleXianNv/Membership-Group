class ListResolver():

    def __init__(self):
        self.memberList = {} #all the member servers with pid_str as key, pid as value
        self.serverList = [] # all the nodes with pid stored
        self.index=0
        self.serverOrder = {}
    
    def getIndex(serverList, pid):
        if pid in serverList:
            return serverList.index(pid)
        else:
            return None

    def getPredecessor(self, pid):
        res = []
        if len(self.serverList) <= 1:
            return []
        elif len(self.serverList) == 2:
            index = self.getIndex(self.serverList, pid)
            if (index-1) < 0:
                res.append(self.serverList[1].ip)
                return res
            else:
                res.append(self.serverList[0].ip)
                return res
        else:
            index = self.getIndex(self.serverList, pid)
            if (index-2) < 0 and (index-1) >= 0:
                num = len(serverList)
                res.append(self.serverList[num-2].ip)
                res.append(self.serverList[index-1].ip)
            elif index<2:
                num = len(serverList)
                res.append(self.serverList[num-2].ip)
                res.append(self.serverList[num-1].ip)
            else:
                res.append(self.serverList[index-2].ip)
                res.append(self.serverList[index-1].ip)
            return res
                
    
    def getSuccessor(self, pid):
        res = []
        if len(self.serverList) <= 1:
            return []
        elif len(self.serverList) == 2:
            index = self.getIndex(self.serverList, pid)
            if index+1 < len(self.serverList):
                res.append(self.serverList[1].ip)
                return res
            else:
                res.append(self.serverList[0].ip)
                return res
        else:
            index = self.getIndex(self.serverList, pid)
            num = len(serverList)
            if (index+2) < num:
                res.append(self.serverList[index+1].ip)
                res.append(self.serverList[index+2].ip)
            elif (index+2) == num:
                res.append(self.serverList[index+1].ip)
                res.append(self.serverList[0].ip)
            else:
                res.append(self.serverList[0].ip)
                res.append(self.serverList[1].ip)
            return res

    def addServer(self,pid):
        self.serverList.append(pid)

    def removeServer(self,pid):
        index = self.getIndex(self.serverList, pid)
        self.serverList.pop(index)