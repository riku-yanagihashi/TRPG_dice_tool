import socket
import threading

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind(("192.168.1.221", 60064))
soc.listen(200)

def send(txt:str):
    for c in clients:
        try:
            c.send(txt.encode())
        except Exception:
            pass

def clt(client:socket.socket):
    try:
        _clientname = client.recv(1024).decode()
        send(f"{_clientname}が参加しました。")
        print(f"{_clientname}が参加しました。")
        while True:
            rcv = ""
            rcv = client.recv(2048).decode()
            if rcv != "":
                send(f"{_clientname}:{rcv}")
                print(f"{_clientname}:{rcv}")
    except Exception:
        pass

clients = []

while True:
    client, addr = soc.accept()
    clients.append(client)
    threading.Thread(target=clt, args=(client, )).start()