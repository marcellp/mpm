import sys, socket, threading, time

sv_addr = "127.0.0.1"
sv_port = 50000

sv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sv_sock.bind((sv_addr, sv_port))


sv_sock.listen(5)

connected = {}

print("Listening on {}:{}".format(sv_addr, sv_port))

def receiver(cl_sock, cl_addr):
	global connected
	c = True
	while c:
		got = cl_sock.recv(1024).decode()
		print("{} received from {}:{}".format(got, cl_addr[0], cl_addr[1]))
		if got == "dc":
			c = False
		
		#Debugging Stuff
		elif got.startswith("print "):
			if got.split(" ")[1] in locals():
				print("Local: ", end="")
				print(locals()[got.split(" ")[1]])
			elif got.split(" ")[1] in globals():
				print("Global: ", end="")
				print(globals()[got.split(" ")[1]])
			else:
				print("Var {} not found".format(got.split(" ")[1]))

		#client --> server --> client
		elif got.startswith("to "):
			dest_addr = got.split(" ")[1]
			dest_port = got.split(" ")[2]
			msg = got[3:]
			connected[(dest_addr, int(dest_port))].send(msg.encode())

	cl_sock.close()
	del connected[cl_addr]
	print("Client has disconnected")

while True:
	cl_sock, cl_addr = sv_sock.accept()
	print("Connection accepted from {}:{}".format(cl_addr[0], cl_addr[1]))
	connected[cl_addr] = cl_sock
	print(connected)
	
	recvHandler = threading.Thread(target = receiver, args = (cl_sock, cl_addr))
	recvHandler.start()