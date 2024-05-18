import tkinter

import time
import socket
import threading
import random

# ↓サーバーへの接続プログラム===================
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(("153.240.10.7", 60064))

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

tkinter.Label(dicecanvas, text="ダイス:",font=("Arial", 14)).pack(side="left",anchor="n")

D_countBox = tkinter.Entry(dicecanvas, width=2,font=("Arial", 14))
D_countBox.insert(0, "1")
D_countBox.pack(side="left",anchor="n")

tkinter.Label(dicecanvas, text="D",font=("Arial", 14)).pack(side="left",anchor="n")

F_countBox = tkinter.Entry(dicecanvas, width=8,font=("Arial", 14))
F_countBox.insert(0, "100")
F_countBox.pack(side="left",anchor="n")

def diceroll():
    D_count = int(D_countBox.get())
    F_count = int(F_countBox.get())
    cache = []
    for _ in range(D_count):
        cache.append(random.randint(1, F_count))
    soc.send(f"{sum(cache)} ({'+'.join(map(str, cache))})-{D_count}D{F_count}".encode())
    print(sum(cache), "+".join(map(str, cache)))

dice_button = tkinter.Button(dicecanvas, text="ダイスを振る", command=diceroll)
dice_button.pack(side="left",anchor="n")

tkinter.Label(text="ログ:",font=("Arial", 14)).pack(anchor="w")

logbox = tkinter.Text(font=("Arial", 14), state="disabled")
logbox.pack()


chatframe = tkinter.Frame()
tkinter.Label(chatframe, text="チャットを入力:",font=("Arial", 14)).pack(anchor="w", side="left")
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
    logbox.insert(tkinter.END, f"{txt}\n")
    logbox.configure(state="disabled")
    logbox.see("end")

def rcv():
    while True:
        time.sleep(0.1)
        txt = soc.recv(2048).decode()
        insert_to_log(txt)

threading.Thread(target=rcv).start()

def type_event(event):
    match str(event.keysym):
        case "Return":
            if str(window.focus_get()) == ".!frame.!entry":
                sendmessage()

window.bind("<KeyPress>", type_event)

window.mainloop()