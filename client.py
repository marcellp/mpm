import sys, socket, threading

sv_addr = "127.0.0.1"
sv_port = 50000

cl_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cl_sock.connect((sv_addr, sv_port))

def send(msg):
    cl_sock.send(msg.encode())

def receiver(cl_sock):
	c = True
	while c:
		got = cl_sock.recv(1024).decode()
		sender_addr = got.split(" ")[0]
		sender_port = got.split(" ")[1]
		got = " ".join(got.split(" ")[2:])
		print("Got message: \"{}\"\nFrom {}:{}".format(got, sender_addr, sender_port))

recvHandler = threading.Thread(target = receiver, args = (cl_sock,))