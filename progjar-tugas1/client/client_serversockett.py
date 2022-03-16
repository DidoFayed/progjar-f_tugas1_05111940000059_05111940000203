import socket
import sys
import math

ipaddress = '192.168.0.1'
port = 5000


def file_recv(conn, file_name, file_size):
    find_loop = math.ceil(int(file_size) / 1024)
    flag = 0
    with open(file_name, 'wb') as rf:
        while True:
            data = conn.recv(1024)
            flag += 1
            rf.write(data)
            # print(flag, max_loop)
            if find_loop == flag:
                print('\nFile selesai ditransfer.')
                break
    rf.close()

def splitData(recv):
    file_name, file_size = recv.split(",\n")
    title_name, file_name = file_name.split(":")
    file_size = filter(str.isdigit, file_size)
    file_size = int(''.join(file_size))
    
    return file_name, str(file_size)


# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((ipaddress, port))
    # Connect to server and send data
    print('>>', end=' ', flush=True)
    try:
        while True:
            message = sys.stdin.readline()
            sock.send(bytes(message, 'utf-8'))
            recv = sock.recv(1024).decode('utf-8')
            if recv == 'File tidak dapat ditemukan' or 'Perintah salah. Masukkan -> unduh nama_file':
                print(recv)
            else:
                # TO DO: cari parsing
                file_name, file_size = splitData(recv)
                print("File-name:", file_name)
                print("File-Size:", file_size)
                # File-name: coba.txt
                # File-size:33\n\n\n
                file_recv(sock, file_name, file_size)

            print('>>', flush=True, end=' ')

    except KeyboardInterrupt:
        sock.close()
        sys.exit(0)



