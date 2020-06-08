
#!/usr/bin/env python3

import socket
import json

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

data_set = {"key1": [1, 2, 3], "key2": [4, 5, 6]}
json_string = json.dumps(data_set)
print('Local print' + json_string)


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