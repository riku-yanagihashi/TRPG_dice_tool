import socket
import os
from pathlib import Path
import platform

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
    "saveddice": Path(fr"{appdata_dir}\\savedDice.csv")
}

for c in dataPaths.values():
    c: Path
    if not c.exists():
        c.touch()

# キャラクターデータを保存するフォルダの作成
try:
    os.makedirs(fr"{appdata_dir}/characters/")
except FileExistsError:
    pass

# サーバーへの接続プログラム
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(("127.0.0.1", 60013))

nameset.main(default_font, soc)

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


mainclass = mainwindow.main(soc, default_font, statuswindow.main, handle_command, dataPaths, appdata_dir)
# ============================================================

