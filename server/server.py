import os
import socket, threading, random

from dotenv import load_dotenv
from os.path import join, dirname


import datas, jsonloader


# サーバーIPとサーバーポートを.envから読み込み
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
_ip = os.getenv("SERVER_IP")
_port = int(os.getenv("SERVER_PORT"))

# サーバー起動
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((_ip, _port))
soc.listen(200)

clients = []
client_colors = {}

# 色の種類
colors = ["red", "green", "blue", "orange", "purple", "brown", "pink"]


def send(txt: str):
    print(txt)
    for c in clients:
        try:
            c.send(txt.encode())
        except Exception:
            pass


def clt(client: socket.socket, clientname):
    try:
        while True:
            rcv = client.recv(2048).decode()
            if not rcv.startswith("/@"):
                color = client_colors[clientname]
                send(f"{clientname}: {rcv}::{color}")
            else:
                command_args = rcv.split()
                match command_args[0][2:]:
                    # クライアントの表示名の変更
                    case "changename":
                        new_name = command_args[1]
                        send(f"{clientname}が名前を{new_name}に変更しました。")
                        client_colors[new_name] = client_colors.pop(clientname)  # 色の情報を更新
                        clientname = new_name  # クライアントの名前を新しくする
                    case "update":
                        version = command_args[1]
                        os_name = command_args[2]
                        client.send(str(jsonloader.loadjsondata(version, os_name)).encode())
    except Exception:
        pass

print("=====<Diceサーバー起動>=====")

while True:
    client, addr = soc.accept()
    client.send(datas.latest_version.encode())
    try:
        initial_name = client.recv(1024).decode()  # 参加時の名前を取得

        send(f"{initial_name}が参加しました。")

        # プレイヤーに色を割り当てる
        client_color = random.choice(colors)
        client_colors[initial_name] = client_color

        # クライアントに色情報を送信
        client.send(f"色: {client_color}".encode())

        clients.append(client)
        threading.Thread(target=clt, args=(client, initial_name)).start()
    except Exception:
        print(f"{addr}の接続が開始前に切断")
