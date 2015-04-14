# Matej Bellus

import socket
import math

default_ip   = "127.0.0.1"
default_port = 5005
default_maxl = 5


def recieve_data():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	ip   = str(raw_input("IP   ("+ default_ip + "): ") or default_ip)
	port = int(raw_input("Port (" + str(default_port) + "): ") or int(default_port))
	sock.bind((ip, port))

	try:
		print "Listening for data on "+ip+":"+str(port)+" (ctrl+c) to stop"
		while True:
			data, addr = sock.recvfrom(4) # buffer size is 1024 bytes
			print "received message:", data
	except KeyboardInterrupt:
		pass
	pass


def send_data():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	ip   = str(raw_input("IP   ("+ default_ip + "): ") or default_ip)
	port = int(raw_input("Port (" + str(default_port) + "): ") or int(default_port))
	maxl = int(raw_input("Maxl (" + str(default_maxl) + "): ") or int(default_maxl))
	msg  = raw_input('Message: ');
	fragments = int(math.ceil( float(len(msg)) / float(maxl) ))

	print "Sendint to: ", ip, ":", port
	print "MAX : ", maxl
	print "N. of fragments", fragments

	print 'Sending to ' + ip + ":" + str(port) + " as " + str(fragments) + " fragments"
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	for x in range(0, fragments):
		print 'Sending fragment ' + str(x)
		f = msg[x*maxl:x*maxl+maxl]
		print 'msg = ' + f
		sock.sendto(f, (ip, port))

	sock.close()



# MAIN LOOP
try:
	while True:
		print "Recieve (1)"
		print "Send    (2)"
		mode = int(raw_input('Select (1): ') or 1)
		
		if mode == 1:
			recieve_data()
			pass

		if mode == 2:
			send_data()
			pass

		pass
except KeyboardInterrupt:
	print '\nBye :)'
	pass
