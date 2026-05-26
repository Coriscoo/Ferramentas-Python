import socket, sys

ip = sys.argv[1]
porta = int(sys.argv[2])

try:
    meusocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    meusocket.settimeout(5)
    meusocket.connect((ip, porta))
    banner = meusocket.recv(1024)
    print(banner.decode(errors="replace").strip())
except TimeoutError:
    print("Algo deu errado!")
