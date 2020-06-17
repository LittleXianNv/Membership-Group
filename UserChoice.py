import os
import setting
import sendTCP from MemberNode

# User keyboard input to access node (Leaving/print memebrship list)
def UserChoice(pid_str):
    while True:
        res = input()
        # Leave the membership network
        if res is 'l':
            LeaveRequest(pid_str)
            os.exit(1)
        # Print the membership list on current node
        else res is 'p':
            for key in setting.memberList.keys():
                print(key)

# Send TCP message to rest of the nodes for leaving the network
# message: {"type": Delete, "pid_str": current node's pid}
def LeaveRequest(pid_str):
    msg_structure = {"type": messageType.Delete.name,"pid_str":pid_str}
	msg_str = json.dumps(msg_structure)+'\n'
    threads = []
    for key in setting.memberList:
		if key != pid_str:
			threads.append(Thread(target = sendTCP, args = (setting.memberList[key],msg_str)))
            threads[-1].start()
    
    for t in threads:
        t.join()
