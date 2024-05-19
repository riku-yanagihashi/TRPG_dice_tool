import tkinter
import json
from pathlib import Path

# ステータスウィンドウのプログラム
class main:
    def __init__(self, default_font, appdata_dir, name):
        self.appdata_dir = appdata_dir
        self.characters_dir = Path(fr"{self.appdata_dir}/characters/")
        self.default_font = default_font

        status_window = tkinter.Tk()
        status_window.title("キャラクターステータス編集")

        
        self.skills_dict = {"こぶし": 50, "キック": 25, "頭突き": 10, "組みつき": 25, "投擲": 25, "拳銃": 20, "ライフル": 25, "弓": 10, "こんぼう": 25, "ナイフ": 25, "回避": "DEX×2%", "マーシャルアーツ": 1, "応急手当": 30, "鍵開け": 1, "隠す": 15, "隠れる": 10, "写真術": 10, "変装": 1, "機械修理": 20, "電気修理": 10, "運転": 20, "重機械操作": 1, "コンピュータ": 1, "製作": 5, "操縦": 1, "追跡": 10, "登攀": 40, "忍び歩き": 10, "乗馬": 5, "水泳": 25, "跳躍": 25, "経理": 10, "目星": 25, "聞き耳": 25, "ナビゲート": 10, "言いくるめ": 5, "信用": 15, "説得": 15, "値切り": 5, "オカルト": 5, "精神分析": 1, "図書館": 25, "医学": 5, "化学": 1, "考古学": 1, "人類学": 1, "生物学": 1, "地質学": 1, "電子工学": 1, "天文学": 1, "博物学": 1, "物理学": 1, "薬学": 1, "心理学": 5, "法律": 5, "歴史": 20, "クトゥルフ神話": 0, "芸術": 5, "言語": "EDU×1%", "母国語": "EDU×5%"}
        self.pageddata = []
        for i in range(0, len(self.skills_dict), 15):
            self.pageddata.append(list(self.skills_dict)[i: i+15])

        self.status_list = ["name", "job", "STR", "CON", "POW", "DEX", "APP", "SIZ", "INT", "EDU", "年収", "財産", "SAN", "幸運", "アイデア", "知識", "耐久力", "マジックポイント", "ダメージボーナス",]
        self.entries = {}

        for i, status in enumerate(self.status_list):
            tkinter.Label(status_window, text=f"{status}:", font=self.default_font).grid(row=i, column=0)
            entry = tkinter.Entry(status_window, font=self.default_font)
            entry.grid(row=i, column=1)
            self.entries[status] = entry

        # 保存ボタンを追加
        tkinter.Button(status_window, text="保存",
                    command=self.save_character_status).grid(row=len(self.status_list),
                    column=0) # status_listが増えれば保存ボタンが増えたぶん下に移動するってわけ

        # 「技能を追加」ボタンを配置
        tkinter.Button(status_window, text="技能を追加",
            command=self.add_skills_window).grid(row=len(self.status_list) + 1,
            column=0)

        if name != "":
            self.setvalues(name)

        status_window.mainloop()

    def save_character_status(self):
        self.new_name = self.entries["name"].get()

        with open(fr"{self.characters_dir}/{self.new_name}.json", "w", encoding="utf-8") as f:
            status = {}
            for key, c in zip(self.status_list, self.entries.values()):
                status[key] = c.get()
            json.dump({"base":status}, f, ensure_ascii=False)

    def load_character_status(self, name):
        try:
            with open(fr"{self.characters_dir}/{name}.json", encoding="utf-8") as f:
                return json.loads(f.read())
        except FileNotFoundError:
            return None

    def add_skills_window(self):
        add_skills_window = tkinter.Tk()
        add_skills_window.title("技能を追加")

    def setvalues(self, name):
        status = self.load_character_status(name)
        if status != None:
            for entry, c in zip(self.entries.values(), list(status["base"].values())):
                entry.insert(0, c)
        else:
            for entry in self.entries.values():
                entry.insert(0, "0")

        # pagenum = 0
        # for c in self.pageddata[pagenum]:
        #     cvs = tkinter.Canvas()
        #     cvs.pack()

        #     tkinter.Label(text=c, font=self.default_font).grid(row=0, column=0)
        #     tkinter.Label(text=self.skills_dict[c], font=self.default_font)

        # add_skills_window.mainloop()
