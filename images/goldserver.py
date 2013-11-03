# coding:utf-8
import socket
import time
from threading import Thread
import subprocess
import os
import copy
import simplejson as json


wait_for_clients_time = 5
game_gap = 3
game_times = 1
host = ""
port = 23211
now_state = "wait"
all_user = {}
has_played = []
all_number = {}
all_data = []
set_times = 10


def handlechild(clientsock):
    global now_state, all_user, has_played, all_number
    data = clientsock.recv(1024)
    temp_data = copy.deepcopy(data)
    method = temp_data.split(' ')[0]
    src = temp_data.split(' ')[1]
    if method == 'GET':
        response_body = json.dumps(all_data)
        response_body_raw = ''.join(response_body)
        response_headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'X-Request, X-Requested-With',
            'Content-type': 'application/json',
            'Content-Length': len(response_body_raw),
            'Connection': 'close',
        }
        response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.iteritems())
        response_proto = 'HTTP/1.1'
        response_status = '200'
        response_status_text = 'OK'  # this can be random
        clientsock.send('%s %s %s' % (response_proto, response_status, response_status_text))
        clientsock.send(response_headers_raw)
        clientsock.send('\n')  # to separate headers from body
        clientsock.send(response_body_raw)
        clientsock.close()
    else:
        clientInfo = str(clientsock.getpeername())
        print "Got connection from %s" % clientInfo
        print game_times
        while 1:
            if not len(data):
                break
            recv_data = data.split(' ')
            if recv_data[0] == 'check':
                if now_state == 'wait':
                    clientsock.sendall('wait')
                elif now_state == 'start':
                    if recv_data[1] in has_played:
                        clientsock.sendall('wait')
                    else:
                        has_played.append(recv_data[1])
                        clientsock.sendall('start')
            elif recv_data[0] == 'sign':
                all_user[recv_data[1]] = recv_data[2]
                clientsock.sendall('success')
                print all_user
            elif recv_data[0] == 'play':
                all_number[recv_data[1]] = recv_data[3]
                clientsock.sendall('success')
            data = clientsock.recv(1024)
        print 'close %s connection.' % clientInfo
        clientsock.close()


def timer():
    global last_time, game_gap, game_times, now_state, has_played, all_number, set_times
    print "waiting for clients to connect......"
    time.sleep(wait_for_clients_time)
    last_time = int(time.time())
    has_played = []
    now_state = 'start'
    print "======================"
    print "start game : 1"
    while 1:
        if int(time.time()) - last_time > game_gap:
            now_state = 'wait'
            print "stop game : " + str(game_times)
            print "now calculating......"
            temp_sum = 0
            for i in all_number:
                temp_sum += int(all_number[i])
            print temp_sum / float(len(all_number)) * 0.618
            all_number['goldpoint'] = temp_sum / float(len(all_number)) * 0.618
            all_data.append(all_number)
            '''file_object = open('results.txt', 'w')
            for i in all_data:
                file_object.writelines(str(i) + '\n')
            file_object.close()'''
            print "stop calculating"
            game_times += 1
            if game_times > set_times:
                file_object = open('results.txt', 'w')
                for i in all_data:
                    file_object.writelines(str(i) + '\n')
                file_object.close()
                for i in subprocess.Popen('lsof -i:23211', stdout=subprocess.PIPE, shell=True).stdout.readlines():
                    if 'LISTEN' in i.strip().split(' ')[-1]:
                        os.system('kill -9 %s' % i.strip().split(' ')[2])
            has_played = []
            all_number = {}
            print "======================"
            print "start game : " + str(game_times)
            last_time = int(time.time())
            now_state = 'start'


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen(1)
t = Thread(target=timer)
t.setDaemon(1)
t.start()


while 1:
    try:
        clientsock, clientaddr = sock.accept()
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        continue

    t = Thread(target=handlechild, args=[clientsock])
    t.setDaemon(1)
    t.start()
