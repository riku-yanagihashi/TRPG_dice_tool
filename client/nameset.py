import tkinter
import tkinter.messagebox

# 名前を決めるウィンドウのプログラム


class main:
    def __init__(self, default_font, soc):
        self.soc = soc

        self.namewindow = tkinter.Tk()
        tkinter.Label(text="名前を入力してください", font=default_font).pack()
        self.nameentry = tkinter.Entry(font=default_font)
        self.nameentry.pack()

        tkinter.Button(text="決定", command=self.enter).pack()

        self.namewindow.bind("<KeyPress>", self.type_event)

        self.nameentry.focus_set()

        self.namewindow.protocol("WM_DELETE_WINDOW", self.close)
        self.namewindow.mainloop()

    def enter(self):
        name = self.nameentry.get()
        if name == "":
            tkinter.messagebox.showwarning(title="警告", message="名前を入力してください。")
        else:
            self.soc.send(self.nameentry.get().encode())
            self.namewindow.destroy()

    def close(self):
        self.namewindow.destroy()
        self.soc.close()
        exit()

    def type_event(self, event):
        if str(self.namewindow.focus_get()) == ".!entry" and str(event.keysym) == "Return":
            self.enter()
