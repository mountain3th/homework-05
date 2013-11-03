# coding:utf-8
import socket
import time
from threading import Thread
import subprocess
import os
import copy
import simplejson as json
import sys


wait_for_clients_time = 15
game_gap = 1
game_times = 0
host = "0.0.0.0"
port = 23211
now_state = "wait"
all_user = {}
has_played = []
all_number = {}
all_data = []
now_order = {}
all_gold = []
set_times = 1000
game_type = 1
ban_list = []
connect_time = {}
ddos_threadhold = 1000


def handlechild(clientsock):
    global now_state, all_user, has_played, all_number, now_order, all_gold, connect_time, ban_list, game_times
    temp_times = game_times
    data = clientsock.recv(1024)
    temp_data = copy.deepcopy(data)
    method = temp_data.split(' ')[0]
    src = temp_data.split(' ')[1]
    if method == 'GET':
        response_body = json.dumps(dict(now_order, **{"goldpoint": all_gold}))
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
            if game_times != temp_times:
                temp_times = game_times
                connect_time[recv_data[1]] = 0
            if recv_data[1] in connect_time and temp_times != 0:
                connect_time[recv_data[1]] += 1
            if recv_data[1] in ban_list:
                break
            if recv_data[0] == 'check':
                if now_state == 'wait':
                    clientsock.sendall('wait')
                elif now_state == 'start':
                    if recv_data[1] in has_played:
                        clientsock.sendall('wait')
                    else:
                        has_played.append(recv_data[1])
                        if game_type == 1:
                            clientsock.sendall('start1')
                        else:
                            clientsock.sendall('start2')
            elif recv_data[0] == 'sign':
                if recv_data[1] in all_user:
                    clientsock.sendall('alreadyuse')
                else:
                    all_user[recv_data[1]] = recv_data[2]
                    connect_time[recv_data[1]] = 1
                    now_order[recv_data[1]] = 0
                    clientsock.sendall('success')
                #print all_user
            elif recv_data[0] == 'play':
                if game_type == 1:
                    all_number[recv_data[1]] = recv_data[3]
                else:
                    all_number[recv_data[1]] = [recv_data[3], recv_data[4]]
                clientsock.sendall('success')
            data = clientsock.recv(1024)
        print 'close %s connection.' % clientInfo
        clientsock.close()


def timer():
    global last_time, game_gap, game_times, now_state, has_played, all_number, set_times, all_gold, now_order, ddos_threadhold, connect_time, ban_list
    print "waiting for clients to connect......"
    time.sleep(wait_for_clients_time)
    last_time = int(time.time())
    has_played = []
    game_times = 1
    now_state = 'start'
    print "======================"
    print "start game : 1"
    while 1:
        for i in connect_time:
            if connect_time[i] > ddos_threadhold:
                ban_list.append(i)
        if int(time.time()) - last_time > game_gap:
            now_state = 'wait'
            print "stop game : " + str(game_times)
            print "now calculating......"
            temp_sum = 0
            if game_type == 1:
                for i in all_number:
                    temp_sum += int(all_number[i])
            else:
                for i in all_number:
                    temp_sum += int(all_number[i][0]) + int(all_number[i][1])
            all_gold.append(temp_sum / float(len(all_number)) * 0.618)
            print "gold point : " + str(temp_sum / float(len(all_number)) * 0.618)
            temp_gold = temp_sum / float(len(all_number)) * 0.618
            if game_type == 1:
                temp_sub = [[x, abs(int(all_number[x]) - temp_gold)] for x in all_number]
            else:
                temp_sub = [[x, min(abs(int(all_number[x][0]) - temp_gold), abs(int(all_number[x][1]) - temp_gold))] for x in all_number]
            temp_sub = sorted(temp_sub, key=lambda x: x[1])
            temp_first = temp_sub[0]
            temp_last = temp_sub[-1]
            for i in now_order:
                try:
                    temp_find = [j[1] for j in temp_sub if j[0] == i][0]
                    if temp_find == temp_first[1]:
                        now_order[i] += 10
                    elif temp_find == temp_last[1]:
                        now_order[i] += -1
                except:
                    now_order[i] += -5
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


if sys.argv[1] == '2':
    game_type = 2
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
