# Matej Bellus
# 
# Custom protocol header
# 
# 2 bytes - Conversation ID
# 2 bytes - Fragment number
# 2 bytes - Total fragments

import sys
import socket
import math
import threading
from struct import *
from random import randint
from time import sleep

max_maxl 	 = 65507
default_ip   = "192.168.1.3"
default_port = 5005
default_maxl = 5

hdr_len 	 = 6
hdr_format   = '!HHH'

conversations = {}



def get_hdr(data):
	my_hdr = unpack(hdr_format, data[0:hdr_len])
	return my_hdr

def get_conversation(id):
	s = ''
	for key, value in conversations[id].iteritems():
		s += value
	return s

def parse_packet(data):
	hdr   = get_hdr(data)
	c_id  = hdr[0]
	f_nm  = hdr[1]
	total = hdr[2]

	if not conversations.has_key(c_id):
		conversations[c_id] = {}
		pass
	conversations[c_id][f_nm] = data[hdr_len:len(data)]

	if len(conversations[c_id]) == total:
		print '\n[Deamon] Compleate message ('+str(total)+' fragments): \n' + get_conversation(c_id) + '\n'
	pass

def recieve_data(ip, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((ip, port))

	print "[Deamon] Listening daemon started on "+ip+":"+str(port)
	while True:
		data, addr = sock.recvfrom(max_maxl) # buffer size is 1024 bytes
		print '[Deamon] got smthng...'
		parse_packet(data)

	pass


def send_data():
	global default_ip
	global default_port
	global default_maxl

	ip = default_ip
	port =default_port
	maxl = default_maxl

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


	if maxl > 65507:
		print 'Max value is ' + str(max_maxl) + ', using that number!'
		maxl = max_maxl
		pass
	msg  = raw_input('Message: ');
	fragments = int(math.ceil( float(len(msg)) / float(maxl) ))

	# print "Sendint to: ", ip, ":", port
	# print "MAX : ", maxl
	# print "N. of fragments", fragments

	print 'Sending to ' + ip + ":" + str(port) + " as " + str(fragments) + " fragments"
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	c_id = randint(0, 65000)
	for x in range(0, fragments):
		# print 'Sending fragment ' + str(x)
		f = pack(hdr_format, c_id, x, fragments)
		f += msg[x*maxl:x*maxl+maxl]
		# print 'msg = ' + f
		sock.sendto(f, (ip, port))

	sock.close()


def set_listener():
	
	print 'Set listening values: '
	ip   = str(raw_input("IP   (any): ") or "0.0.0.0")
	port = int(raw_input("Port (" + str(default_port) + "): ") or int(default_port))

	t = threading.Thread(target=recieve_data, args = (ip, port))
	t.daemon = True
	t.start()

	sleep(0.3)
	return t

def set_sender():

	global default_ip
	global default_port
	global default_maxl

	print 'Set sending values: '

	default_ip   = str(raw_input("IP   ("+ default_ip + "): ") or default_ip)
	default_port = int(raw_input("Port (" + str(default_port) + "): ") or int(default_port))
	default_maxl = int(raw_input("Maxl (" + str(default_maxl) + "): ") or int(default_maxl))

	pass



listener = set_listener()
set_sender()

# MAIN LOOP
try:
	while True:

		# while True:
		# 	try:
		# 		send_data()
		# 	except KeyboardInterrupt:
		# 		print '\nYou are now in menu'

		print "Reconfigure sender   (1)"
		print "Send                 (2)"
		mode = int(raw_input('Select (2): ') or 2)
		

		if mode == 1:
			set_sender()
			pass

		if mode == 2:
			send_data()
			pass

except KeyboardInterrupt:
	print '\nBye :)'
	pass
