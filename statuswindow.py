import tkinter
import json

# ステータスウィンドウのプログラム
class main:
    def __init__(self, default_font, dataPaths):
        self.dataPaths = dataPaths
        self.default_font = default_font

        status_window = tkinter.Tk()
        status_window.title("キャラクターステータス編集")

        tkinter.Label(status_window, text="名前:", font=self.default_font).grid(row=0, column=0)
        name_entry = tkinter.Entry(status_window, font=self.default_font)
        name_entry.grid(row=0, column=1)

        tkinter.Label(status_window, text="SAN:", font=self.default_font).grid(row=1, column=0)
        san_entry = tkinter.Entry(status_window, font=self.default_font)
        san_entry.grid(row=1, column=1)

        tkinter.Label(status_window, text="STR:", font=self.default_font).grid(row=2, column=0)
        str_entry = tkinter.Entry(status_window, font=self.default_font)
        str_entry.grid(row=2, column=1)

        tkinter.Label(status_window, text="DEX:", font=self.default_font).grid(row=3, column=0)
        dex_entry = tkinter.Entry(status_window, font=self.default_font)
        dex_entry.grid(row=3, column=1)

        tkinter.Label(status_window, text="INT:", font=self.default_font).grid(row=4, column=0)
        int_entry = tkinter.Entry(status_window, font=self.default_font)
        int_entry.grid(row=4, column=1)

        tkinter.Label(status_window, text="CON:", font=self.default_font).grid(row=5, column=0)
        con_entry = tkinter.Entry(status_window, font=self.default_font)
        con_entry.grid(row=5, column=1)

        tkinter.Label(status_window, text="POW:", font=self.default_font).grid(row=6, column=0)
        pow_entry = tkinter.Entry(status_window, font=self.default_font)
        pow_entry.grid(row=6, column=1)

        tkinter.Label(status_window, text="APP:", font=self.default_font).grid(row=7, column=0)
        app_entry = tkinter.Entry(status_window, font=self.default_font)
        app_entry.grid(row=7, column=1)

        tkinter.Label(status_window, text="SIZ:", font=self.default_font).grid(row=8, column=0)
        siz_entry = tkinter.Entry(status_window, font=self.default_font)
        siz_entry.grid(row=8, column=1)

        tkinter.Label(status_window, text="EDU:", font=self.default_font).grid(row=9, column=0)
        edu_entry = tkinter.Entry(status_window, font=self.default_font)
        edu_entry.grid(row=9, column=1)

        tkinter.Label(status_window, text="LUCK:", font=self.default_font).grid(row=10, column=0)
        luck_entry = tkinter.Entry(status_window, font=self.default_font)
        luck_entry.grid(row=10, column=1)

        # キャラクターステータスをロードしてエントリーにセット
        self.set_character_status_entries(name_entry, san_entry, str_entry, dex_entry, int_entry, con_entry, pow_entry, app_entry, siz_entry, edu_entry, luck_entry)

        # 保存ボタンを追加
        tkinter.Button(status_window, text="保存", command=lambda: self.save_character_status({
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

    # キャラクターステータスをJSONから読み込み、エントリーにセットする関数
    def set_character_status_entries(self, name_entry, san_entry, str_entry, dex_entry, int_entry, con_entry, pow_entry, app_entry, siz_entry, edu_entry, luck_entry):
        character_status = self.load_character_status(name_entry.get())
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

    # キャラクターステータスを保存する関数
    def save_character_status(self, character_status):
        json_file_path = self.dataPaths["saveddice"].parent / f"character.json"
        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(character_status, f, ensure_ascii=False)

    # キャラクターステータスをロードする関数
    def load_character_status(self, name):
        try:
            with open(f"{name}.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return None