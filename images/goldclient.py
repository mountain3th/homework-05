import socket
import time
import sys
import random


sleep_gap = 1
port = 23211
host = "localhost"


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.send('sign %s %s' % (sys.argv[1], sys.argv[2]))
s.recv(1024)
while 1:
    s.send('check %s %s' % (sys.argv[1], sys.argv[2]))
    recv_data = s.recv(1024).split(' ')
    if recv_data[0] == 'wait':
        print "wait"
        time.sleep(sleep_gap)
        continue
    elif recv_data[0] == 'start':
        print "send my number"
        s.send('play %s %s %s' % (sys.argv[1], sys.argv[2], random.randint(0, 100)))
        s.recv(1024)
s.close()
