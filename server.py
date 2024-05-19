import socket
import threading
import random

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind(("127.0.0.1", 60013))
soc.listen(200)

clients = []
client_colors = {}

# 色の種類
colors = ["red", "green", "blue", "orange", "purple", "brown", "pink"]

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
                client_colors[new_name] = client_colors.pop(clientname)  # 色の情報を更新
                clientname = new_name  # クライアントの名前を新しくする
            elif rcv != "":
                color = client_colors[clientname]
                send(f"{clientname}: {rcv}::{color}")
                print(f"{clientname}: {rcv}::{color}")
    except Exception:
        pass

while True:
    client, addr = soc.accept()
    initial_name = client.recv(1024).decode()  # 参加時の名前を取得
    
    send(f"{initial_name}が参加しました。")
    print(f"{initial_name}が参加しました。")
    
    # プレイヤーに色を割り当てる
    client_color = random.choice(colors)
    client_colors[initial_name] = client_color
    
    # クライアントに色情報を送信
    client.send(f"色: {client_color}".encode())
    
    clients.append(client)
    threading.Thread(target=clt, args=(client, initial_name)).start()
