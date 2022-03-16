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
print("Server is listening...\n")

def cari(namaFile):
    for file in os.listdir("./dataset/"):
        if file.lower() == namaFile.lower():
            return namaFile
    return False

def kirim(path, koneksi):
    with open(path,'rb') as f: #rb->open file in binary format for reading
        l = f.read(1024)
        while (l):
            koneksi.send(l)
            l = f.read(1024)
            #print("Mengirim file\n")
        f.close()

        #print("Selesai.")
        #koneksi.close()

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        #select -- bisa melayani banyak client

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)

            else:
                data = sock.recv(1024)
                print(sock.getpeername(), data)

                if data:
                    #sock.send(data)
                    nama = data.decode(FORMAT)
                    namainput = nama.split(" ") #memisah string
                    if namainput[0] == 'unduh':
                        namaFile = namainput[1].strip()
                        hasil = cari(namaFile)
                        while hasil is not False:
                            path = "./dataset/" + hasil
                            size = os.path.getsize(path)
                            sock.send(f"Nama file: {hasil} \nUkuran file: {size}\n\n\n".encode())
                            kirim(path, sock)
                        sock.send(bytes('File tidak dapat ditemukan', FORMAT))
                        #ngirim dari server ke client--muncul di terminal client
                    else:
                        sock.send(bytes('Perintah salah. Masukkan format: unduh nama_file', FORMAT))

                else:
                    sock.close()
                    input_socket.remove(sock)

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)
