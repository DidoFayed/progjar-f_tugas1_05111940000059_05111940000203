import socket
import threading
import socketserver
import os

ipaddress = '192.168.0.1'
port = 5000

#input_socket = [server_socket]
sourcePath = "./dataset/"

def cari(file_name):
    for file in os.listdir(sourcePath):
        if file.lower() == file_name.lower():
            return file
    return False


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        cur_thread = threading.current_thread()
        while True:
            self.data = self.request.recv(1024)
            print(self.request.getpeername(), self.data)

            if self.data:
                    kata = self.data.decode('utf-8')
                    splitKata = kata.split(" ")
                    if splitKata[0] == 'unduh':
                        file_name = splitKata[1]
                        file_name = file_name.strip()
                        resultFile = cari(file_name)

                        if resultFile is False:
                            self.request.send(bytes('File tidak dapat ditemukan', 'utf-8'))
                        else:
                            path_file = sourcePath + resultFile
                            size_file = os.path.getsize(path_file)
                            self.request.send(f"File-name:{resultFile},\nFile-size:{size_file}\n\n\n".encode())
                            #sendFile(path_file, self.request)

                            # mengirim file
                            with open(path_file, "rb") as sf:
                                data = sf.read(1024)
                                while (data):
                                    self.request.send(data)
                                    data = sf.read(1024)
                            sf.close()

                    else:
                        self.request.send(bytes('Perintah salah. Masukkan dengan format: unduh nama_file', 'utf-8'))

            else:
                return


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


with ThreadedTCPServer((ipaddress, port), ThreadedTCPRequestHandler) as s:
        try:
            s.serve_forever()

        except KeyboardInterrupt:
            print('selesai')
            s.shutdown()
