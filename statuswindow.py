import tkinter
import json
from pathlib import Path

# ステータスウィンドウのプログラム
class main:
    def __init__(self, default_font, appdata_dir):
        self.appdata_dir = appdata_dir
        self.characters_dir = Path(fr"{self.appdata_dir}/characters/")
        self.default_font = default_font

        status_window = tkinter.Tk()
        status_window.title("キャラクターステータス編集")

        
        skills_dict = {"こぶし": 50, "キック": 25, "頭突き": 10, "組みつき": 25, "投擲": 25, "拳銃": 20, "ライフル": 25, "弓": 10, "こんぼう": 25, "ナイフ": 25, "回避": "DEX×2%", "マーシャルアーツ": 1, "応急手当": 30, "鍵開け": 1, "隠す": 15, "隠れる": 10, "写真術": 10, "変装": 1, "機械修理": 20, "電気修理": 10, "運転": 20, "重機械操作": 1, "コンピュータ": 1, "製作": 5, "操縦": 1, "追跡": 10, "登攀": 40, "忍び歩き": 10, "乗馬": 5, "水泳": 25, "跳躍": 25, "経理": 10, "目星": 25, "聞き耳": 25, "ナビゲート": 10, "言いくるめ": 5, "信用": 15, "説得": 15, "値切り": 5, "オカルト": 5, "精神分析": 1, "図書館": 25, "医学": 5, "化学": 1, "考古学": 1, "人類学": 1, "生物学": 1, "地質学": 1, "電子工学": 1, "天文学": 1, "博物学": 1, "物理学": 1, "薬学": 1, "心理学": 5, "法律": 5, "歴史": 20, "クトゥルフ神話": 0, "芸術": 5, "言語": "EDU×1%", "母国語": "EDU×5%"}
        self.status_list = ["name", "STR", "CON", "POW", "DEX", "APP", "SIZ", "INT", "EDU", "年収", "財産", "SAN", "幸運", "アイデア", "知識", "耐久力", "マジックポイント", "ダメージボーナス"]
        self.entries = {}

        for i, status in enumerate(self.status_list):
            tkinter.Label(status_window, text=f"{status}:", font=self.default_font).grid(row=i, column=0)
            entry = tkinter.Entry(status_window, font=self.default_font)
            entry.grid(row=i, column=1)
            self.entries[status] = entry

        # # キャラクターステータスをロードしてエントリーにセット
        # self.set_character_status_entries(name_entry, san_entry, str_entry, dex_entry, int_entry, con_entry, pow_entry, app_entry, siz_entry, edu_entry, luck_entry)

        # 保存ボタンを追加
        tkinter.Button(status_window, text="保存", command=self.save_character_status).grid(row=16, column=0)

        status_window.mainloop()

    def save_character_status(self):
        name = self.entries["name"].get()

        with open(fr"{self.characters_dir}/{name}.json", "w", encoding="utf-8") as f:
            status = {}
            for key, c in zip(self.status_list, self.entries.values()):
                status[key] = c.get()
            json.dump(status, f, ensure_ascii=False)

    def load_character_status(self, name):
        try:
            with open(fr"{self.characters_dir}/{name}.json", encoding="utf-8") as f:
                return json.loads(f.read())
        except FileNotFoundError:
            return None

    # # キャラクターステータスをJSONから読み込み、エントリーにセットする関数
    # def set_character_status_entries(self, name_entry, san_entry, str_entry, dex_entry, int_entry, con_entry, pow_entry, app_entry, siz_entry, edu_entry, luck_entry):
    #     character_status = self.load_character_status(name_entry.get())
    #     if character_status:
    #         name_entry.insert(0, character_status.get("name", ""))
    #         san_entry.insert(0, character_status.get("SAN", ""))
    #         str_entry.insert(0, character_status.get("STR", ""))
    #         dex_entry.insert(0, character_status.get("DEX", ""))
    #         int_entry.insert(0, character_status.get("INT", ""))
    #         con_entry.insert(0, character_status.get("CON", ""))
    #         pow_entry.insert(0, character_status.get("POW", ""))
    #         app_entry.insert(0, character_status.get("APP", ""))
    #         siz_entry.insert(0, character_status.get("SIZ", ""))
    #         edu_entry.insert(0, character_status.get("EDU", ""))
    #         luck_entry.insert(0, character_status.get("LUCK", ""))

    # # キャラクターステータスをロードする関数
    # def load_character_status(self, name):
    #     try:
    #         with open(f"{name}.json", "r", encoding="utf-8") as f:
    #             return json.load(f)
    #     except FileNotFoundError:
    #         return None