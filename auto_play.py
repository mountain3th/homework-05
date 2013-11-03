import os
import subprocess


all_user = []

file_object = open('all_user_data1.txt')
for i in file_object:
    all_user.append(i.strip().split(' '))
# p = subprocess.Popen('python goldserver.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for i in range(len(all_user)):
    p = subprocess.Popen('python goldclient.py %s %s' % (all_user[i][0], all_user[i][1]), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
