import socket
import select
import sys
import os

server_address = ('192.168.0.1', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)
FORMAT = "utf-8"

input_socket = [server_socket]
print("Server is ready...")

def cari(filename):
    for file in os.listdir("./dataset/"):
        if file.lower() == filename.lower():
            return file
    return False

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)

            else:
                data = sock.recv(1024)
                print(sock.getpeername(), data)

                if data:
                    input = data.decode(FORMAT)
                    kata = input.split(" ")

                    if kata[0] == 'unduh':
                        filename = kata[1].strip()
                        file = cari(filename)

                        if file is False:
                            messageFileNotFound = bytes('File tidak dapat ditemukan', FORMAT)
                            sock.send(messageFileNotFound)
                        else:
                            path = "./dataset/" + file
                            sizeFile = os.path.getsize(path)
                            sock.send(f"File-name:{file},\nFile-size:{sizeFile}\n\n\n".encode())

                            # mengirim file
                            with open(path, 'rb') as sf:
                                data = sf.read(1024)
                                while (data):
                                    sock.send(data)
                                    data = sf.read(1024)
                            sf.close()
                    else:
                        messageCommandWrong = bytes('Perintah salah. Masukkan dengan format: unduh nama_file', FORMAT)
                        sock.send(messageCommandWrong)

                else:
                    sock.close()
                    input_socket.remove(sock)

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)