import socket
import sys
import math

FORMAT = "utf-8"

def accFile(conn, namaFile, sizeFile):
    find_loop = math.ceil(int(sizeFile) / 1024)
    flag = 0
    with open(namaFile, 'wb') as rf:
        while True:
            data = conn.recv(1024)
            flag += 1
            rf.write(data)
            if find_loop == flag:
                print('\nFile selesai ditransfer.')
                break
    rf.close()


def splitData(received_data):
    namaFile, sizeFile = received_data.split(",\n")
    title_name, namaFile = namaFile.split(":")
    sizeFile = int(''.join(filter(str.isdigit, sizeFile)))

    return namaFile, str(sizeFile)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('192.168.0.1', 5000))
    print('--', end=' ', flush=True)

    try:
        while True:
            message = sys.stdin.readline()
            s.send(bytes(message, FORMAT))
            received_data = s.recv(1024).decode(FORMAT)
            if received_data == 'File tidak dapat ditemukan':
                print(received_data)
            elif received_data == 'Perintah salah. Masukkan dengan format: unduh nama_file':
                print(received_data)
            else:
                namaFile, sizeFile = splitData(received_data)
                print("File-name:", namaFile)
                print("File-Size:", sizeFile)
                accFile(s, namaFile, sizeFile)

            print('--', flush=True, end=' ')

    except KeyboardInterrupt:
        s.close()
        sys.exit(0)
