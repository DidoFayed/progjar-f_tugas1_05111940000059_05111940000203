import socket
import sys
import math

server_address = ('192.168.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)
FORMAT = "utf-8"

#sys.stdout.write('>> ')

try:
    while True:
        message = sys.stdin.readline()
        client_socket.send(bytes(message, FORMAT))
        received_data = client_socket.recv(1024).decode(FORMAT)
        #sys.stdout.write(received_data)
        #sys.stdout.write('>> ')
        if received_data == 'File tidak dapat ditemukan' or 'Perintah salah. Masukkan format unduh nama-file':
            print(received_data)
        else:
            namaFile, size = received_data.split(",\n")
            namaFile = namaFile.split(":")
            size = int(''.join(filter(str.isdigit, size)))

            print(namaFile)
            print(size)

            with open(namaFile, 'wb') as f:
                while True:
                    data = client_socket.recv(1024)
                    f.write(data)

                    if len(data) < 1024:
                        break
                    else:
                        data = client_socket.recv(1024)

            f.close()


except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)