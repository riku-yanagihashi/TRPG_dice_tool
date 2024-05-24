import tkinter
import glob
from pathlib import Path
import os

# とりあえずself.character_nameに選択したキャラ名を保存するところまではいった
"""
ToDo: (マークダウン)
[x] ウィンドウを閉じてメインに行く
[x] キャラクターのステータスを取得して編集の時にその値を出すようにする(これによってstatuswindowを開いたときに空欄じゃなくなる)
[ ] Dexとかのステータス値を計算したうえで表示するようにする
[x] セーブは関数呼び出し一つでできる
↑ここまでがキャラクターセレクト
[x] キャラクターの切り替えができるようにする(多分characterSelectをもう一度呼び出せばできる)
[x] =任意= 現在選択しているキャラクターを表示するようにする
"""


class main:
    character_name = ""

    def __init__(self, appdata_dir, default_font, change_playername):
        self.change_playername = change_playername
        self.default_font = default_font
        characters = [os.path.splitext(os.path.basename(file))[0] for file in glob.glob(
            str(Path(fr"{appdata_dir}/characters/*")))]

        self.characterselect_window = tkinter.Toplevel()
        self.characterselect_window.title = "キャラクター選択"

        tkinter.Label(self.characterselect_window,
                      text="~キャラクターを選択~", font=default_font).pack()
        self.buttons = tkinter.Canvas(self.characterselect_window)
        self.buttons.pack()
        for c in characters:
            self.add_select_button(c)

    def add_select_button(self, txt):
        tkinter.Button(self.buttons, text=txt, command=lambda: self.set_character_name(
            txt), font=self.default_font).pack(side="left")

    def set_character_name(self, name):
        self.character_name = name
        self.change_playername(name)
        self.characterselect_window.destroy()
