import socket
import threading

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind(("127.0.0.1", 60013))
soc.listen(200)

def send(txt:str):
    for c in clients:
        try:
            c.send(txt.encode())
        except Exception:
            pass

def clt(client:socket.socket, clientname):
    try:
        while True:
            rcv = client.recv(2048).decode()
            if rcv.startswith("名前変更: "):
                new_name = rcv.split("名前変更: ")[1]
                send(f"{clientname}が名前を{new_name}に変更しました。")
                print(f"{clientname}が名前を{new_name}に変更しました。")
                clientname = new_name  # クライアントの名前を更新
            elif rcv != "":
                send(f"{clientname}: {rcv}")
                print(f"{clientname}: {rcv}")
    except Exception:
        pass

clients = []

while True:
    client, addr = soc.accept()
    initial_name = client.recv(1024).decode()  # クライアントから最初の名前を受け取る
    send(f"{initial_name}が参加しました。")
    print(f"{initial_name}が参加しました。")
    clients.append(client)
    threading.Thread(target=clt, args=(client, initial_name)).start()