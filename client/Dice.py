import socket
import os
from pathlib import Path
import platform
import tkinter.messagebox

import mainwindow
import nameset
import statuswindow


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
    "saveddice": Path(fr"{appdata_dir}/savedDice.csv")
}

print(dataPaths["saveddice"])
for c in dataPaths.values():
    c: Path
    if not c.exists():
        c.touch()

# キャラクターデータを保存するフォルダの作成
try:
    os.makedirs(fr"{appdata_dir}/characters/")
except FileExistsError:
    pass


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def serverconnect(server_addr):
    try:
        soc.connect(server_addr)
        return True
    except Exception:
        return False


# サーバーへの接続プログラム
server_addr = ("153.240.10.7", 60065)
while True:
    "124.100.76.59"
    if serverconnect(server_addr):
        break
    elif tkinter.messagebox.askyesno(title="接続エラー", message="サーバーへの接続に失敗しました。\n接続先のIPを変更しますか?"):
        reconnet_window = tkinter.Tk()
        tkinter.Label(text="新しいIPアドレス").pack()
        new_ip_entry = tkinter.Entry()
        new_ip_entry.pack()

        def reconnect():
            new_ip = new_ip_entry.get()
            global server_addr
            server_addr = (new_ip, 60013)
            global reconnet_window
            reconnet_window.destroy()
        tkinter.Button(text="変更して再接続", command=reconnect).pack()
        reconnet_window.protocol("WM_DELETE_WINDOW", exit)
        reconnet_window.mainloop()
    else:
        exit()


nameset.main(default_font, soc)

mainclass = mainwindow.main(
    soc, default_font, statuswindow.main, dataPaths, appdata_dir)
