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
		got = cl_sock.recv(1024)
		print("{} received from {}:{}".format(got.decode(), cl_addr[0], cl_addr[1]))
		if got.decode() == "dc":
			c = False
		
		elif got.decode() == "shutdown":
			cl_sock.close()
			sv_sock.close()
			print("Exiting...")
			raise SystemExit
		
		elif got.decode().startswith("print "):
			if got.decode().split(" ")[1] in locals():
				print("Local: ", end="")
				print(locals()[got.decode().split(" ")[1]])
			elif got.decode().split(" ")[1] in globals():
				print("Global: ", end="")
				print(globals()[got.decode().split(" ")[1]])
			else:
				print("Var {} not found".format(got.decode().split(" ")[1]))

		elif got.decode().startswith("to "):
			dest_addr = got.decode().split(" ")[1]
			dest_port = got.decode().split(" ")[2]
			msg = got.decode().split(" ")[3]
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