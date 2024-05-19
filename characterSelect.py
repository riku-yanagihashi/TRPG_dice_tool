import tkinter
import glob
from pathlib import Path
import os

# とりあえずself.character_nameに選択したキャラ名を保存するところまではいった
"""
ToDo: (マークダウン)
[ ] ウィンドウを閉じてメインに行く
[ ] キャラクターのステータスを取得して編集の時にその値を出すようにする(これによってstatuswindowを開いたときに空欄じゃなくなる)
[ ] Dexとかのステータス値を計算したうえで表示するようにする
[x] セーブは関数呼び出し一つでできる
↑ここまでがキャラクターセレクト
[ ] キャラクターの切り替えができるようにする(多分characterSelectをもう一度呼び出せばできる)
[ ] =任意= 現在選択しているキャラクターを表示するようにする
"""

class main:
    character_name = ""
    def __init__(self, appdata_dir, default_font):
        self.default_font = default_font
        characters = [os.path.splitext(os.path.basename(file))[0] for file in glob.glob(str(Path(fr"{appdata_dir}/characters/*")))]

        window = tkinter.Tk()

        tkinter.Label(text="~キャラクターを選択~", font=default_font).pack()
        self.buttons = tkinter.Canvas()
        self.buttons.pack()
        for c in characters:
            self.add_select_button(c)

        window.mainloop()

    def set_character_name(self, name):
        self.character_name = name
        print(self.character_name)

    def add_select_button(self, txt):
        tkinter.Button(self.buttons, text=txt, command=lambda:self.set_character_name(txt), font=self.default_font).pack(side="left")

main(fr"{Path(os.getenv('APPDATA')).parent}\\Local\\DiceApp\\", ("Arial", 14))