import tkinter
import threading
import csv
import time
import random



# ダイスを振る、チャットをするウィンドウのプログラム
class main:
    def __init__(self, soc, default_font, main_window, handle_command, dataPaths):
        self.soc = soc
        self.dataPaths = dataPaths

        self.default_font = default_font
        self.saved_dices = {}

        self.main_window = main_window
        self.handle_command = handle_command

        # csvからセーブ済みのダイスをロード
        with open(self.dataPaths["saveddice"]) as f:
            reader = csv.reader(f)
            for c in reader:
                if c != []:
                    self.saved_dices[int(c[0])] = (int(c[1]), int(c[2]))


        self.window = tkinter.Tk()
        self.window.title("ダイス")

        main_canvas = tkinter.Canvas()
        main_canvas.pack(side="left", anchor="n")

        dicecanvas = tkinter.Canvas(main_canvas)
        dicecanvas.pack()

        tkinter.Label(dicecanvas, text="ダイス:", font=self.default_font).pack(side="left", anchor="n")

        self.D_countBox = tkinter.Entry(dicecanvas, width=2, font=self.default_font)
        self.D_countBox.insert(0, "1")
        self.D_countBox.pack(side="left", anchor="n")

        tkinter.Label(dicecanvas, text="D", font=self.default_font).pack(side="left", anchor="n")

        self.F_countBox = tkinter.Entry(dicecanvas, width=8, font=self.default_font)
        self.F_countBox.insert(0, "100")
        self.F_countBox.pack(side="left", anchor="n")

        dice_button = tkinter.Button(dicecanvas, text="ダイスを振る", command=self.diceroll)
        dice_button.pack(side="left", anchor="n")

        tkinter.Button(dicecanvas, text="プライベートダイスを振る", command=self.private_diceroll).pack(side="left", anchor="n")

        # ダイス保存とかの機能
        self.savedice_canvas = tkinter.Canvas()
        self.savedice_canvas.pack(side="left", anchor="n")

        tkinter.Label(self.savedice_canvas, text="保存したダイス", font=self.default_font).pack(anchor="e")

        tkinter.Button(main_canvas, text="ダイスを保存", command=self.savedice).pack()

        for k, c in zip(list(self.saved_dices.keys()), list(self.saved_dices.values())):
            self.addsaveddice(k, c[0], c[1])

        tkinter.Label(main_canvas, text="ログ:", font=self.default_font).pack(anchor="w")

        self.logbox = tkinter.Text(main_canvas, font=self.default_font, state="disabled")
        self.logbox.pack()

        chatframe = tkinter.Frame(main_canvas)
        tkinter.Label(chatframe, text="チャットを入力:", font=self.default_font).pack(anchor="w", side="left")
        self.chatentry = tkinter.Entry(chatframe, font=self.default_font)
        self.chatentry.pack(anchor="w", side="left")

        sendbutton = tkinter.Button(chatframe, text="送信", command=self.sendmessage)
        sendbutton.pack(anchor="w", side="left")
        chatframe.pack()

        threading.Thread(target=self.rcv).start()

        # 名前変更ボタンを追加
        change_name_button = tkinter.Button(main_canvas, text="名前を変更", command=self.change_name)
        change_name_button.pack()

        self.window.bind("<KeyPress>", self.type_event)

        edit_character_button = tkinter.Button(main_canvas, text="キャラクターステータスを編集", command=self.main_window)
        edit_character_button.pack()

        self.window.protocol("WM_DELETE_WINDOW", self.window_close)
        self.window.mainloop()

    def diceroll(self, d="", f=""):
        D_count = int(self.D_countBox.get())
        F_count = int(self.F_countBox.get())
        if d != "":
            D_count = int(d)
        if f != "":
            F_count = int(f)
        cache = []
        for _ in range(D_count):
            cache.append(random.randint(1, F_count))
        self.soc.send(f"{sum(cache)} ({'+'.join(map(str, cache))})-{D_count}D{F_count}".encode())

    def private_diceroll(self):
        D_count = int(self.D_countBox.get())
        F_count = int(self.F_countBox.get())
        cache = []
        for _ in range(D_count):
            cache.append(random.randint(1, F_count))
        result = f"プライベートロール: {sum(cache)} ({'+'.join(map(str, cache))})-{D_count}D{F_count}"
        self.insert_to_log(result)

    def addsaveddice(self, id, D, F):
        diceval_canvas = tkinter.Canvas(self.savedice_canvas)
        diceval_canvas.pack(side="top", anchor="n")

        diceval_entry = tkinter.Entry(diceval_canvas, font=self.default_font)
        diceval_entry.insert(0, f"{D}D{F}")
        diceval_entry.configure(state="readonly")
        diceval_entry.pack(side="left")

        roll_button = tkinter.Button(diceval_canvas, text="振る", command=lambda:self.diceroll(D, F), font=("Arial", 10))
        roll_button.pack(side="left")

        def delcanvas(id):
            with open(self.dataPaths["saveddice"]) as f:
                reader = csv.reader(f)
                rowdata = [c for c in reader if c != [] and c[0] != str(id)]
                with open(self.dataPaths["saveddice"], "w") as f2:
                    writer = csv.writer(f2)
                    for c in rowdata:
                        writer.writerow(c)
            diceval_canvas.destroy()

        tkinter.Button(diceval_canvas, text="削除", command=lambda:delcanvas(id)).pack(side="left")

    def savedice(self):
        D_count = int(self.D_countBox.get())
        F_count = int(self.F_countBox.get())
        try:
            id = max(list(self.saved_dices.keys()))+1
        except ValueError:
            id = 0
        self.saved_dices[id] = (D_count, F_count)
        self.addsaveddice(id, D_count, F_count)

        with open(self.dataPaths["saveddice"], "a") as f:
            writer = csv.writer(f)
            writer.writerow([str(id), D_count, F_count])

# [チャット欄が空欄],[送信した際の入力欄の内容削除],[enterを押した際にチャットを送信する機能]を追加
    def sendmessage(self):
        msg = self.chatentry.get()
        if msg != "":
            if msg.startswith("/"):
                self.handle_command(msg)
            else:
                self.soc.send(f"「{msg}」".encode())
            self.chatentry.delete(0, tkinter.END)

    def insert_to_log(self, txt):
        self.logbox.configure(state="normal")
        log_parts = txt.split("::")
        if len(log_parts) == 2:
            self.logbox.insert(tkinter.END, f"{log_parts[0]}\n", (log_parts[1],))
        else:
            self.logbox.insert(tkinter.END, f"{txt}\n")
        self.logbox.configure(state="disabled")
        self.logbox.see("end")

    def rcv(self):
        global player_color
        while True:
            time.sleep(0.1)
            try:
                txt = self.soc.recv(2048).decode()
                if txt.startswith("色: "):
                    player_color = txt.split("色: ")[1]
                    self.logbox.tag_configure(player_color, foreground=player_color)
                else:
                    # メッセージに色のタグをつける
                    if "::" in txt:
                        log_parts = txt.split("::")
                        color = log_parts[1]
                        if color not in self.logbox.tag_names():
                            self.logbox.tag_configure(color, foreground=color)
                        self.insert_to_log(txt)
                    else:
                        self.insert_to_log(txt)
            except Exception:
                break

    def type_event(self, event):
        match str(event.keysym):
            case "Return":
                if str(self.window.focus_get()) == ".!frame.!entry":
                    self.sendmessage()

# 名前を変更するときに出る新しいウィンドウとそのための関数
    def change_name(self):
        changewindow = tkinter.Toplevel()

        tkinter.Label(changewindow, text="新しい名前を入力してください", font=self.default_font).pack()

        new_name_entry = tkinter.Entry(changewindow, font=self.default_font)
        new_name_entry.pack()

        def submit_new_name():
            new_name = new_name_entry.get()
            if new_name:
                self.soc.send(f"名前変更: {new_name}".encode())
                changewindow.destroy()

        tkinter.Button(changewindow, text="名前を変更", command=submit_new_name).pack()

        def changewindow_type_event(event):
            if str(event.keysym) == "Return" and str(changewindow.focus_get()) == ".!toplevel.!entry":
                submit_new_name()

        new_name_entry.focus_set()

        changewindow.bind("<KeyPress>", changewindow_type_event)

    def window_close(self):
        self.window.destroy()
        self.soc.close()
        exit()

    def clear(self):
        self.logbox.configure(state="normal")
        self.logbox.delete('1.0', tkinter.END)
        self.logbox.insert(tkinter.END, "システム:ログの履歴を削除しました\n")
        self.logbox.configure(state="disabled")