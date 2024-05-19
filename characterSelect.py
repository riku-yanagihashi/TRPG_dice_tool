import tkinter
import glob
from pathlib import Path
import os

class main:
    character_name = ""
    def __init__(self, appdata_dir, default_font):
        # characters = [os.path.splitext(os.path.basename(file))[0] for file in glob.glob(str(Path(fr"{appdata_dir}/characters/*")))]
        characters = ["A","B","C","D"]

        window = tkinter.Tk()

        tkinter.Label(text="~キャラクターを選択~", font=default_font).pack()
        buttons = tkinter.Canvas()
        buttons.pack()
        for c in characters:
            print(c)
            tkinter.Button(buttons, text=c, command=lambda:self.set_character_name(c), font=default_font).pack(side="left")

        window.mainloop()

    def set_character_name(self, name):
        self.character_name = name
        print(self.character_name)

main(fr"{Path(os.getenv('APPDATA')).parent}\\Local\\DiceApp\\", ("Arial", 14))