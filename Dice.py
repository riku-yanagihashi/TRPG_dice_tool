import tkinter
import time
import socket
import threading
import random

# ↓サーバーへの接続プログラム===================
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(("127.0.0.1", 60013))

# プレイヤーの色を保存する変数
player_color = None

# ↓名前を決めるウィンドウのプログラム=============

namewindow = tkinter.Tk()

tkinter.Label(text="名前を入力してください", font=("Arial", 14)).pack()

nameentry = tkinter.Entry(font=("Arial", 14))
nameentry.pack()

def enter():
    soc.send(nameentry.get().encode())
    namewindow.destroy()

tkinter.Button(text="決定", command=enter).pack()

namewindow.mainloop()

# ↓ダイスを振る、チャットをするウィンドウのプログラム===========

window = tkinter.Tk()
window.title("ダイス")

dicecanvas = tkinter.Canvas()
dicecanvas.pack()

tkinter.Label(dicecanvas, text="ダイス:", font=("Arial", 14)).pack(side="left", anchor="n")

D_countBox = tkinter.Entry(dicecanvas, width=2, font=("Arial", 14))
D_countBox.insert(0, "1")
D_countBox.pack(side="left", anchor="n")

tkinter.Label(dicecanvas, text="D", font=("Arial", 14)).pack(side="left", anchor="n")

F_countBox = tkinter.Entry(dicecanvas, width=8, font=("Arial", 14))
F_countBox.insert(0, "100")
F_countBox.pack(side="left", anchor="n")

def diceroll():
    D_count = int(D_countBox.get())
    F_count = int(F_countBox.get())
    cache = []
    for _ in range(D_count):
        cache.append(random.randint(1, F_count))
    soc.send(f"{sum(cache)} ({'+'.join(map(str, cache))})-{D_count}D{F_count}".encode())
    print(sum(cache), "+".join(map(str, cache)))

def private_diceroll():
    D_count = int(D_countBox.get())
    F_count = int(F_countBox.get())
    cache = []
    for _ in range(D_count):
        cache.append(random.randint(1, F_count))
    result = f"プライベートロール: {sum(cache)} ({'+'.join(map(str, cache))})-{D_count}D{F_count}"
    print(result)
    insert_to_log(result)

dice_button = tkinter.Button(dicecanvas, text="ダイスを振る", command=diceroll)
dice_button.pack(side="left", anchor="n")

private_dice_button = tkinter.Button(dicecanvas, text="プライベートダイスを振る", command=private_diceroll)
private_dice_button.pack(side="left", anchor="n")

tkinter.Label(text="ログ:", font=("Arial", 14)).pack(anchor="w")

logbox = tkinter.Text(font=("Arial", 14), state="disabled")
logbox.pack()

chatframe = tkinter.Frame()
tkinter.Label(chatframe, text="チャットを入力:", font=("Arial", 14)).pack(anchor="w", side="left")
chatentry = tkinter.Entry(chatframe, font=("Arial", 14))
chatentry.pack(anchor="w", side="left")

# [チャット欄が空欄],[送信した際の入力欄の内容削除],[enterを押した際にチャットを送信する機能]を追加
def sendmessage():
    msg = chatentry.get()
    if msg != "":
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
    tkinter.Label(changewindow, text="新しい名前を入力してください", font=("Arial", 14)).pack()

    new_name_entry = tkinter.Entry(changewindow, font=("Arial", 14))
    new_name_entry.pack()

    def submit_new_name():
        new_name = new_name_entry.get()
        if new_name:
            soc.send(f"名前変更: {new_name}".encode())
            changewindow.destroy()

    tkinter.Button(changewindow, text="名前を変更", command=submit_new_name).pack()

# 名前変更ボタンを追加
change_name_button = tkinter.Button(window, text="名前を変更", command=change_name)
change_name_button.pack()

window.bind("<KeyPress>", type_event)

window.mainloop()