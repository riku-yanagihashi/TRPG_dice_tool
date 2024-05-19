import tkinter
import time
import socket
import threading
import random
import os
from pathlib import Path
import csv
import platform
import tkinter.messagebox
import json

saved_dices = {}
default_font = ("Arial", 14)

# アプリケーションのデータ保存フォルダのセットアップ
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
    "saveddice": Path(fr"{appdata_dir}\\savedDice.csv")
}

for c in dataPaths.values():
    c: Path
    if not c.exists():
        c.touch()

# csvからセーブ済みのダイスをロード
with open(dataPaths["saveddice"]) as f:
    reader = csv.reader(f)
    for c in reader:
        if c != []:
            saved_dices[int(c[0])] = (int(c[1]), int(c[2]))

# サーバーへの接続プログラム
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(("127.0.0.1", 60013))

# プレイヤーの色を保存する変数
player_color = None

# コマンドハンドラの処理
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
    logbox.insert(tkinter.END, "システム:ログの履歴を削除しました\n")
    logbox.configure(state="disabled")

# コマンドハンドラにclear_logを登録
register_command("/clear", clear_log)

# 名前を決めるウィンドウのプログラム
namewindow = tkinter.Tk()
tkinter.Label(text="名前を入力してください", font=default_font).pack()
nameentry = tkinter.Entry(font=default_font)
nameentry.pack()

def enter():
    name = nameentry.get()
    if name == "":
        tkinter.messagebox.showwarning(title="警告", message="名前を入力してください。")
    else:
        soc.send(nameentry.get().encode())
        namewindow.destroy()

tkinter.Button(text="決定", command=enter).pack()

def name_close():
    namewindow.destroy()
    soc.close()
    exit()

def name_type_event(event):
    if str(namewindow.focus_get()) == ".!entry" and str(event.keysym) == "Return":
        enter()
namewindow.bind("<KeyPress>", name_type_event)

nameentry.focus_set()

namewindow.protocol("WM_DELETE_WINDOW", name_close)
namewindow.mainloop()

# ダイスを振る、チャットをするウィンドウのプログラム
window = tkinter.Tk()
window.title("ダイス")

main_canvas = tkinter.Canvas()
main_canvas.pack(side="left", anchor="n")

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

# ダイス保存とかの機能
savedice_canvas = tkinter.Canvas()
savedice_canvas.pack(side="left", anchor="n")

tkinter.Label(savedice_canvas, text="保存したダイス", font=default_font).pack(anchor="e")

def addsaveddice(id, D, F):
    diceval_canvas = tkinter.Canvas(savedice_canvas)
    diceval_canvas.pack(side="top", anchor="n")

    diceval_entry = tkinter.Entry(diceval_canvas, font=default_font)
    diceval_entry.insert(0, f"{D}D{F}")
    diceval_entry.configure(state="readonly")
    diceval_entry.pack(side="left")

    roll_button = tkinter.Button(diceval_canvas, text="振る", command=lambda:diceroll(D, F), font=("Arial", 10))
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
        try:
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
        except Exception:
            break

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

    def changewindow_type_event(event):
        if str(event.keysym) == "Return" and str(changewindow.focus_get()) == ".!toplevel.!entry":
            submit_new_name()

    new_name_entry.focus_set()

    changewindow.bind("<KeyPress>", changewindow_type_event)

# 名前変更ボタンを追加
change_name_button = tkinter.Button(main_canvas, text="名前を変更", command=change_name)
change_name_button.pack()

window.bind("<KeyPress>", type_event)

# キャラクターステータスをロードする関数
def load_character_status(name):
    try:
        with open(f"{name}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# キャラクターステータスを保存する関数
def save_character_status(character_status):
    json_file_path = dataPaths["saveddice"].parent / f"character_{len(saved_dices) + 1}.json"
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(character_status, f, ensure_ascii=False)

# キャラクターステータスをJSONから読み込み、エントリーにセットする関数
def set_character_status_entries(name_entry, san_entry, str_entry, dex_entry, int_entry, con_entry, pow_entry, app_entry, siz_entry, edu_entry, luck_entry):
    character_status = load_character_status(name_entry.get())
    if character_status:
        name_entry.insert(0, character_status.get("name", ""))
        san_entry.insert(0, character_status.get("SAN", ""))
        str_entry.insert(0, character_status.get("STR", ""))
        dex_entry.insert(0, character_status.get("DEX", ""))
        int_entry.insert(0, character_status.get("INT", ""))
        con_entry.insert(0, character_status.get("CON", ""))
        pow_entry.insert(0, character_status.get("POW", ""))
        app_entry.insert(0, character_status.get("APP", ""))
        siz_entry.insert(0, character_status.get("SIZ", ""))
        edu_entry.insert(0, character_status.get("EDU", ""))
        luck_entry.insert(0, character_status.get("LUCK", ""))



# クライアントUIのメインウィンドウのプログラム
def main_window():
    window = tkinter.Tk()
    window.title("キャラクターステータス編集")

    default_font = ("Arial", 14)

    tkinter.Label(window, text="名前:", font=default_font).grid(row=0, column=0)
    name_entry = tkinter.Entry(window, font=default_font)
    name_entry.grid(row=0, column=1)

    tkinter.Label(window, text="SAN:", font=default_font).grid(row=1, column=0)
    san_entry = tkinter.Entry(window, font=default_font)
    san_entry.grid(row=1, column=1)

    tkinter.Label(window, text="STR:", font=default_font).grid(row=2, column=0)
    str_entry = tkinter.Entry(window, font=default_font)
    str_entry.grid(row=2, column=1)

    tkinter.Label(window, text="DEX:", font=default_font).grid(row=3, column=0)
    dex_entry = tkinter.Entry(window, font=default_font)
    dex_entry.grid(row=3, column=1)

    tkinter.Label(window, text="INT:", font=default_font).grid(row=4, column=0)
    int_entry = tkinter.Entry(window, font=default_font)
    int_entry.grid(row=4, column=1)

    tkinter.Label(window, text="CON:", font=default_font).grid(row=5, column=0)
    con_entry = tkinter.Entry(window, font=default_font)
    con_entry.grid(row=5, column=1)

    tkinter.Label(window, text="POW:", font=default_font).grid(row=6, column=0)
    pow_entry = tkinter.Entry(window, font=default_font)
    pow_entry.grid(row=6, column=1)

    tkinter.Label(window, text="APP:", font=default_font).grid(row=7, column=0)
    app_entry = tkinter.Entry(window, font=default_font)
    app_entry.grid(row=7, column=1)

    tkinter.Label(window, text="SIZ:", font=default_font).grid(row=8, column=0)
    siz_entry = tkinter.Entry(window, font=default_font)
    siz_entry.grid(row=8, column=1)

    tkinter.Label(window, text="EDU:", font=default_font).grid(row=9, column=0)
    edu_entry = tkinter.Entry(window, font=default_font)
    edu_entry.grid(row=9, column=1)

    tkinter.Label(window, text="LUCK:", font=default_font).grid(row=10, column=0)
    luck_entry = tkinter.Entry(window, font=default_font)
    luck_entry.grid(row=10, column=1)

    # キャラクターステータスをロードしてエントリーにセット
    set_character_status_entries(name_entry, san_entry, str_entry, dex_entry, int_entry, con_entry, pow_entry, app_entry, siz_entry, edu_entry, luck_entry)

    # 保存ボタンを追加
    tkinter.Button(window, text="保存", command=lambda: save_character_status({
        "name": name_entry.get(),
        "SAN": san_entry.get(),
        "STR": str_entry.get(),
        "DEX": dex_entry.get(),
        "INT": int_entry.get(),
        "CON": con_entry.get(),
        "POW": pow_entry.get(),
        "APP": app_entry.get(),
        "SIZ": siz_entry.get(),
        "EDU": edu_entry.get(),
        "LUCK": luck_entry.get()
    })).grid(row=11, column=0)

    window.mainloop()

edit_character_button = tkinter.Button(main_canvas, text="キャラクターステータスを編集", command=main_window)
edit_character_button.pack()

# ============================================================
def window_close():
    window.destroy()
    soc.close()
    exit()

window.protocol("WM_DELETE_WINDOW", window_close)
window.mainloop()
