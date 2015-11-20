import socket

host = ''
port = 1337

s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

(conn , addr) = s.accept()
test = conn.recv(1024).decode() #decode convers from bytes to string

for i in range(0, len(test)):
  print (test[i])
