import tkinter
import time
import socket
import threading
import random
import os
from pathlib import Path
import csv
import platform


saved_dices = {}

default_font = ("Arial", 14)

# ↓アプリケーションのデータを保存するフォルダのセットアップ
match platform.system():
    case "Windows":
        appdata_dir = fr"{Path(os.getenv('APPDATA')).parent}\\Local\\DiceApp\\"
    case "Darwin":
        appdata_dir = fr"{os.environ['HOME']}/Library/Application Support/DiceApp/"
try:
    os.makedirs(appdata_dir)
except FileExistsError:
    pass

dataPaths = {
    "saveddice":Path(fr"{appdata_dir}\\savedDice.csv")
}

for c in dataPaths.values():
    c:Path
    if not c.exists():
        c.touch()

# csvからセーブ済みのダイスをロード
with open(dataPaths["saveddice"]) as f:
    reader = csv.reader(f)
    for c in reader:
        if c != []:
            saved_dices[int(c[0])] = (int(c[1]), int(c[2]))

# ↓サーバーへの接続プログラム===================
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(("127.0.0.1", 60013))

# プレイヤーの色を保存する変数
player_color = None

# ↓コマンドハンドラの処理========================================
# コマンドハンドラの辞書
command_handlers = {}

# コマンドハンドラを登録する関数
def register_command(command, handler):
    command_handlers[command] = handler

# コマンドを処理する関数
def handle_command(command):
    handler = command_handlers.get(command)
    if handler:
        handler()

def clear_log():
    logbox.configure(state="normal")
    logbox.delete('1.0', tkinter.END)
    logbox.insert(tkinter.END,"システム:ログの履歴を削除しました\n")
    logbox.configure(state="disabled")

# ↑====================================================================

# コマンドハンドラにclear_logを登録
register_command("/clear", clear_log)

# ↓名前を決めるウィンドウのプログラム=============

namewindow = tkinter.Tk()

tkinter.Label(text="名前を入力してください", font=default_font).pack()

nameentry = tkinter.Entry(font=default_font)
nameentry.pack()

def enter():
    soc.send(nameentry.get().encode())
    namewindow.destroy()

tkinter.Button(text="決定", command=enter).pack()

namewindow.mainloop()

# ↓ダイスを振る、チャットをするウィンドウのプログラム===========

window = tkinter.Tk()
window.title("ダイス")

main_canvas = tkinter.Canvas()
main_canvas.pack(side="left",anchor="n")

dicecanvas = tkinter.Canvas(main_canvas)
dicecanvas.pack()

tkinter.Label(dicecanvas, text="ダイス:", font=default_font).pack(side="left", anchor="n")

D_countBox = tkinter.Entry(dicecanvas, width=2, font=default_font)
D_countBox.insert(0, "1")
D_countBox.pack(side="left", anchor="n")

tkinter.Label(dicecanvas, text="D", font=default_font).pack(side="left", anchor="n")

F_countBox = tkinter.Entry(dicecanvas, width=8, font=default_font)
F_countBox.insert(0, "100")
F_countBox.pack(side="left", anchor="n")

def diceroll(d="", f=""):
    D_count = int(D_countBox.get())
    F_count = int(F_countBox.get())
    if d != "":
        D_count = int(d)
    if f != "":
        F_count = int(f)
    cache = []
    for _ in range(D_count):
        cache.append(random.randint(1, F_count))
    soc.send(f"{sum(cache)} ({'+'.join(map(str, cache))})-{D_count}D{F_count}".encode())

def private_diceroll():
    D_count = int(D_countBox.get())
    F_count = int(F_countBox.get())
    cache = []
    for _ in range(D_count):
        cache.append(random.randint(1, F_count))
    result = f"プライベートロール: {sum(cache)} ({'+'.join(map(str, cache))})-{D_count}D{F_count}"
    insert_to_log(result)

dice_button = tkinter.Button(dicecanvas, text="ダイスを振る", command=diceroll)
dice_button.pack(side="left", anchor="n")

private_dice_button = tkinter.Button(dicecanvas, text="プライベートダイスを振る", command=private_diceroll)
private_dice_button.pack(side="left", anchor="n")

# ダイス保存とかの機能
savedice_canvas = tkinter.Canvas()
savedice_canvas.pack(side="left", anchor="n")

tkinter.Label(savedice_canvas, text="保存したダイス", font=default_font).pack(anchor="e")

def addsaveddice(id, D, F):
    diceval_canvas = tkinter.Canvas(savedice_canvas)
    diceval_canvas.pack(side="top",anchor="n")

    diceval_entry = tkinter.Entry(diceval_canvas, font=default_font)
    diceval_entry.insert(0, f"{D}D{F}")
    diceval_entry.configure(state="readonly")
    diceval_entry.pack(side="left")

    roll_button = tkinter.Button(diceval_canvas, text="振る", command=lambda:diceroll(D, F))
    roll_button.pack(side="left")

    def delcanvas(id):
        with open(dataPaths["saveddice"]) as f:
            reader = csv.reader(f)
            rowdata = [c for c in reader if c != [] and c[0] != str(id)]
            with open(dataPaths["saveddice"], "w") as f2:
                writer = csv.writer(f2)
                for c in rowdata:
                    writer.writerow(c)
        diceval_canvas.destroy()

    tkinter.Button(diceval_canvas, text="削除", command=lambda:delcanvas(id)).pack(side="left")

def savedice():
    D_count = int(D_countBox.get())
    F_count = int(F_countBox.get())
    try:
        id = max(list(saved_dices.keys()))+1
    except ValueError:
        id = 0
    saved_dices[id] = (D_count, F_count)
    addsaveddice(id, D_count, F_count)

    with open(dataPaths["saveddice"], "a") as f:
        writer = csv.writer(f)
        writer.writerow([str(id), D_count, F_count])

tkinter.Button(main_canvas, text="ダイスを保存", command=savedice).pack()

for k, c in zip(list(saved_dices.keys()), list(saved_dices.values())):
    addsaveddice(k, c[0], c[1])
#=========================

tkinter.Label(main_canvas, text="ログ:", font=default_font).pack(anchor="w")

logbox = tkinter.Text(main_canvas, font=default_font, state="disabled")
logbox.pack()

chatframe = tkinter.Frame(main_canvas)
tkinter.Label(chatframe, text="チャットを入力:", font=default_font).pack(anchor="w", side="left")
chatentry = tkinter.Entry(chatframe, font=default_font)
chatentry.pack(anchor="w", side="left")

# [チャット欄が空欄],[送信した際の入力欄の内容削除],[enterを押した際にチャットを送信する機能]を追加
def sendmessage():
    msg = chatentry.get()
    if msg != "":
        if msg.startswith("/"):
            handle_command(msg)
        else:
            soc.send(f"「{msg}」".encode())
        chatentry.delete(0, tkinter.END)

sendbutton = tkinter.Button(chatframe, text="送信", command=sendmessage)
sendbutton.pack(anchor="w", side="left")
chatframe.pack()

def insert_to_log(txt):
    logbox.configure(state="normal")
    log_parts = txt.split("::")
    if len(log_parts) == 2:
        logbox.insert(tkinter.END, f"{log_parts[0]}\n", (log_parts[1],))
    else:
        logbox.insert(tkinter.END, f"{txt}\n")
    logbox.configure(state="disabled")
    logbox.see("end")


def rcv():
    global player_color
    while True:
        time.sleep(0.1)
        txt = soc.recv(2048).decode()
        if txt.startswith("色: "):
            player_color = txt.split("色: ")[1]
            logbox.tag_configure(player_color, foreground=player_color)
        else:
            # メッセージに色のタグをつける
            if "::" in txt:
                log_parts = txt.split("::")
                color = log_parts[1]
                if color not in logbox.tag_names():
                    logbox.tag_configure(color, foreground=color)
                insert_to_log(txt)
            else:
                insert_to_log(txt)

threading.Thread(target=rcv).start()

def type_event(event):
    match str(event.keysym):
        case "Return":
            if str(window.focus_get()) == ".!frame.!entry":
                sendmessage()

# 名前を変更するときに出る新しいウィンドウとそのための関数
def change_name():
    changewindow = tkinter.Toplevel()
    tkinter.Label(changewindow, text="新しい名前を入力してください", font=default_font).pack()

    new_name_entry = tkinter.Entry(changewindow, font=default_font)
    new_name_entry.pack()

    def submit_new_name():
        new_name = new_name_entry.get()
        if new_name:
            soc.send(f"名前変更: {new_name}".encode())
            changewindow.destroy()

    tkinter.Button(changewindow, text="名前を変更", command=submit_new_name).pack()

# 名前変更ボタンを追加
change_name_button = tkinter.Button(main_canvas, text="名前を変更", command=change_name)
change_name_button.pack()

window.bind("<KeyPress>", type_event)

window.mainloop()
