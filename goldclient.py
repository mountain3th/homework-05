import socket
import time
import sys
import random


sleep_gap = 0.3
port = 23211
host = "192.168.1.101"


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.send('sign %s %s' % (sys.argv[1], sys.argv[2]))
if s.recv(1024).split(' ')[0] == 'alreadyuse':
    print "ERROR: Username has been used! Please change another one!"
    exit(0)
while 1:
    s.send('check %s %s' % (sys.argv[1], sys.argv[2]))
    recv_data = s.recv(1024).split(' ')
    if recv_data[0] == 'wait':
        print "wait"
        time.sleep(sleep_gap)
        continue
    elif recv_data[0] == 'start1':
        print "send my number"
        s.send('play %s %s %s' % (sys.argv[1], sys.argv[2], random.randint(0, 100)))
        s.recv(1024)
    elif recv_data[0] == 'start2':
        print "send my number"
        s.send('play %s %s %s %s' % (sys.argv[1], sys.argv[2], random.randint(0, 100), random.randint(0, 100)))
        s.recv(1024)
s.close()
