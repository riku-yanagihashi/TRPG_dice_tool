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

import mainwindow


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



# サーバーへの接続プログラム
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(("127.0.0.1", 60013))

# プレイヤーの色を保存する変数
player_color = None

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


# キャラクターステータスをロードする関数
def load_character_status(name):
    try:
        with open(f"{name}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# キャラクターステータスを保存する関数
def save_character_status(character_status):
    json_file_path = dataPaths["saveddice"].parent / f"character.json"
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
    status_window = tkinter.Tk()
    status_window.title("キャラクターステータス編集")

    default_font = ("Arial", 14)

    tkinter.Label(status_window, text="名前:", font=default_font).grid(row=0, column=0)
    name_entry = tkinter.Entry(status_window, font=default_font)
    name_entry.grid(row=0, column=1)

    tkinter.Label(status_window, text="SAN:", font=default_font).grid(row=1, column=0)
    san_entry = tkinter.Entry(status_window, font=default_font)
    san_entry.grid(row=1, column=1)

    tkinter.Label(status_window, text="STR:", font=default_font).grid(row=2, column=0)
    str_entry = tkinter.Entry(status_window, font=default_font)
    str_entry.grid(row=2, column=1)

    tkinter.Label(status_window, text="DEX:", font=default_font).grid(row=3, column=0)
    dex_entry = tkinter.Entry(status_window, font=default_font)
    dex_entry.grid(row=3, column=1)

    tkinter.Label(status_window, text="INT:", font=default_font).grid(row=4, column=0)
    int_entry = tkinter.Entry(status_window, font=default_font)
    int_entry.grid(row=4, column=1)

    tkinter.Label(status_window, text="CON:", font=default_font).grid(row=5, column=0)
    con_entry = tkinter.Entry(status_window, font=default_font)
    con_entry.grid(row=5, column=1)

    tkinter.Label(status_window, text="POW:", font=default_font).grid(row=6, column=0)
    pow_entry = tkinter.Entry(status_window, font=default_font)
    pow_entry.grid(row=6, column=1)

    tkinter.Label(status_window, text="APP:", font=default_font).grid(row=7, column=0)
    app_entry = tkinter.Entry(status_window, font=default_font)
    app_entry.grid(row=7, column=1)

    tkinter.Label(status_window, text="SIZ:", font=default_font).grid(row=8, column=0)
    siz_entry = tkinter.Entry(status_window, font=default_font)
    siz_entry.grid(row=8, column=1)

    tkinter.Label(status_window, text="EDU:", font=default_font).grid(row=9, column=0)
    edu_entry = tkinter.Entry(status_window, font=default_font)
    edu_entry.grid(row=9, column=1)

    tkinter.Label(status_window, text="LUCK:", font=default_font).grid(row=10, column=0)
    luck_entry = tkinter.Entry(status_window, font=default_font)
    luck_entry.grid(row=10, column=1)

    # キャラクターステータスをロードしてエントリーにセット
    set_character_status_entries(name_entry, san_entry, str_entry, dex_entry, int_entry, con_entry, pow_entry, app_entry, siz_entry, edu_entry, luck_entry)

    # 保存ボタンを追加
    tkinter.Button(status_window, text="保存", command=lambda: save_character_status({
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

    status_window.mainloop()





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
    mainclass.clear()

# コマンドハンドラにclear_logを登録
register_command("/clear", clear_log)


mainclass = mainwindow.main(soc, default_font, main_window, handle_command, dataPaths)
# ============================================================

